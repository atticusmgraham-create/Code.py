for i in range(0,1):    
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
    c=vect(2,2,56,2,2)
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
    probA=entanglement_entropy(ev(rho_A))
    #print("purity A:", purity)
    puritya = np.trace(rho_B @ rho_B)
    probB=entanglement_entropy(ev(rho_B))
    #print("purity B:", puritya)
    purityofAB=np.trace(rho_A @ rho_B)
    #print("purity of AB:")
    #print(purityofAB)
    probAB=entanglement_entropy(ev(np.kron(rho_A,rho_B)))
    purityofBA=np.trace(rho_B @ rho_A)
    #print("purity of BA:")
    #print(purityofBA)
    SLa=max(0.0,1.0-purity)
    SLb=max(0.0,1.0-puritya)
    SLba=max(0.0,1.0-purityofBA)
    SLab=max(0.0,1.0-purityofAB)
    probBA=entanglement_entropy(ev(np.kron(rho_B,rho_A)))
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
    entangledBits=np.array([entangledBitsA,entangledBitsB,entangledBitsab,entangledBitsba])
    entangledBitsAandB=np.array([entangledBitsA,entangledBitsB])
    entangledBitsABandBA=np.array([entangledBitsab,entangledBitsba])
    entangledBitsABandA=np.array([entangledBitsab,entangledBitsA])
    entangledBitsBAandB=np.array([entangledBitsba,entangledBitsB])
    entangledBitsABandB=np.array([entangledBitsab,entangledBitsB])
    entangledBitsBAandA=np.array([entangledBitsba,entangledBitsA])
    
    my_experiments = {
        "ALL systems": entangledBits,
        "System A and B": entangledBitsAandB,
        "System A and AB": entangledBitsABandA,
        "System A and BA": entangledBitsBAandA,
        "System B and BA": entangledBitsBAandB,
        "System B and AB": entangledBitsABandB,
        "System AB and BA": entangledBitsABandBA
        
    
    }
    def compare_system_entanglement_pure_numpy(systems_dict):
        """
        Compares and ranks the entanglement of multiple quantum systems without Qiskit.
        
        Parameters:
        systems_dict (dict): A dictionary where keys are system names (str) 
                            and values are 1D NumPy arrays (statevectors).
        """
        def _get_entanglement_score(statevector):
            # Ensure it is a flat NumPy array
            vec = np.asarray(statevector, dtype=complex)
            
            # Calculate number of qubits from the statevector size (2^n = size)
            num_qubits = int(np.log2(len(vec)))
            
            # 1. Handle 2-qubit systems manually (Concurrence)
            if num_qubits == 2:
                # For a pure state [a, b, c, d], Concurrence = 2 * |ad - bc|
                a, b, c, d = vec
                score = 2.0 * np.abs(a * d - b * c)
                return float(score), num_qubits
            
            # 2. Handle 3+ qubit systems (Partial trace of Qubit 0 + von Neumann Entropy)
            else:
                # Construct a 2x2 reduced density matrix for Qubit 0
                # Qiskit convention tracks Qubit 0 at the least significant bit (LSB)
                rho_0 = np.zeros((2, 2), dtype=complex)
                half_size = len(vec) // 2
                
                for other_qubits_state in range(half_size):
                    # Map binary indices where Qubit 0 is 0 or 1
                    idx_0 = (other_qubits_state << 1) | 0
                    idx_1 = (other_qubits_state << 1) | 1
                    
                    v0 = vec[idx_0]
                    v1 = vec[idx_1]
                    
                    rho_0[0, 0] += v0 * np.conj(v0)
                    rho_0[0, 1] += v0 * np.conj(v1)
                    rho_0[1, 0] += v1 * np.conj(v0)
                    rho_0[1, 1] += v1 * np.conj(v1)
                
                # Calculate eigenvalues of the reduced density matrix
                eigenvalues = np.linalg.eigvalsh(rho_0)
                
                # Clean floating-point noise and filter out zeros to prevent log2(0) errors
                eigenvalues = eigenvalues[eigenvalues > 1e-12]
                
                # Calculate von Neumann Entropy: -Sum(p * log2(p))
                # Since max entropy for 1 qubit is 1.0, this value is natively normalized
                score = -np.sum(eigenvalues * np.log2(eigenvalues))
                return float(score), num_qubits
    
        # Process all systems and calculate scores
        results = {}
        for name, statevector in systems_dict.items():
            score, qubits = _get_entanglement_score(statevector)
            results[name] = {"score": score, "qubits": qubits}
        
        # Sort systems by score in descending order
        ranked_systems = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)
        
        # Print formatted results
        print("=" * 46)
        print(f"{'RANK':<5} | {'SYSTEM NAME':<15} | {'QUBITS':<6} | {'SCORE':<7} | {'STATUS'}")
        print("=" * 46)
        
        for rank, (name, data) in enumerate(ranked_systems, 1):
            score = data["score"]
            qubits = data["qubits"]
            
            if score > 0.99:
                status = "Maximally Entangled"
            elif score > 0.4:
                status = "Partially Entangled"
            elif score > 0.01:
                status = "Weakly Entangled"
            else:
                status = "Separable (None)"
                
            print(f"{rank:<5} | {name:<15} | {qubits:<6} | {score:.4f} | {status}")
        print("=" * 46)
        
        return ranked_systems
    
    results = compare_system_entanglement_pure_numpy(my_experiments)
