from decimal import Decimal, getcontext
import decimal

# Set precision to 65 decimal places to easily clear 10^50
getcontext().prec = 65

def true_riemann_trend_high_precision(n_int):
    """
    Finds the baseline of the n-th Riemann zero using 65-digit precision decimal math.
    Removes the volatile linear regression layers entirely.
    """
    n = Decimal(n_int)
    pi = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923')
    e = Decimal('2.7182818284590452353602874713526624977572470936999595749669676277')
    
    # Precise initial guess for y = t / 2pi using first-order approximation
    # n = y * ln(y) - y -> y approx n / (ln(n) - 1)
    ln_n = n.ln()
    y = n / (ln_n - Decimal('1'))
    
    # Newton-Raphson Solver on the true Riemann-von Mangoldt baseline
    for _ in range(25):
        f = y * y.ln() - y - n
        df = y.ln()
        if df == 0:
            break
        y_next = y - f / df
        if abs(y_next - y) < Decimal('1e-20'):
            y = y_next
            break
        y = y_next
        
    return Decimal('2') * pi * y

# Test target indices around 10^50 safely
future_targets = [(10**100)+1, (10**100)+2, (10**100)+3]

print("--- High-Precision Baseline Positions ---")
for idx in future_targets:
    pred = true_riemann_trend_high_precision(idx)
    print(f"Index: {pred}")
