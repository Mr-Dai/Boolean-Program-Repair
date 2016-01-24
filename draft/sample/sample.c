static int x;

void main() {
	x = 3;
	f();
	assert(x == 0);
}

void f() {
	x = x - 1;
	if (x > 1) {
		f();
	}
}