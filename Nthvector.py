def vect(o,p,i,x):
 import math
 angle=[p,i,x]
 ans=[1,1,1]
 for i in range(1,len(angle)):
  ans[i]=ans[i]*math.sin(angle[i])
 for i in range(0,len(angle)-1):
  ans[i]=ans[i]*math.cos(angle[i])
 for i in range(0,len(angle)):
    ans[i]=ans[i]*o
 print(ans)
 return ans
