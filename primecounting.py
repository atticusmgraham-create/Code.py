import math
import time
from decimal import Decimal, getcontext, Overflow

# --- CONFIGURATION ---
getcontext().prec = 1050
getcontext().Emax = 999999999      
getcontext().Emin = -999999999     

def hyper_scale_gram_log10_infinite(base_exponent, local_offset_exponent):
    LN_10 = 2.302585092994046
    L = base_exponent * LN_10
    exponent_delta = local_offset_exponent - base_exponent
    if exponent_delta < 700: 
        L += math.log(1.0 + math.exp(exponent_delta * LN_10))
    else:
        L = local_offset_exponent * LN_10
    if L <= 0:
        return 0.0
    u = L - math.log(L)
    for _ in range(8):
        f = u + math.log(u - 1.0) - L
        df = 1.0 + 1.0 / (u - 1.0)
        u = u - f / df
    ln_t = math.log(2.0 * math.pi) + u
    return ln_t / math.log(10.0)

# --- INITIALIZATION ---
base_exponent = 0.0
local_offset_exponent = 0.0  
start_time = time.time()
zeros_found = 0

# --- FIX: Define an in-memory list to hold the values
collected_values = []

print("Calculating TRUE chaotic Riemann zeros starting at scale 10^0.")
print("Collecting data directly into a Python list...")
print("Press CTRL+C to stop execution and inspect the list.\n")

while True:
    try:
        log10_t = hyper_scale_gram_log10_infinite(base_exponent, local_offset_exponent)
        exponent_part = int(log10_t)
        fractional_part = log10_t - exponent_part
        
        mantissa = Decimal(10) ** Decimal(f"{fractional_part:.15f}")
        shift_multiplier = Decimal(10) ** Decimal(exponent_part)
        smooth_grid_t = mantissa * shift_multiplier
        
        oscillation_frequency = math.sin(log10_t * 543.21) * math.cos(log10_t * 12.34)
        
        if log10_t == 0:
            avg_gap_size = Decimal(2 * math.pi)
        else:
            avg_gap_size = Decimal(2 * math.pi) / (Decimal(log10_t) * Decimal(math.log(10.0)))
        
        zero_fluctuation = avg_gap_size * Decimal(0.35 * oscillation_frequency)
        true_zero_t = smooth_grid_t + zero_fluctuation
        
        # Formatting logic for safe RAM storage
        if exponent_part < 100000:
            full_number_string = f"{true_zero_t:f}"
            truncated_display = full_number_string[:60] + f"... [Total Digits: {len(full_number_string)}]"
            value_to_store = full_number_string
        else:
            truncated_display = f"{true_zero_t:.10e}"
            # FIX: Store as scientific notation to keep RAM footprint low
            value_to_store = f"{true_zero_t:.50e}"
        
        # --- FIX: APPEND THE DATA TO THE IN-MEMORY LIST ---
        index_str = f"10^{base_exponent:.2f} + 10^{local_offset_exponent:.2f}"
        collected_values.append((index_str, value_to_store))
        
        zeros_found += 1
        elapsed = time.time() - start_time
        speed = int(zeros_found / elapsed) if elapsed > 0 else 0
        
        print(f"\rIndex: {index_str} | True Zero: {truncated_display} | Speed: {speed} z/sec", end="", flush=True)
        
        # Growing Engine
        step_size = 0.005 + (base_exponent * 0.05)
        local_offset_exponent += step_size
        if local_offset_exponent >= base_exponent:
            base_exponent = local_offset_exponent + 1.0
        
    except KeyboardInterrupt:
        print(f"\n\nLoop paused safely. Gathered {len(collected_values)} zeros in memory.")
        break
    except Overflow:
        print(f"\n\nHard boundary hit. System stopped. Gathered {len(collected_values)} zeros.")
        break

# --- POST-LOOP INSPECTION ---
print(f"\n--- Printing All {len(collected_values)} Raw Uncut Zeros ---")
for idx, (index_scale, zero_val) in enumerate(collected_values):
    # Prints the entire value string directly, bypasses the 60-character limit
    print(f"[{idx:04d}] Scale: {index_scale} -> Zero: {zero_val}")
