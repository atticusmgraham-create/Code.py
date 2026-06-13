import math
ball=0.09
H=[]
K=[]
r=0.00001
def u(x,m):
    import math
    return x**2*m*0.5
for i in range(-10,10):
      func=abs(-i*math.sin(i/r)**3)
      H.append(func)
      K.append(u(ball,func))
print(H)
print(K)
