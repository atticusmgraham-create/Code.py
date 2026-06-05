import math
r=2
angle=[4.0,56.0,7.0]
ans=[1,1,1]
for i in range(0,len(angle)-1):
  ans[i+1]=ans[i+1]*math.sin(angle[i])
for i in range(0,len(angle)):
  ans[i]=ans[i]*math.cos(angle[i])
print(ans)
  
