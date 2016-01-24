#!/usr/bin/python
# -*- coding: utf-8 -*-  

import sys,os,subprocess,tempfile
script_path = os.path.abspath(sys.argv[0][:sys.argv[0].rfind('/')])
os.chdir(script_path)
common_path = os.path.abspath('..') + '/'
sys.path.append(common_path)
import common

key_var = ['x']
c_file_name = 'sample.c'
repair_file_name = 'repair.sample.c'
repair_line = 11


def replace(file_in_name, file_out_name, para):
	file_in = open(file_in_name, 'r')
	all_lines = file_in.readlines()
	file_in.close()
	file_out = open(file_out_name, 'w')
	# 不改变不涉及输入数据的语句
	for line in all_lines[:3]:
		file_out.write(line)
	# 得到变量名，在这个样例中是a[0],a[1],a[2],a[3],a[4]
	para_name = all_lines[3].split()
	# 替换为输入数据
	file_out.write('	%s = %s;\n' %(para_name[0], para[0]))
	# 不改变不涉及输入数据的语句
	for line in all_lines[4:]:
		file_out.write(line)
	file_out.close()

def replace_satabs(file_out_name, para):
	file_in = open('sample_satabs.bp', 'r')
	all_lines = file_in.readlines()
	file_in.close()
	file_out = open(file_out_name, 'w')
	# 不改变不涉及重新赋值的语句
	for line in all_lines[:57]:
		file_out.write(line)
	# 对相关的布尔变量重新赋值
	replace_string = all_lines[57][:all_lines[57].find(':=')+3]
	deli = ','
	if int(para[0]) == 0:
		replace_string = replace_string + '1' + deli
	else:
		replace_string = replace_string + '0' + deli
	if int(para[0]) > 1:
		replace_string = replace_string + '1' + deli
	else:
		replace_string = replace_string + '0' + deli
	if int(para[0]) == 1:
		replace_string = replace_string + '1' + deli
	else:
		replace_string = replace_string + '0' + deli
	if int(para[0]) > 2:
		replace_string = replace_string + '1'
	else:
		replace_string = replace_string + '0'
	replace_string = replace_string + ';\n'
	file_out.write(replace_string)
	# 不改变不涉及重新赋值的语句
	for line in all_lines[58:]:
		file_out.write(line)

if __name__ == '__main__':
	# 删除原来的文件
	common.clean()
	# 拷贝了一个修复文件
	subprocess.Popen('cp %s %s' %(c_file_name, repair_file_name), shell = True).wait()
	testcase_file = open('testcase.txt')
	# 读入测试用例
	testcases = testcase_file.readlines()
	testcase_file.close()
	# 错误路径
	bad_route = []
	# 变量列表
	var_list = []
	# 记录有用的测试样例 
	useful = []
	# 对每个数据做处理
	for testcase in testcases:
		# EOF
		if testcase.strip() == '':
			break
		
		para = testcase.split()
		# 打印数据样例序号
		num = para[0][:-1]
		print num
		
		# 新文件命名
		new_c_file_name = '%s.%s' %(num, c_file_name)
		
		# 对于每一条测试数据，对应一个c文件
		# 因此要把原c文件的原数据修改为输入数据来生成测试c文件程序
		replace(repair_file_name, new_c_file_name, para[1:])
		
		# 这里是生成测试c文件程序对应的布尔程序
		# 因为原c文件里的变量被重新赋值，因此相应的布尔变量的值也应该改变
		replace_satabs('satabs.1.bp', para[1:])
		# 创建临时文件
		tempf = tempfile.TemporaryFile()
		i = 1
		# 找到最后一个布尔程序文件
		while os.access('satabs.%d.bp' %(i), os.F_OK):
			i += 1
		i -= 1
		# 做预处理
		subprocess.Popen(common_path + 'reorder.py satabs.%d.bp' %(i), stdout = tempf, shell = True).wait()
		# 复制这个测试样例的预处理文件
		subprocess.Popen('cp reorder.bp %s.reorder.bp' %(num), shell = True).wait()
		
		# 找到包含关键字的布尔变量
		key_bp_var = common.cal_key_var(key_var)
		
		# 剔除那些包含关键字却不重要的布尔变量
		#for i in range(len(key_bp_var)-1, -1, -1):
			#if key_bp_var[i][1].find('i') == -1:
				#key_bp_var.pop(i)
		
		# 输出重要的布尔变量
		key_var_file = open('key_var.txt', 'w')
		for item in key_bp_var:
			key_var_file.write('%s\n' %(item[0]))
		key_var_file.close()
		tempf.close()
		tempf = tempfile.TemporaryFile()
		
		# 对预处理后的布尔程序进行寻找错误路径
		subprocess.Popen(common_path + 'find_bad_route %s %s.reorder.bp %d' %(new_c_file_name, num, repair_line), stdout = tempf, shell = True).wait()
		tempf.seek(0)
		content = tempf.readlines()
		tempf.close()
		bad_route, var_list,return_num = common.add_bad_route(bad_route, var_list, content, key_bp_var,num)
		if return_num == None:
			useful.append(int(num))		
		common.clean()
		subprocess.Popen('rm key_var.txt -f', shell = True).wait()
		subprocess.Popen('rm %s -f' % (new_c_file_name), shell = True).wait()
		subprocess.Popen('rm %s.reorder.bp -f' % (num), shell = True).wait()
	print bad_route, var_list
	bad_route_file = tempfile.TemporaryFile()
	n = len(var_list)
	for route in bad_route:
		for line in route:
			for i in range(n):
				bad_route_file.write('%d ' %(line[0][i]))
			bad_route_file.write('%d\n' %(line[1]))
		bad_route_file.write('---------------\n')
	bad_route_file.seek(0)
	tempf = tempfile.TemporaryFile()
	# 收集错误路径
	subprocess.Popen(common_path + 'collect_bad_route %d' %(n), stdin = bad_route_file, stdout = tempf, shell = True).wait()
	bad_route_file.close()
	tempf.seek(0)
	var_file = 'var.txt'
	varf = open(var_file, 'w')
	for i in range(n):
		varf.write('b%d: %s\n' %(i, var_list[i]))
	varf.close()
	print 'useful testcase:', useful
	# 映射到C程序
	subprocess.Popen(common_path + 'map_to_c %s %s %s %d' %(c_file_name, repair_file_name, var_file, repair_line), stdin = tempf, shell = True).wait()
