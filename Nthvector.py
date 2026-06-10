import string
import math
def x(val,h,k,lds,od,p,i,e,r,pl,ui,kol):   
    def Qs(h,k,lds,od,p,i,e,r,pl,ui):  
        
        import numpy as np
        #from numpy.linalg import matrix_rank
        
        def findState(v):
            
            b=(1-math.sqrt((1-math.pow(v,2))))
            return math.sqrt(b/2)
        def findStates(v):
            
            b=(1+math.sqrt((1-math.pow(v,2))))
            return math.sqrt(b/2)
    
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
         #print("measurements",ans)
         return ans
        c=vect(pl,h,k,lds,od)
        g=vect(ui,p,i,e,r)
        
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
        #print("state vector A: ",psia)
        #print("state vector B: ",psid)
        def projection(psi, i):
            return psi[i]
        basisa=np.eye(len(psia))
        basisb=np.eye(len(psid))
        #print(basisb)
        #print(basisa)
        
        
        #rank = matrix_rank(basisa)
        
        #print("Dimension of basis:", rank)
        
        
        Q, R = np.linalg.qr(basisa.T)  # QR decomposition
        
        basis = Q[:, :np.linalg.matrix_rank(basisa)]

        D=2
   
        
        P, K = np.linalg.qr(basisb.T)  # QR decomposition
        
        basisu = P[:, :np.linalg.matrix_rank(basisb)]

        c = np.linalg.inv(basis) @ psia
        cd = np.linalg.inv(basisu) @ psid

        psic=c/np.linalg.norm(c)
        rhop=np.outer(psic,psic)
       
        rhorp=rhop.reshape(2,2,2,2)
        
        psiec=cd/np.linalg.norm(cd)
        rhodp=np.outer(psiec,psiec)
       
        rhordp=rhodp.reshape(2,2,2,2)

        rho_A = np.zeros((2, 2))
        
        for i in range(2):
        
            for j in range(2):
        
                rho_A[i, j] = sum(rhorp[i, k, j, k] for k in range(2))
        #print("subsystem A: ")
        #print(rho_A)
        rho_B = np.zeros((2, 2))
        
        for i in range(2):
        
            for j in range(2):
        
                rho_B[i, j] = sum(rhordp[i, k, j, k] for k in range(2))
        #print("subsystem B: ")
        #print(rho_B)
        purity = np.trace(rho_A @ rho_A)
        probA=entanglement_entropy(ev(rho_A))
        #print("purity A:", purity)
        puritya = np.trace(rho_B)
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
        #print("entanglement B: ",probB)
        #print("entanglement BA: ",probBA)
        entangledB=-(probB*math.log(probB,2)+probBA*math.log(probBA,2))
        #print("entangelement BA and B equals:", entangledB)
        
        #print("dimensions for system B:",D)
        entangledBitsB=(D/(D-1))*SLb
        
        #print("entangled Bits for B and BA: ",entangledBitsB)
        #print("entanglement A: ",probA)
        #print("entanglement AB: ",probAB)
        
        entangledA=-(probA*math.log(probA,2)+probAB*math.log(probAB,2))
        #print("entangelement BA and B equals:", entangledA)
        
        #print("dimensions for system A:",D)
        entangledBitsA=(D/(D-1))*SLa
        #print("entangled Bits for A and AB: ",entangledBitsA)
        #print("entanglement A: ",probA)
        #print("entanglement B: ",probB)
        entangledBA=-(probA*math.log(probA,2)+probB*math.log(probB,2))
        #print("entangelement A and B equals:", entangledBA)
        
        #print("dimensions for system A and system B:",D)
        entangledBitsba=(D/(D-1))*SLba
        #print("entangled Bits for A and B: ",entangledBitsba)
        #print("entanglement AB: ",probAB)
        #print("entanglement BA: ",probBA)
        entangledAB=-(probAB*math.log(probAB,2)+probBA*math.log(probBA,2))
        #print("entangelement AB and BA equals:", entangledAB)
        #print("dimensions for system AB and system BA:",D)
        entangledBitsab=(D/(D-1))*SLab
        #print("entangled Bits for AB and BA: ",entangledBitsab)
        
        C_system_B = math.sqrt(max(0.0, entangledBitsB))
       
        C_system_A = math.sqrt(max(0.0, entangledBitsA))
        AllQbits=[findState(C_system_A),findStates(C_system_A),findState(C_system_B),findStates(C_system_B)]
        #entangledBits=np.array([entangledBitsA,entangledBitsB,entangledBitsab,entangledBitsba])
        #entangledBitsAandB=np.array([entangledBitsA,entangledBitsB])
        #entangledBitsABandBA=np.array([entangledBitsab,entangledBitsba])
        #entangledBitsABandA=np.array([entangledBitsab,entangledBitsA])
        #entangledBitsBAandB=np.array([entangledBitsba,entangledBitsB])
        
        #entangledBitsABandB=np.array([entangledBitsab,entangledBitsB])
        #entangledBitsBAandA=np.array([entangledBitsba,entangledBitsA])
        
        #my_experiments = {
        #    "ALL systems": entangledBits,
        #    "System A and B": entangledBitsAandB,
        #    "System A and AB": entangledBitsABandA,
        #    "System A and BA": entangledBitsBAandA,
        #    "System B and BA": entangledBitsBAandB,
        #    "System B and AB": entangledBitsABandB,
        #    "System AB and BA": entangledBitsABandBA
            
        
        #}
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
            #print("=" * 46)
            #print(f"{'RANK':<5} | {'SYSTEM NAME':<15} | {'QUBITS':<6} | {'SCORE':<7} | {'STATUS'}")
            #print("=" * 46)
            
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
                    
                #print(f"{rank:<5} | {name:<15} | {qubits:<6} | {score:.4f} | {status}")
            #print("=" * 46)
            
            return ranked_systems
    
        #results = compare_system_entanglement_pure_numpy(my_experiments)
        return AllQbits
    import numpy as np
    Xlist=[]
    Ylist=[]
    kk=40
    for i in range(0,kk):
        import math
        LO=Qs(i,i+5,(i**2),(i**3)+1,(i**2)+1,0,(i**4),i-2,1,1)
        #print("The system is: ",sum(LO),"qubits")
        #print(LO)
        Xlist.append(LO[0])
        Xlist.append(LO[1])
        Ylist.append(LO[2])
        Ylist.append(LO[3])
    M1=np.array([Xlist])
    M2=np.array([Ylist]).reshape(len(M1[0]),1)
    Matrixofstates=(M2@M1)*(M1@M2)
    eigenvalues, eigenvectors = np.linalg.eig(Matrixofstates)
    
    descending_indices = np.argsort(np.abs(eigenvalues))[::-1]
    #sorted_values = eigenvalues[descending_indices]
    sorted_vectors = eigenvectors[:, descending_indices]
    
    #best_eigenvalues = sorted_values[:kol]
    best_eigenvectors = sorted_vectors[:, :kol]
    matr=best_eigenvectors.T@Matrixofstates@best_eigenvectors
    #print("new matrix:", matr)
    state=[]
    idl=0
    for i in range(0,len(matr)):
        for io in range(0,len(matr)):
            state.append("")
            if(matr[i][io].real>0):
                #print("^",end=" ")
                state[idl]="^"+state[idl]
            elif(matr[i][io].real<0):
                #print("v",end=" ")
                state[idl]="v"+state[idl]
            else:
                #print("O",end=" ")
                state[idl]="O"+state[idl]
            if(matr[i][io].imag>0):
                #print("^",end=" ")
                state[idl]="^"+state[idl]
            elif(matr[i][io].imag<0):
                #print("v",end=" ")
                state[idl]="v"+state[idl]
            else:
                #print("O",end=" ")
                state[idl]="O"+state[idl]
            idl+=1
        
        #print()
    for i in range(0,len(state)):
        if(state[i]=='O^'):
            state[i]='<<'
        elif(state[i]=='Ov'):
            state[i]='>>'
        elif(state[i]=='OO'):
            state[i]='<>'
    for i in range(0,len(state)):
        if(state[i]=='<>' or state[i]=='^v' or state[i]=='v^'):
            state[i]=0
        else:
            state[i]=1*(10**(len(state)-i-1))
    
    state=str(sum(state))
    state=int(state,2)
    return state,val
a=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ab=[]
for i in range(0,26): 

    e=x(a[i],4,6,6,6,6,6,6,0,6,0,i)
    #print(e[0])
    ab.append(e[0])
def human(x,y,lde,o,p):
    return y[lde]-y[o]-y[p],x[lde]+x[o]+x[p]


dictionary_array = [
    "aah", "aal", "aas", "aba", "abb", "abs", "aby", "ace", "act", "add", 
  "ado", "ads", "adz", "aff", "aft", "aga", "age", "ago", "aha", "ahi", 
  "ahs", "aid", "ail", "aim", "ain", "air", "ais", "ait", "aji", "aka", 
  "ala", "alb", "ale", "all", "alp", "alt", "alu", "ama", "ami", "amp", 
  "amu", "ana", "and", "ane", "ani", "ant", "any", "ape", "apo", "app", 
  "apt", "arb", "arc", "ard", "are", "arf", "ark", "arm", "ars", "art", 
  "ary", "ash", "ask", "asp", "ass", "ate", "auk", "ava", "ave", "avo", 
  "awa", "awe", "awl", "awn", "axe", "aye",
   "baa", "bac", "bad", "bae", "bag", "bah", "bal", "bam", "ban", "bao", 
  "bap", "bar", "bas", "bat", "baw", "bay", "bed", "bee", "beg", "bel", 
  "ben", "bes", "bet", "bey", "bez", "bib", "bid", "big", "bin", "bio", 
  "bis", "bit", "biz", "boa", "bob", "bod", "bog", "boh", "boi", "bok", 
  "bon", "boo", "bop", "bor", "bos", "bot", "bow", "box", "boy", "bra", 
  "bro", "brr", "bru", "bub", "bud", "bug", "bum", "bun", "bur", "bus", 
  "but", "buy", "bye", "bys",
   "caa", "cab", "cad", "caf", "cag", "cal", "cam", "can", "cap", "car", 
  "cat", "caw", "cay", "caz", "cee", "cel", "cep", "cha", "che", "chi", 
  "cid", "cig", "cis", "cit", "cly", "cob", "cod", "cog", "col", "con", 
  "coo", "cop", "coq", "cor", "cos", "cot", "cow", "cox", "coy", "coz", 
  "cru", "cry", "cub", "cud", "cue", "cum", "cup", "cur", "cut", "cuz", 
  "cwm","dab", "dad", "dae", "dag", "dah", "dak", "dal", "dam", "dan", "dap", 
  "dar", "das", "daw", "day", "dbx", "deb", "dee", "def", "deg", "dei", 
  "del", "den", "dep", "des", "dev", "dew", "dex", "dey", "dib", "did", 
  "die", "dif", "dig", "dil", "dim", "din", "dip", "dis", "dit", "div", 
  "dkg", "dkl", "dkm", "dlr", "dms", "dob", "doc", "dod", "doe", "dof", 
  "dog", "doh", "dol", "dom", "don", "doo", "dop", "dor", "dos", "dot", 
  "dow", "dox", "doy", "dpi", "dpt", "dry", "dso", "dsp", "dub", "duc", 
  "dud", "due", "dug", "duh", "dui", "dum", "dun", "duo", "dup", "dur", 
  "dux", "dwt", "dwy", "dye", "dyn", "dzo",  "ean", "ear", "eas", "eat", "eau", "ebb", "ech", "eco", "ecu", "edh", 
  "eds", "eek", "eel", "een", "eew", "eff", "efs", "eft", "egg", "ego", 
  "ehs", "eik", "eke", "eld", "elf", "elk", "ell", "elm", "els", "elt", 
  "eme", "emo", "ems", "emu", "end", "ene", "eng", "ens", "eon", "era", 
  "ere", "erf", "erg", "erk", "erm", "ern", "err", "ers", "ess", "est", 
  "eta", "eth", "euk", "eve", "evo", "ewe", "ewk", "ewt", "exo", "exp", 
  "ext", "eye",  "faa", "fab", "fad", "fae", "fag", "fah", "fam", "fan", "fap", "far", 
  "fas", "fat", "fav", "faw", "fax", "fay", "fed", "fee", "feg", "feh", 
  "fem", "fen", "fer", "fes", "fet", "feu", "few", "fey", "fez", "fib", 
  "fid", "fie", "fig", "fil", "fin", "fir", "fit", "fix", "fiz", "flo", 
  "flu", "fly", "fob", "foe", "fog", "foh", "fon", "foo", "fop", "for", 
  "fou", "fox", "foy", "fra", "fro", "fry", "fub", "fud", "fug", "fum", 
  "fun", "fur","gab", "gad", "gae", "gag", "gah", "gak", "gal", "gam", "gan", "gap", 
  "gar", "gas", "gat", "gaw", "gay", "gds", "ged", "gee", "gel", "gem", 
  "gen", "geo", "get", "gey", "ghi", "gib", "gid", "gie", "gig", "gin", 
  "gio", "gip", "gis", "git", "gju", "glb", "gld", "gnu", "goa", "gob", 
  "god", "goe", "goi", "gon", "goo", "gor", "gos", "got", "gov", "gox", 
  "goy", "gpd", "gph", "gpm", "gps", "grr", "gsm", "gtd", "gub", "gue", 
  "gul", "gum", "gun", "gup", "gur", "gus", "gut", "guv", "guy", "gym", 
  "gyp",  "had", "hae", "hag", "hah", "haj", "ham", "han", "hao", "hap", "has", 
  "hat", "haw", "hay", "heh", "hem", "hen", "hep", "her", "hes", "het", 
  "hew", "hex", "hey", "hic", "hid", "hie", "him", "hin", "hip", "his", 
  "hit", "hmm", "hoa", "hob", "hoc", "hod", "hoe", "hog", "hoh", "hoi", 
  "hom", "hon", "hoo", "hop", "hos", "hot", "how", "hox", "hoy", "hub", 
  "hue", "hug", "huh", "hui", "hum", "hun", "hup", "hut", "hye", "hyp", "ibn", "ice", "ich", "ick", "icy", "ide", "ids", "iff", "ifs", "igg", 
  "ihp", "iid", "ilk", "ill", "imp", "imu", "inf", "ing", "ink", "inn", 
  "ins", "int", "ion", "ios", "ipm", "ipr", "ips", "ire", "irk", "ish", 
  "ism", "iso", "ist", "ita", "itd", "itr", "its", "iva", "ivy", "iwa", "iwi",  "jab", "jac", "jag", "jai", "jak", "jam", "jap", "jar", "jaw", "jay", 
  "jee", "jen", "jer", "jet", "jeu", "jib", "jig", "jin", "jiz", "job", 
  "joe", "jog", "jol", "jor", "jot", "jow", "joy", "jud", "jue", "jug", 
  "jun", "jus", "jut",  "kab", "kae", "kaf", "kai", "kak", "kam", "kas", "kat", "kaw", "kay", 
  "kea", "keb", "ked", "kef", "keg", "ken", "kep", "kes", "ket", "kex", 
  "key", "khi", "kia", "kid", "kif", "kin", "kip", "kir", "kis", "kit", 
  "koa", "kob", "koi", "kon", "kop", "kor", "kos", "kow", "kue", "kye", 
  "kyu",  "lab", "lac", "lad", "lag", "lah", "lam", "lap", "lar", "las", "lat", 
  "lav", "law", "lax", "lay", "lea", "led", "lee", "leg", "lei", "lek", 
  "let", "leu", "lev", "lex", "ley", "lez", "lib", "lid", "lie", "lig", 
  "lin", "lip", "lis", "lit", "loa", "lob", "lod", "log", "loo", "lop", 
  "lor", "los", "lot", "lou", "low", "lox", "loy", "lud", "lug", "lum", 
  "lun", "lur", "luv", "lux", "luz", "lye", "lym",  "maa", "mab", "mac", "mad", "mae", "mag", "mai", "mak", "mal", "mam", 
  "man", "map", "mar", "mas", "mat", "maw", "max", "may", "med", "mee", 
  "meg", "meh", "mel", "mem", "men", "mer", "mes", "met", "meu", "mew", 
  "mho", "mib", "mic", "mid", "mig", "mil", "mim", "min", "mir", "mis", 
  "mix", "miz", "mmm", "mna", "moa", "mob", "moc", "mod", "moe", "mog", 
  "moi", "mol", "mom", "mon", "moo", "mop", "mor", "mos", "mot", "mou", 
  "mow", "moy", "moz", "mud", "mug", "mum", "mun", "mus", "mut", "mux", 
  "mwa", "myc",  "nab", "nad", "nae", "nag", "nah", "nam", "nan", "nao", "nap", "nas", 
  "nat", "nav", "naw", "nay", "nde", "neb", "ned", "nee", "nef", "neg", 
  "nek", "nep", "net", "new", "nib", "nid", "nie", "nil", "nim", "nip", 
  "nis", "nit", "nix", "noa", "nob", "nod", "nog", "noh", "nom", "non", 
  "noo", "nor", "nos", "not", "now", "nox", "noy", "nth", "nub", "nug", 
  "nun", "nur", "nus", "nut", "nux", "nye", "nym", "nys",  "oad", "oaf", "oak", "oar", "oat", "oba", "obe", "obi", "obo", "obs", 
  "obv", "oca", "och", "oda", "odd", "ode", "ods", "oer", "oes", "off", 
  "oft", "ohm", "oho", "ohs", "ohv", "oik", "oil", "oka", "oke", "ola", 
  "old", "ole", "olm", "oma", "oms", "one", "ono", "ons", "ony", "oof", 
  "ooh", "oom", "oos", "oot", "ope", "ops", "opt", "ora", "orb", "orc", 
  "ord", "ore", "orf", "org", "oro", "orp", "ors", "ort", "ose", "oud", 
  "oui", "our", "ous", "out", "ova", "ovo", "owe", "owl", "own", "owt", 
  "oxo", "oxy", "ozs",  "pac", "pad", "pah", "pak", "pal", "pam", "pan", "pap", "par", "pas", 
  "pat", "pav", "paw", "pax", "pay", "pea", "pec", "ped", "pee", "peg", 
  "peh", "pel", "pen", "pep", "per", "pes", "pet", "pew", "phi", "pho", 
  "pht", "pia", "pic", "pie", "pig", "pin", "pip", "pir", "pis", "pit", 
  "piu", "pix", "plu", "ply", "poa", "pod", "poh", "poi", "pol", "pom", 
  "poo", "pop", "pos", "pot", "pow", "pox", "poz", "pre", "pro", "pry", 
  "psi", "pst", "pub", "pud", "pug", "puh", "pul", "pun", "pup", "pur", 
  "pus", "put", "puy", "pwn", "pya", "pye", "pyx","qat", "qis", "qua", "que", "qui", "quo",  "rab", "rad", "rag", "rah", "rai", "raj", "ram", "ran", "rap", "ras", 
  "rat", "rav", "raw", "rax", "ray", "reb", "rec", "red", "ree", "ref", 
  "reg", "reh", "rei", "rem", "ren", "reo", "rep", "res", "ret", "rev", 
  "rew", "rex", "rez", "rho", "rhy", "ria", "rib", "rid", "rif", "rig", 
  "rim", "rin", "rip", "rit", "riz", "rob", "roc", "rod", "roe", "rok", 
  "rom", "roo", "rot", "row", "rub", "ruc", "rud", "rue", "rug", "run", 
  "rut", "rya", "rye", "ryu",  "sab", "sac", "sad", "sae", "sag", "sai", "sal", "sam", "san", "sap", 
  "sar", "sat", "sau", "sav", "saw", "sax", "say", "saz", "sea", "sec", 
  "sed", "see", "seg", "sei", "sel", "sen", "ser", "set", "sev", "sew", 
  "sex", "sey", "sez", "sha", "she", "shh", "sho", "shy", "sib", "sic", 
  "sif", "sig", "sik", "sim", "sin", "sip", "sir", "sis", "sit", "six", 
  "ska", "ski", "sky", "sly", "sma", "sny", "sob", "soc", "sod", "sog", 
  "soh", "sol", "som", "son", "sop", "sos", "sot", "sou", "sov", "sow", 
  "sox", "soy", "soz", "spa", "spy", "sri", "sty", "sub", "sud", "sue", 
  "sug", "sui", "suk", "sum", "sun", "sup", "suq", "sur", "sus", "swy", 
  "sye", "syn",  "tab", "tad", "tae", "tag", "tai", "taj", "tak", "tam", "tan", "tao", 
  "tap", "tar", "tas", "tat", "tau", "tav", "taw", "tax", "tay", "tea", 
  "tec", "ted", "tee", "tef", "teg", "tel", "ten", "tes", "tet", "tew", 
  "tex", "the", "tho", "thy", "tic", "tid", "tie", "tig", "tik", "til", 
  "tin", "tip", "tis", "tit", "tix", "tiz", "toc", "tod", "toe", "tog", 
  "tom", "ton", "too", "top", "tor", "tot", "tow", "toy", "try", "tsk", 
  "tub", "tug", "tui", "tum", "tun", "tup", "tut", "tux", "twa", "two", 
  "twp", "tye", "tyg",  "udo", "uds", "uey", "ufo", "ugh", "ugs", "uke", "ule", 
  "ulu", "ume", "umm", "ump", "ums", "umu", "uni", "uns", 
  "upo", "ups", "urb", "urd", "ure", "urn", "urp", "use", 
  "uta", "ute", "uts", "utu", "uva", "uwu",  "vac", "vae", "vag", "van", "var", "vas", "vat", "vau", "vav", "vaw", 
  "vax", "vee", "veg", "vet", "vex", "vey", "via", "vid", "vie", "vig", 
  "vim", "vin", "vip", "vir", "vis", "viz", "vly", "voe", "vog", "vol", 
  "vom", "von", "vor", "vow", "vox", "vug", "vum",  "wab", "wad", "wae", "wag", "wah", "wai", "wan", "wap", "war", "was", 
  "wat", "waw", "wax", "way", "waz", "web", "wed", "wee", "wem", "wen", 
  "wet", "wex", "wey", "wha", "who", "why", "wig", "win", "wis", "wit", 
  "wiz", "woe", "wof", "wok", "won", "woo", "wop", "wos", "wot", "wow", 
  "wox", "wry", "wud", "wus", "wuz", "wye", "wyn","xat","xed", "xes", "xis","xon","xys",  "yaa", "yad", "yae", "yag", "yah", "yak", "yam", "yap", "yar", "yas", 
  "yaw", "yay", "yea", "yed", "yeh", "yen", "yep", "yer", "yes", "yet", 
  "yew", "yex", "yey", "yez", "ygo", "yid", "yin", "yip", "yiz", "yob", 
  "yod", "yok", "yom", "yon", "you", "yow", "yrs", "yug", "yuk", "yum", 
  "yup", "yus",  "zag", "zap", "zas", "zax", "zea", "zed", "zee", "zek", 
  "zel", "zen", "zep", "zex", "zho", "zig", "zin", "zip", 
  "zit", "ziz", "zoa", "zol", "zoo", "zos", "zuz", "zzz",
    # ... (add more 3-letter words as needed)
]


# Convert standard dictionary to a high-speed hashing Set
real_words_set = set(dictionary_array)

# 2. Generate all combinations natively
letters = string.ascii_lowercase
all_combinations = [i + j + k for i in letters for j in letters for k in letters]

# 3. Match against your inline set
valid_words = [word for word in all_combinations if word in real_words_set]

#print(f"Offline execution complete! Matched {len(valid_words)} words.")
#print(valid_words)
def g(n,p,ldf):
  hil=n.index(list(p[ldf])[0]),n.index(list(p[ldf])[1]),n.index(list(p[ldf])[2])
  return hil
my_dict={}
for i in range(0,len(dictionary_array)):
    iopp=g(a,dictionary_array,i) 
    j=human(a,ab,iopp[0],iopp[1],iopp[2])
    my_dict[j[1]] = j[0]
hilo=[]
for value in my_dict.values():
    hilo.append(value)
#print(hilo)
seen = set()
duplicates = set()

for value in hilo:
    if value in seen:
        duplicates.add(value)
    else:
        seen.add(value)

#print("repeats",len(list(duplicates))) 

for i in range(0,20):
    kl=list(duplicates)
    ui=[]
    for i in range(0,len(kl)):
        ui.append(hilo.index(kl[i]))
    #print(ui)
    for i in range(0,len(ui)):
        hilo[ui[i]]=int(ui[i]*math.sin(i**3))
    #print(hilo)
    seen = set()
    duplicates = set()
    for value in hilo:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
#print("repeats",len(list(duplicates))) 
dictionary_arrays = [
    "aah", "aal", "aas", "aba", "abb", "abs", "aby", "ace", "act", "add", 
  "ado", "ads", "adz", "aff", "aft", "aga", "age", "ago", "aha", "ahi", 
  "ahs", "aid", "ail", "aim", "ain", "air", "ais", "ait", "aji", "aka", 
  "ala", "alb", "ale", "all", "alp", "alt", "alu", "ama", "ami", "amp", 
  "amu", "ana", "and", "ane", "ani", "ant", "any", "ape", "apo", "app", 
  "apt", "arb", "arc", "ard", "are", "arf", "ark", "arm", "ars", "art", 
  "ary", "ash", "ask", "asp", "ass", "ate", "auk", "ava", "ave", "avo", 
  "awa", "awe", "awl", "awn", "axe", "aye",
   "baa", "bac", "bad", "bae", "bag", "bah", "bal", "bam", "ban", "bao", 
  "bap", "bar", "bas", "bat", "baw", "bay", "bed", "bee", "beg", "bel", 
  "ben", "bes", "bet", "bey", "bez", "bib", "bid", "big", "bin", "bio", 
  "bis", "bit", "biz", "boa", "bob", "bod", "bog", "boh", "boi", "bok", 
  "bon", "boo", "bop", "bor", "bos", "bot", "bow", "box", "boy", "bra", 
  "bro", "brr", "bru", "bub", "bud", "bug", "bum", "bun", "bur", "bus", 
  "but", "buy", "bye", "bys",
   "caa", "cab", "cad", "caf", "cag", "cal", "cam", "can", "cap", "car", 
  "cat", "caw", "cay", "caz", "cee", "cel", "cep", "cha", "che", "chi", 
  "cid", "cig", "cis", "cit", "cly", "cob", "cod", "cog", "col", "con", 
  "coo", "cop", "coq", "cor", "cos", "cot", "cow", "cox", "coy", "coz", 
  "cru", "cry", "cub", "cud", "cue", "cum", "cup", "cur", "cut", "cuz", 
  "cwm","dab", "dad", "dae", "dag", "dah", "dak", "dal", "dam", "dan", "dap", 
  "dar", "das", "daw", "day", "dbx", "deb", "dee", "def", "deg", "dei", 
  "del", "den", "dep", "des", "dev", "dew", "dex", "dey", "dib", "did", 
  "die", "dif", "dig", "dil", "dim", "din", "dip", "dis", "dit", "div", 
  "dkg", "dkl", "dkm", "dlr", "dms", "dob", "doc", "dod", "doe", "dof", 
  "dog", "doh", "dol", "dom", "don", "doo", "dop", "dor", "dos", "dot", 
  "dow", "dox", "doy", "dpi", "dpt", "dry", "dso", "dsp", "dub", "duc", 
  "dud", "due", "dug", "duh", "dui", "dum", "dun", "duo", "dup", "dur", 
  "dux", "dwt", "dwy", "dye", "dyn", "dzo",  "ean", "ear", "eas", "eat", "eau", "ebb", "ech", "eco", "ecu", "edh", 
  "eds", "eek", "eel", "een", "eew", "eff", "efs", "eft", "egg", "ego", 
  "ehs", "eik", "eke", "eld", "elf", "elk", "ell", "elm", "els", "elt", 
  "eme", "emo", "ems", "emu", "end", "ene", "eng", "ens", "eon", "era", 
  "ere", "erf", "erg", "erk", "erm", "ern", "err", "ers", "ess", "est", 
  "eta", "eth", "euk", "eve", "evo", "ewe", "ewk", "ewt", "exo", "exp", 
  "ext", "eye",  "faa", "fab", "fad", "fae", "fag", "fah", "fam", "fan", "fap", "far", 
  "fas", "fat", "fav", "faw", "fax", "fay", "fed", "fee", "feg", "feh", 
  "fem", "fen", "fer", "fes", "fet", "feu", "few", "fey", "fez", "fib", 
  "fid", "fie", "fig", "fil", "fin", "fir", "fit", "fix", "fiz", "flo", 
  "flu", "fly", "fob", "foe", "fog", "foh", "fon", "foo", "fop", "for", 
  "fou", "fox", "foy", "fra", "fro", "fry", "fub", "fud", "fug", "fum", 
  "fun", "fur","gab", "gad", "gae", "gag", "gah", "gak", "gal", "gam", "gan", "gap", 
  "gar", "gas", "gat", "gaw", "gay", "gds", "ged", "gee", "gel", "gem", 
  "gen", "geo", "get", "gey", "ghi", "gib", "gid", "gie", "gig", "gin", 
  "gio", "gip", "gis", "git", "gju", "glb", "gld", "gnu", "goa", "gob", 
  "god", "goe", "goi", "gon", "goo", "gor", "gos", "got", "gov", "gox", 
  "goy", "gpd", "gph", "gpm", "gps", "grr", "gsm", "gtd", "gub", "gue", 
  "gul", "gum", "gun", "gup", "gur", "gus", "gut", "guv", "guy", "gym", 
  "gyp",  "had", "hae", "hag", "hah", "haj", "ham", "han", "hao", "hap", "has", 
  "hat", "haw", "hay", "heh", "hem", "hen", "hep", "her", "hes", "het", 
  "hew", "hex", "hey", "hic", "hid", "hie", "him", "hin", "hip", "his", 
  "hit", "hmm", "hoa", "hob", "hoc", "hod", "hoe", "hog", "hoh", "hoi", 
  "hom", "hon", "hoo", "hop", "hos", "hot", "how", "hox", "hoy", "hub", 
  "hue", "hug", "huh", "hui", "hum", "hun", "hup", "hut", "hye", "hyp", "ibn", "ice", "ich", "ick", "icy", "ide", "ids", "iff", "ifs", "igg", 
  "ihp", "iid", "ilk", "ill", "imp", "imu", "inf", "ing", "ink", "inn", 
  "ins", "int", "ion", "ios", "ipm", "ipr", "ips", "ire", "irk", "ish", 
  "ism", "iso", "ist", "ita", "itd", "itr", "its", "iva", "ivy", "iwa", "iwi",  "jab", "jac", "jag", "jai", "jak", "jam", "jap", "jar", "jaw", "jay", 
  "jee", "jen", "jer", "jet", "jeu", "jib", "jig", "jin", "jiz", "job", 
  "joe", "jog", "jol", "jor", "jot", "jow", "joy", "jud", "jue", "jug", 
  "jun", "jus", "jut",  "kab", "kae", "kaf", "kai", "kak", "kam", "kas", "kat", "kaw", "kay", 
  "kea", "keb", "ked", "kef", "keg", "ken", "kep", "kes", "ket", "kex", 
  "key", "khi", "kia", "kid", "kif", "kin", "kip", "kir", "kis", "kit", 
  "koa", "kob", "koi", "kon", "kop", "kor", "kos", "kow", "kue", "kye", 
  "kyu",  "lab", "lac", "lad", "lag", "lah", "lam", "lap", "lar", "las", "lat", 
  "lav", "law", "lax", "lay", "lea", "led", "lee", "leg", "lei", "lek", 
  "let", "leu", "lev", "lex", "ley", "lez", "lib", "lid", "lie", "lig", 
  "lin", "lip", "lis", "lit", "loa", "lob", "lod", "log", "loo", "lop", 
  "lor", "los", "lot", "lou", "low", "lox", "loy", "lud", "lug", "lum", 
  "lun", "lur", "luv", "lux", "luz", "lye", "lym",  "maa", "mab", "mac", "mad", "mae", "mag", "mai", "mak", "mal", "mam", 
  "man", "map", "mar", "mas", "mat", "maw", "max", "may", "med", "mee", 
  "meg", "meh", "mel", "mem", "men", "mer", "mes", "met", "meu", "mew", 
  "mho", "mib", "mic", "mid", "mig", "mil", "mim", "min", "mir", "mis", 
  "mix", "miz", "mmm", "mna", "moa", "mob", "moc", "mod", "moe", "mog", 
  "moi", "mol", "mom", "mon", "moo", "mop", "mor", "mos", "mot", "mou", 
  "mow", "moy", "moz", "mud", "mug", "mum", "mun", "mus", "mut", "mux", 
  "mwa", "myc",  "nab", "nad", "nae", "nag", "nah", "nam", "nan", "nao", "nap", "nas", 
  "nat", "nav", "naw", "nay", "nde", "neb", "ned", "nee", "nef", "neg", 
  "nek", "nep", "net", "new", "nib", "nid", "nie", "nil", "nim", "nip", 
  "nis", "nit", "nix", "noa", "nob", "nod", "nog", "noh", "nom", "non", 
  "noo", "nor", "nos", "not", "now", "nox", "noy", "nth", "nub", "nug", 
  "nun", "nur", "nus", "nut", "nux", "nye", "nym", "nys",  "oad", "oaf", "oak", "oar", "oat", "oba", "obe", "obi", "obo", "obs", 
  "obv", "oca", "och", "oda", "odd", "ode", "ods", "oer", "oes", "off", 
  "oft", "ohm", "oho", "ohs", "ohv", "oik", "oil", "oka", "oke", "ola", 
  "old", "ole", "olm", "oma", "oms", "one", "ono", "ons", "ony", "oof", 
  "ooh", "oom", "oos", "oot", "ope", "ops", "opt", "ora", "orb", "orc", 
  "ord", "ore", "orf", "org", "oro", "orp", "ors", "ort", "ose", "oud", 
  "oui", "our", "ous", "out", "ova", "ovo", "owe", "owl", "own", "owt", 
  "oxo", "oxy", "ozs",  "pac", "pad", "pah", "pak", "pal", "pam", "pan", "pap", "par", "pas", 
  "pat", "pav", "paw", "pax", "pay", "pea", "pec", "ped", "pee", "peg", 
  "peh", "pel", "pen", "pep", "per", "pes", "pet", "pew", "phi", "pho", 
  "pht", "pia", "pic", "pie", "pig", "pin", "pip", "pir", "pis", "pit", 
  "piu", "pix", "plu", "ply", "poa", "pod", "poh", "poi", "pol", "pom", 
  "poo", "pop", "pos", "pot", "pow", "pox", "poz", "pre", "pro", "pry", 
  "psi", "pst", "pub", "pud", "pug", "puh", "pul", "pun", "pup", "pur", 
  "pus", "put", "puy", "pwn", "pya", "pye", "pyx","qat", "qis", "qua", "que", "qui", "quo",  "rab", "rad", "rag", "rah", "rai", "raj", "ram", "ran", "rap", "ras", 
  "rat", "rav", "raw", "rax", "ray", "reb", "rec", "red", "ree", "ref", 
  "reg", "reh", "rei", "rem", "ren", "reo", "rep", "res", "ret", "rev", 
  "rew", "rex", "rez", "rho", "rhy", "ria", "rib", "rid", "rif", "rig", 
  "rim", "rin", "rip", "rit", "riz", "rob", "roc", "rod", "roe", "rok", 
  "rom", "roo", "rot", "row", "rub", "ruc", "rud", "rue", "rug", "run", 
  "rut", "rya", "rye", "ryu",  "sab", "sac", "sad", "sae", "sag", "sai", "sal", "sam", "san", "sap", 
  "sar", "sat", "sau", "sav", "saw", "sax", "say", "saz", "sea", "sec", 
  "sed", "see", "seg", "sei", "sel", "sen", "ser", "set", "sev", "sew", 
  "sex", "sey", "sez", "sha", "she", "shh", "sho", "shy", "sib", "sic", 
  "sif", "sig", "sik", "sim", "sin", "sip", "sir", "sis", "sit", "six", 
  "ska", "ski", "sky", "sly", "sma", "sny", "sob", "soc", "sod", "sog", 
  "soh", "sol", "som", "son", "sop", "sos", "sot", "sou", "sov", "sow", 
  "sox", "soy", "soz", "spa", "spy", "sri", "sty", "sub", "sud", "sue", 
  "sug", "sui", "suk", "sum", "sun", "sup", "suq", "sur", "sus", "swy", 
  "sye", "syn",  "tab", "tad", "tae", "tag", "tai", "taj", "tak", "tam", "tan", "tao", 
  "tap", "tar", "tas", "tat", "tau", "tav", "taw", "tax", "tay", "tea", 
  "tec", "ted", "tee", "tef", "teg", "tel", "ten", "tes", "tet", "tew", 
  "tex", "the", "tho", "thy", "tic", "tid", "tie", "tig", "tik", "til", 
  "tin", "tip", "tis", "tit", "tix", "tiz", "toc", "tod", "toe", "tog", 
  "tom", "ton", "too", "top", "tor", "tot", "tow", "toy", "try", "tsk", 
  "tub", "tug", "tui", "tum", "tun", "tup", "tut", "tux", "twa", "two", 
  "twp", "tye", "tyg",  "udo", "uds", "uey", "ufo", "ugh", "ugs", "uke", "ule", 
  "ulu", "ume", "umm", "ump", "ums", "umu", "uni", "uns", 
  "upo", "ups", "urb", "urd", "ure", "urn", "urp", "use", 
  "uta", "ute", "uts", "utu", "uva", "uwu",  "vac", "vae", "vag", "van", "var", "vas", "vat", "vau", "vav", "vaw", 
  "vax", "vee", "veg", "vet", "vex", "vey", "via", "vid", "vie", "vig", 
  "vim", "vin", "vip", "vir", "vis", "viz", "vly", "voe", "vog", "vol", 
  "vom", "von", "vor", "vow", "vox", "vug", "vum",  "wab", "wad", "wae", "wag", "wah", "wai", "wan", "wap", "war", "was", 
  "wat", "waw", "wax", "way", "waz", "web", "wed", "wee", "wem", "wen", 
  "wet", "wex", "wey", "wha", "who", "why", "wig", "win", "wis", "wit", 
  "wiz", "woe", "wof", "wok", "won", "woo", "wop", "wos", "wot", "wow", 
  "wox", "wry", "wud", "wus", "wuz", "wye", "wyn","xat","xed", "xes", "xis","xon","xys",  "yaa", "yad", "yae", "yag", "yah", "yak", "yam", "yap", "yar", "yas", 
  "yaw", "yay", "yea", "yed", "yeh", "yen", "yep", "yer", "yes", "yet", 
  "yew", "yex", "yey", "yez", "ygo", "yid", "yin", "yip", "yiz", "yob", 
  "yod", "yok", "yom", "yon", "you", "yow", "yrs", "yug", "yuk", "yum", 
  "yup", "yus",  "zag", "zap", "zas", "zax", "zea", "zed", "zee", "zek", 
  "zel", "zen", "zep", "zex", "zho", "zig", "zin", "zip", 
  "zit", "ziz", "zoa", "zol", "zoo", "zos", "zuz", "zzz",
    # ... (add more 3-letter words as needed)
]
#1
threeLetterNouns = [

  "ace", "act", "ado", "ads", "age", "aid", "aim", "air", "ale", "alp", "amp", "ant", "ape", "arc", "ark", "arm", "art", "ash", "asp", "ass", "auk", "awl", "axe", 
  "bag", "bar", "bat", "bay", "bed", "bee", "beg", "bib", "bid", "bin", "bio", "bit", "boa", "bob", "bog", "boo", "bop", "bow", "box", "boy", "bra", "bro", "bud", "bug", "bum", "bun", "bur", "bus", "buy", "bye",
  

  "cab", "cad", "cam", "can", "cap", "car", "cat", "caw", "cee", "cel", "chi", "cob", "cod", "cog", "con", "coo", "cop", "cot", "cow", "cox", "coy", "cry", "cub", "cud", "cue", "cup", "cur", "cut",
  "dad", "dam", "day", "deb", "den", "dew", "did", "die", "dig", "dim", "din", "dip", "doc", "doe", "dog", "don", "dot", "dry", "dub", "dud", "due", "dug", "duo", "dye",
  "ear", "eat", "ebb", "eco", "eel", "egg", "ego", "elk", "ell", "elm", "emu", "end", "eon", "era", "erg", "eve", "ewe", "eye",
  

  "fad", "fag", "fan", "far", "fat", "fax", "fed", "fee", "fen", "fez", "fib", "fie", "fig", "fil", "fin", "fir", "fit", "fix", "flu", "fly", "fob", "foe", "fog", "fon", "fop", "fox", "fro", "fry", "fun", "fur",
  "gab", "gad", "gag", "gal", "gam", "gap", "gas", "gat", "gel", "gem", "gen", "get", "gig", "gin", "gip", "gnu", "gob", "god", "goo", "got", "gum", "gun", "gut", "guy", "gym", "gyp",
  "hag", "ham", "hat", "haw", "hay", "hem", "hen", "hew", "hex", "hey", "him", "hip", "hit", "hob", "hod", "hog", "hon", "hop", "hot", "how", "hub", "hue", "hug", "hum", "hun", "hut",
  "ice", "ich", "ick", "icy", "ide", "iff", "igg", "ilk", "ill", "imp", "ink", "inn", "ion", "ire", "irk", "ish", "ism", "its", "ivy",
  

  "jab", "jag", "jam", "jar", "jaw", "jay", "jee", "jet", "jib", "jig", "job", "jog", "jot", "joy", "jug", "jun", "jut",
  "keg", "ken", "key", "kid", "kin", "kip", "kit", "koa", "kob", "koi", "kop", "kos", "kue",
  "lab", "lad", "lag", "lam", "lap", "law", "lax", "lay", "lea", "led", "lee", "leg", "lei", "lek", "let", "lex", "lid", "lie", "lip", "lit", "lob", "log", "loo", "lop", "lot", "low", "lox", "lug", "lum", "luv", "lux", "lye",
  
  
  "mac", "mad", "mag", "man", "map", "mar", "mat", "maw", "max", "may", "med", "meg", "mel", "men", "met", "mew", "mid", "mig", "mil", "mim", "min", "mix", "moa", "mob", "moc", "mod", "mog", "mom", "mon", "moo", "mop", "mor", "mos", "mot", "mow", "mud", "mug", "mum", "mun", "mut", "mux", "mys",
  "nab", "nae", "nag", "nah", "nan", "nap", "naw", "nay", "neb", "nee", "neg", "net", "new", "nib", "nil", "nim", "nip", "nit", "nix", "nob", "nod", "nog", "noh", "nom", "non", "noo", "nor", "nos", "not", "now", "nth", "nub", "nun", "nus", "nut", "nye",
  "oaf", "oak", "oar", "oat", "oba", "obe", "obi", "oca", "och", "oct", "odd", "ode", "ods", "oes", "off", "oft", "ohm", "oho", "ohs", "oil", "oka", "oke", "old", "ole", "oms", "one", "ono", "ons", "oof", "oom", "oon", "oor", "oos", "oot", "ope", "ops", "opt", "ora", "orb", "orc", "ord", "ore", "org", "ors", "ort", "ose", "oud", "ouk", "our", "ous", "out", "ova", "owe", "owl", "own", "owt", "oxe", "oxo", "oxs", "oxy", "oye", "oys",
  

  "pac", "pad", "pal", "pam", "pan", "pap", "par", "pas", "pat", "paw", "pax", "pay", "pea", "pec", "ped", "pee", "peg", "peh", "pen", "pep", "per", "pes", "pet", "pew", "phi", "pho", "pht", "pia", "pic", "pie", "pig", "pin", "pip", "pis", "pit", "piu", "pix", "ple", "ply", "poa", "pod", "poh", "poi", "pol", "pom", "poo", "pop", "pos", "pot", "pow", "pox", "poy", "pre", "pro", "prow", "psi", "pst", "pub", "pud", "pug", "puj", "pun", "pup", "pur", "pus", "put", "puy", "pya", "pye", "pyx",
  "qat", "qis", "qua", "quo",
  "rad", "rag", "rah", "rai", "raj", "ram", "ran", "rap", "ras", "rat", "raw", "rax", "ray", "reb", "rec", "red", "ree", "ref", "reg", "rei", "rem", "ren", "reo", "rep", "res", "ret", "rev", "rew", "rex", "rez", "rho", "ria", "rib", "rid", "rif", "rig", "rim", "rin", "rip", "rit", "riv", "riz", "rob", "roc", "rod", "roe", "rok", "rom", "roo", "rot", "row", "rub", "rud", "rue", "rug", "rum", "run", "rut", "rya", "rye",
  
  
  "sab", "sac", "sad", "sae", "sag", "sai", "sal", "sam", "san", "sap", "sar", "sat", "sau", "saw", "sax", "say", "sea", "sec", "sed", "see", "seg", "sei", "sel", "sen", "ser", "set", "sew", "sex", "sey", "fez", "shh", "sho", "shy", "sib", "sic", "sid", "sie", "sig", "sin", "sip", "sir", "sis", "sit", "six", "ska", "ski", "sky", "sob", "soc", "sod", "sof", "sog", "sol", "som", "son", "sop", "sos", "sot", "sou", "sow", "gox", "soy", "spa", "spy", "sub", "sud", "sue", "suk", "sum", "sun", "sup", "suq", "sur", "sus", "swy", "sye",
  "tab", "tad", "tae", "tag", "tai", "taj", "tak", "tam", "tan", "tao", "tap", "tar", "tas", "tat", "tau", "tav", "taw", "tax", "tay", "tea", "tec", "ted", "tee", "teg", "tel", "ten", "tes", "tet", "tew", "tex", "the", "tho", "thy", "tic", "tid", "tie", "tig", "til", "tin", "tip", "tis", "tit", "tix", "tiz", "tod", "toe", "tog", "tom", "ton", "too", "top", "tor", "tot", "tow", "toy", "try", "tsk", "tub", "tug", "tui", "tum", "tun", "tup", "tut", "tux", "twa", "two", "twp", "tye", "tyg",
  
  
  "udo", "ugh", "ugs", "uka", "uke", "ulu", "umm", "ump", "umu", "uni", "uns", "upo", "ups", "urn", "urp", "uru", "use", "uta", "ute", "uts", "uva", "vac", "vae", "vag", "van", "var", "vas", "vat", "vau", "vaw", "vax", "vee", "veg", "vei", "vending", "vet", "vex", "via", "vibe", "vid", "vie", "vig", "vim", "vin", "viny", "vis", "vly", "voe", "vol", "vom", "vow", "vox", "vug", "vum",
  "wab", "wad", "wae", "wag", "wah", "wai", "waw", "wax", "way", "web", "wed", "wee", "wem", "wen", "wet", "wex", "wey", "wha", "who", "why", "wig", "win", "wis", "wit", "wiz", "woe", "wog", "wok", "won", "woo", "wop", "wos", "wot", "wow", "wry", "wud", "wus", "wye", "wyn",
  "xat", "xis", "xon", "xys",
  "yad", "yae", "yak", "yam", "yan", "yap", "yar", "yaw", "yay", "yea", "yeh", "yen", "yep", "yer", "yes", "yet", "yew", "yex", "ygo", "yin", "yip", "yob", "yod", "yok", "yom", "yon", "you", "yow", "yuk", "yum", "yup", "yus", "ywi",
  "zaa", "zag", "zap", "zas", "zat", "zax", "zed", "zee", "zek", "zel", "zen", "zep", "zer", "zig", "zin", "zip", "zit", "ziz", "zoa", "zoo", "zos", "zuz", "zym"
]
#2
largeThreeLetterVerbs = [
 "act", "add", "aid", "aim", "ape", "arm", "ask", "awl", "ban", "bar", "bat", "beg", "bet", "bid", "bit", "bow", "box", "bum", "buy", "can", "cap", "cat", "caw", "con", "cop", "cow", "cry", "cue", "cup", "cum", "cut", "dab", "dam", "day", "die", "dig", "dim", "din", "dip", "dog", "don", "dot", "dry", "dub", "due", "dug", "dye", "eat", "ebb", "egg", "eke", "end", "err", "eye", "fan", "fax", "fed", "fee", "fib", "fit", "fix", "fly", "fog", "fox", "fry", "gab", "gag", "gel", "gem", "get", "gig", "gin", "git", "got", "gum", "gun", "gut", "guy", "had", "hag", "ham", "has", "hat", "haw", "hay", "hem", "hid", "hie", "hip", "hit", "hob", "hoe", "hog", "hop", "hot", "hug", "hum", "hut", "ice", "ink", "inn", "jab", "jag", "jam", "jar", "jaw", "jet", "jib", "jig", "job", "jog", "jot", "joy", "jug", "jut", "keg", "ken", "kep", "key", "kid", "kin", "kip", "kit", "lab", "lac", "lad", "lag", "lam", "lap", "law", "lax", "lay", "led", "leg", "let", "lib", "lid", "lie", "lip", "lit", "lob", "log", "loo", "lop", "lot", "low", "lox", "lug", "lum", "luv", "lux", "mad", "man", "map", "mar", "mat", "maw", "max", "may", "met", "mew", "mix", "mob", "moc", "mod", "mog", "moo", "mop", "mor", "mot", "mow"
]
#3
allThreeLetterAdverbs = [
 "aft", "ago", "all", "any", "awk", "bad", "bak", "ben", "big", "bis", "but", "cam", "dat", "den", "der", "dim", "doe", "due", "eek", "een", "eft", "eke", "ere", "esp", "eva", "far", "fay", "fra", "fro", "gey", "hea", "hen", "hoo", "how", "ill", "ish", "jes", "lak", "low", "mad", "moe", "muy", "nao", "nat", "net", "new", "nix", "non", "noo", "not", "now", "off", "oft", "oop", "orf", "orl", "out", "owt", "pat", "raw", "sam", "say", "sho", "sic", "sly", "str", "ter", "the", "tho", "tog", "top", "viz", "wai", "wat", "way", "wee", "wen", "why", "wis", "yay", "yea", "yep", "yer", "yet", "ygo", "yis", "yon", "yus"
]
#4
allThreeLetterAdjectives = [
 "ace", "all", "alt", "any", "apt", "bad", "big", "bio", "coy", "cut", "def","ten" ,"dim", "dry", "due", "eco", "far", "fat", "few", "fit", "fly", "fun", "fur", "gay", "goy", "hot", "icy", "ill", "key", "lax", "low", "mad", "mid", "neo", "new", "nil", "odd", "off", "old", "one", "out", "own", "pop", "pro", "raw", "red", "sad", "set", "shy", "six", "sly", "sub", "tan", "top", "two", "uni", "wee", "wet", "wry", "zen"
]

#5
threeLetterPronouns = ["all", "any", "few", "her", "him", "his", "its", "one", "our", "she", "who", "you"]
#6
threeLetterPrepositions = [
"and", "bar", "but", "cum", "for", "mid", "off", "out", "per", "pro", "sub", "til", "via"
]

#print(dictionary_arrays)
other_dict={}
other_dict = dict(zip(dictionary_arrays, hilo))    
other_dict['aah']=3
hilo[0]=3
other_dict['aal']=4
hilo[1]=4
other_dict['aas']=5
hilo[2]=5
other_dict['aba']=6
hilo[3]=6
other_dict['yay']=7
hilo[1350]=7
seen = set()
duplicates = set()
for idf in range(0,len(threeLetterNouns)):
    if threeLetterNouns[idf] in other_dict:
        other_dict[threeLetterNouns[idf]]=[other_dict.get(threeLetterNouns[idf])]
        other_dict[threeLetterNouns[idf]].append(1)
for ilo in range(0,len(largeThreeLetterVerbs)):
    if largeThreeLetterVerbs[ilo] in other_dict:
        other_dict[largeThreeLetterVerbs[ilo]]=[other_dict.get(largeThreeLetterVerbs[ilo])]
        other_dict[largeThreeLetterVerbs[ilo]].append(2)
for isuo in range(0,len(allThreeLetterAdverbs)):
    if allThreeLetterAdverbs[isuo] in other_dict:
        other_dict[allThreeLetterAdverbs[isuo]]=[other_dict.get(allThreeLetterAdverbs[isuo])]
        other_dict[allThreeLetterAdverbs[isuo]].append(3)
for iopl in range(0,len(allThreeLetterAdjectives)):
    if allThreeLetterAdjectives[iopl] in other_dict:
        other_dict[allThreeLetterAdjectives[iopl]]=[other_dict.get(allThreeLetterAdjectives[iopl])]
        other_dict[allThreeLetterAdjectives[iopl]].append(4)
for iiu in range(0,len(threeLetterPronouns)):
    if threeLetterPronouns[iiu] in other_dict:
        other_dict[threeLetterPronouns[iiu]]=[other_dict.get(threeLetterPronouns[iiu])]
        other_dict[threeLetterPronouns[iiu]].append(5)
for iople in range(0,len(threeLetterPrepositions)):
    if threeLetterPrepositions[iople] in other_dict:
        other_dict[threeLetterPrepositions[iople]]=[other_dict.get(threeLetterPrepositions[iople])]
        other_dict[threeLetterPrepositions[iople]].append(6)
#print(other_dict) 
def o(target_values,other_dictd,maxk):
    ldfw=0
    for target in target_values:
    # Check if the target value exists as a key in the dictionary
      if target in other_dictd and ldfw>=maxk:
        # Safely fetch the array stored under that key
        array = other_dictd[target]
        return array
        #print(f"Found target '{target}' as a key. Its array value is: {array}")
      ldfw+=1
def h(other_dict,largeThreeLetterVerbsd,allThreeLetterAdverbsd,allThreeLetterAdjectivesd,threeLetterPrepositionsd,threeLetterNounsd,threeLetterPronounsd,IY,IO,OP,ID,HU,HY):    
    klopi=o(threeLetterPrepositionsd,other_dict,ID)#4
    target_value=klopi[0]
    pronoun=""
    Prepositions=""
    verb=""
    noun=""
    adverb=""
    adjectives=""
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            Prepositions=key
    klopi=o(largeThreeLetterVerbsd,other_dict,IY)#2
    target_value=klopi[0]
    
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            verb=key
    
    klopid=o(threeLetterNounsd,other_dict,HU)#3
    target_value=klopid[0]
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            noun=key
   
    klopiol=o(threeLetterPronounsd,other_dict,HY)#4
    target_value=klopiol[0]
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            pronoun=key
    
    klopio=o(allThreeLetterAdverbsd,other_dict,IO)#5
    target_value=klopio[0]
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            adverb=key
    
    klopio=o(allThreeLetterAdjectivesd,other_dict,OP)#6
    target_value=klopio[0]
    for key, value in other_dict.items():
        if isinstance(value, list) and target_value in value:
            adjectives=key
    return verb,adverb,adjectives,Prepositions,pronoun,noun
def iu(ad,da,ko,il,er,ur,other_dictd,largeThreeLetterVerbsd,allThreeLetterAdverbsd,allThreeLetterAdjectivesd,threeLetterPrepositionsd,threeLetterNounsd,threeLetterPronounsd):
    words=(h(other_dictd,largeThreeLetterVerbsd,allThreeLetterAdverbsd,allThreeLetterAdjectivesd,threeLetterPrepositionsd,threeLetterNounsd,threeLetterPronounsd,ad,da,ko,il,er,ur))
    print(words)
    return words
for i in range(0,6):
    iu(2+i,3+i,4+i,5+i,6+i,2+i,other_dict,largeThreeLetterVerbs,allThreeLetterAdverbs,allThreeLetterAdjectives,threeLetterPrepositions,threeLetterNouns,threeLetterPronouns)
