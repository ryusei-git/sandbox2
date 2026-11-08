#include <stdio.h>
#include <stdlib.h>
long fib(int n){return n<2?n:fib(n-1)+fib(n-2);}
int main(int c,char**v){int n=atoi(v[1]);printf("%ld\n",fib(n));}
