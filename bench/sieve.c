#include <stdio.h>
#include <stdlib.h>
int main(int c,char**v){int n=atoi(v[1]);char*s=calloc(n+1,1);int cnt=0;
for(int i=2;i<=n;i++){if(!s[i]){cnt++;for(long j=(long)i*i;j<=n;j+=i)s[j]=1;}}printf("%d\n",cnt);}
