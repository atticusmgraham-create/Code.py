import math
import time
ball=0.09
velocitytime=[]
K=[]
Dis=[]
H=[]
r=0.00001
def u(x,m):
    import math
    return x**2*m*0.5
def f(B):
    import math
    return (B**2)/(2*9.81)
for i in range(-100,100):
      func=abs(-i*math.sin(i/r)**3)
      start_time = time.perf_counter()

      end_time = time.perf_counter()
      T=end_time-start_time
      velocitytime.append([func,T])
      K.append([u(ball,func),T])
      Dis.append([func*T,T])
      H.append([f(func),T])
print(H)
print(K)
print(Dis)
print(velocitytime)
