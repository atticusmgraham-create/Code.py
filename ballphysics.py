n=[]
oi=0
k=0
oo=3
ball = 2.17645e-8
for c in range(0,oo):   
   for ide in range(0,1):
        import numpy as np
        import math
        import time
        
        ME = []
        ts = []
        
        r = 0.01
        
        def u(x, m): return x**2 * m * 0.5
        def PE(K, L): return math.sqrt(K * L * 9.81)
        def f(B): return (B**2) / (2 * 9.81)
        
        total_elapsed_time = 0.0
        
        for timestep in range(0, 3):  
            MEnergy = []
            Ts = []
            
            for i in range(1, 15):
                start_time = time.perf_counter()
                
                for _ in range(3):
                    math.sin(i / r)
                    
                end_time = time.perf_counter()
                T = (end_time - start_time) or 1e-9
                    
                func = abs(-i * math.sin(i / r)**3) / T
                MEnergy.append(PE(ball, f(func) + u(func / T, ball)))
                Ts.append(T)
                  
            AvgVT = sum(MEnergy) / len(MEnergy)
            Tl = sum(Ts) / len(Ts)
            
            total_elapsed_time += Tl
            ME.append(AvgVT)
            ts.append(total_elapsed_time)
        
        # --- PURE MATH LOW-PASS FILTER (NO EXTRA LIBRARIES) ---
        def low_pass_filter(data_list, alpha=0.1):
            """
            Applies a forward-backward exponential moving average filter.
            alpha: Controls smoothing strength. Lower = smoother. Higher = less lag.
            """
            # 1. Forward Pass (Smooths noise but introduces a slight time lag)
            forward = [data_list[0]]
            for val in data_list[1:]:
                forward.append(alpha * val + (1 - alpha) * forward[-1])
                
            # 2. Backward Pass (Removes the time lag so data aligns perfectly)
            backward = [forward[-1]]
            for val in reversed(forward[:-1]):
                backward.append(alpha * val + (1 - alpha) * backward[-1])
                
            backward.reverse() # Restore chronological order
            return np.array(backward)
        
        # Set smoothing factor (0.1 = heavy filtering, 0.3 = light filtering)
        smoothing_factor = 0.1
        smoothing_factord=0.3
        # Clean both datasets using the native low-pass function
        ts_pass1 = low_pass_filter(ts, alpha=smoothing_factor)
        ME_pass1 = low_pass_filter(ME, alpha=smoothing_factord)
    
    # Second filtering pass (smooths out remaining low-frequency waves)
        ts_clean1 = low_pass_filter(ts_pass1, alpha=smoothing_factor)
        ME_clean1 = low_pass_filter(ME_pass1, alpha=smoothing_factord)
    
    
        # Compute gradients on the cleanly smoothed data
        MEA = np.gradient(ME_clean1, ts_clean1)
        
        oi=len(MEA)*oo
        n.append(sum(MEA))
        k+=(sum(MEA)/len(MEA))
Me=sum(n)/oi

print("avg mechaincal energy:",f"{Me:.2g}","joules")
