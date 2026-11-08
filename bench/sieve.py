import sys
n=int(sys.argv[1]); s=bytearray(n+1); cnt=0
for i in range(2,n+1):
    if not s[i]:
        cnt+=1
        for j in range(i*i,n+1,i): s[j]=1
print(cnt)
