import math
import numpy as np
from numpy.linalg import matrix_rank


def entanglement_entropy(eigenvalues):

    return -sum(

        lam * math.log2(lam)

        for lam in eigenvalues

        if lam > 0

    )
def ev(x):
 import numpy as np
 return np.linalg.eigvals(x)
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
c=vect(2,2,2,2,2)
g=vect(2,2,2,2,2)

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
D=2
#print("Dimension of basis:", rank)

P, K = np.linalg.qr(basisb.T)  # QR decomposition

basisu = P[:, :np.linalg.matrix_rank(basisb)]
print("m2:")
print(basisu)
print("m3:")
print(basisu@basis)
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
probA=entanglement_entropy(ev(rho_A@rho_A))
#print("purity A:", purity)
puritya = np.trace(rho_B @ rho_B)
probB=entanglement_entropy(ev(rho_B@rho_B))
#print("purity B:", puritya)
purityofAB=np.trace(rho_A @ rho_B)
#print("purity of AB:")
#print(purityofAB)
probAB=entanglement_entropy(ev(rho_A@rho_B))
purityofBA=np.trace(rho_B @ rho_A)
#print("purity of BA:")
#print(purityofBA)
SLa=max(0.0,1.0-purity)
SLb=max(0.0,1.0-puritya)
SLba=max(0.0,1.0-purityofBA)
SLab=max(0.0,1.0-purityofAB)
probBA=entanglement_entropy(ev(rho_B@rho_A))
print("entanglement B: ",probB)
print("entanglement BA: ",probBA)
entangledB=-(probB*math.log(probB,2)+probBA*math.log(probBA,2))
print("entangelement BA and B equals:", entangledB)

print("dimensions for system B:",D)
entangledBitsB=(D/(D-1))*SLb

print("entangled Bits for B and BA: ",entangledBitsB)
print("entanglement A: ",probA)
print("entanglement AB: ",probAB)

entangledA=-(probA*math.log(probA,2)+probAB*math.log(probAB,2))
print("entangelement BA and B equals:", entangledA)

print("dimensions for system A:",D)
entangledBitsA=(D/(D-1))*SLa
print("entangled Bits for A and AB: ",entangledBitsA)
print("entanglement A: ",probA)
print("entanglement B: ",probB)
entangledBA=-(probA*math.log(probA,2)+probB*math.log(probB,2))
print("entangelement A and B equals:", entangledBA)

print("dimensions for system A and system B:",D)
entangledBitsba=(D/(D-1))*SLba
print("entangled Bits for A and B: ",entangledBitsba)
print("entanglement AB: ",probAB)
print("entanglement BA: ",probBA)
entangledAB=-(probAB*math.log(probAB,2)+probBA*math.log(probBA,2))
print("entangelement AB and BA equals:", entangledAB)
print("dimensions for system AB and system BA:",D)
entangledBitsab=(D/(D-1))*SLab
print("entangled Bits for AB and BA: ",entangledBitsab)
