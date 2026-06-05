import math
import numpy as np
from numpy.linalg import matrix_rank
def vect(o,p,i,a,x):
 import math
 angle=[p,i,x,a]
 ans=[1,1,1,1]
 for i in range(1,len(angle)):
  ans[i]=ans[i]*math.sin(angle[i])
 for i in range(0,len(angle)-1):
  ans[i]=ans[i]*math.cos(angle[i])
 for i in range(0,len(angle)):
    ans[i]=ans[i]*o
 print("measurements",ans)
 return ans
c=vect(2,5,3,8,6)
g=vect(2,3,7,9,1)

norma = math.sqrt(sum(x*x for x in c))
psi_n= [x / norma for x in c]
#print(psi_n)
normb = math.sqrt(sum(x*x for x in g))
psi_nd= [x / normb for x in g]
#print(psi_nd)
psid = np.array(psi_n, dtype=float)
psia= np.array(psi_nd, dtype=float)
psia = psia / np.linalg.norm(psia)
psid =psid/np.linalg.norm(psid)
print("state vector A: ",psia)
print("state vector B: ",psid)
def projection(psi, i):
    return psi[i]
basisa=np.eye(len(psia))
basisb=np.eye(len(psid))
#print(basisb)
#print(basisa)


rank = matrix_rank(basisa)

#print("Dimension of basis:", rank)
Q, R = np.linalg.qr(basisa.T)  # QR decomposition

basis = Q[:, :np.linalg.matrix_rank(basisa)]
print("m1:")
print(basis)
rankd = matrix_rank(basisb)

#print("Dimension of basis:", rank)
Q, R = np.linalg.qr(basisb.T)  # QR decomposition

basisu = Q[:, :np.linalg.matrix_rank(basisb)]
print("m2:")
print(basisu)

#gs=projection(psia, 2) # amplitude of |2>
#tb=(projection(psid, 2))  
#a = np.array([1, 2, 3])   # system A (n=3)
#b = np.array([4, 5, 6])   # system B (n=3)
#psi = np.kron(a, b)  # n^2-dimensional state
#n = 3
#psi_matrix = psi.reshape
