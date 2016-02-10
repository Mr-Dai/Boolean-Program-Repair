# Program Repair Based on SMT

A (still on writing) paper describing how to repair a faulty C program automatically by converting it to its boolean program equivalence.

## TODO List

- [x] Revise Chapter 1
- [x] Revise Chapter 2
- [x] Revise Chapter 3
- [x] Revise Chapter 4
- [x] Revise Chapter 5
- [x] Revise Chapter 6
- [x] Write Appendix A

## How to contribute

The main document file is `0.bpr.tex`, chapter files include `abstract.tex`, `chapter1.tex`, `chapter2.tex`, `chapter3.tex`, `chapter4.tex`, `chapter5.tex`, `appendixA.tex`(not created yet).

Automatic compiling and cleaning scripts are included in the project. Before using it, make sure you have installed `xelatex` and `bibtex` and included them in your execution environment.

You can build the paper by runing

```
compile
```

and the result paper file should be `0.bpr.pdf`.

Addtionally, you can clean up all those intermediate files by running

```
clean
```

Make sure to clean those files before you commit.

If you are working on Windows, you can easily run these scripts by double-clicking the corresponding `bat` files.

`sh` version has been included for Linux and Mac users, but it is not fully tested. Use them with caution.

