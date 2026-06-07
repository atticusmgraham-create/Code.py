import math
import numpy as np
from numpy.linalg import matrix_rank
def conditions(x,y,z,w):
 if(x==y==z==w):
  return "all entangled"
 if(x==y==w):
  return "a and b and ba are entangled"
 if(x==y==z):
  return "a and b and ab are entangled"
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
c=vect(2,2,2,2,6)
g=vect(2,2,2,2,6)

norma = math.sqrt(sum(x*x for x in c))
psi_n= [x / norma for x in c]
#print(psi_n)
normb = math.sqrt(sum(xa*xa for xa in g))
psi_nd= [xa / normb for xa in g]
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

P, K = np.linalg.qr(basisb.T)  # QR decomposition

basisu = P[:, :np.linalg.matrix_rank(basisb)]
print("m2:")
print(basisu)
c = np.linalg.inv(basis) @ psia
cd = np.linalg.inv(basisu) @ psid
print("coordinates for A:")
print(c)
print("coordinates for B:")
print(cd)
psic=c/np.linalg.norm(c)
rhop=np.outer(psic,psic)
print("density matrix a:")
rhorp=rhop.reshape(2,2,2,2)
print(rhorp)
psiec=cd/np.linalg.norm(cd)
rhodp=np.outer(psiec,psiec)
print("density matrix b:")
rhordp=rhodp.reshape(2,2,2,2)
print(rhordp)
#gs=projection(psia, 2) # amplitude of |2>
#tb=(projection(psid, 2))  
#a = np.array([1, 2, 3])   # system A (n=3)
#b = np.array([4, 5, 6])
rho_A = np.zeros((2, 2))

for i in range(2):

    for j in range(2):

        rho_A[i, j] = sum(rhorp[i, k, j, k] for k in range(2))
print("subsystem A: ")
print(rho_A)
rho_B = np.zeros((2, 2))

for i in range(2):

    for j in range(2):

        rho_B[i, j] = sum(rhordp[i, k, j, k] for k in range(2))
print("subsystem B: ")
print(rho_B)
purity = np.trace(rho_A @ rho_A)

print("purity A:", purity)
puritya = np.trace(rho_B @ rho_B)

print("purity B:", puritya)
purityofAB=np.trace(rho_A @ rho_B)
print("purity of AB:")
print(purityofAB)
purityofBA=np.trace(rho_B @ rho_A)
print("purity of BA:")
print(purityofBA)

