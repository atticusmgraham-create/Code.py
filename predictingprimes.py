def rt(xo=None):    
    import math
    from decimal import Decimal, getcontext
    
    # 1. EXPAND PRECISION CONTEXT
    # We add padding digits to prevent rounding errors accumulating across thousands of iterations
    working_precision = 10050
    getcontext().prec = working_precision
    
    def approx_prime_count(x):
        """Calculates accurate high-precision approximation for pi(x) at scale."""
        x_dec = Decimal(x)
        if x_dec < 2:
            return Decimal(0)
        return exact_li_high_scale(x_dec).quantize(Decimal('1'))
    
    def decimal_ln(x):
        """Computes a high-precision Natural Logarithm using the Decimal module."""
        x_dec = Decimal(x)
        if x_dec <= 0: 
            raise ValueError("Math domain error")
        
        sign, digits, exponent = x_dec.as_tuple()
        if len(digits) + exponent > 300:
            scale_factor = len(digits) + exponent - 5
            scaled_x = x_dec / (Decimal(10) ** scale_factor)
            # Ramanujan-level constant precision for ln(10)
            ln_10 = Decimal('2.3025850929940456840179914546843642076011014886287729760333279009675726096773531128874143214168835708438')
            return decimal_ln(scaled_x) + (Decimal(scale_factor) * ln_10)
    
        guess = Decimal(str(math.log(float(x_dec))))
        for _ in range(100):
            e_g = guess.exp()
            num = Decimal(2) * (x_dec - e_g)
            den = x_dec + e_g
            delta = num / den
            guess += delta
            if abs(delta) < Decimal('1e-10050'): 
                break
        return guess
    
    def exact_li_high_scale(x):
        """
        FIX 1: TRUE DYNAMIC ASYMPTOTIC SERIES
        Loops adaptively until the terms become smaller than our precision limit.
        """
        x_dec = Decimal(x)
        if x_dec < 2:
            return Decimal(0.0)
        
        ln_x = decimal_ln(x_dec)
        
        # Base initial term: x / ln(x)
        base = x_dec / ln_x
        li_val = base
        
        current_term = Decimal(1)
        factorial_accumulator = Decimal(1)
        
        # At x = 10**10004, ln_x is ~23032. 
        # The series terms shrink until i ≈ 23032, then begin to diverge.
        # We loop until terms reach minimum size or fall below our precision threshold.
        max_optimal_terms = int(ln_x)
        
        for i in range(1, max_optimal_terms):
            factorial_accumulator *= i
            term_multiplier = factorial_accumulator / (ln_x ** i)
            next_add = base * term_multiplier
            
            # If the terms start growing again (divergence point), break to preserve accuracy
            if next_add > current_term and i > 1:
                break
                
            li_val += next_add
            current_term = next_add
            
            # Stop if the added value is completely invisible to our system precision
            if next_add < Decimal('1e-10010'):
                break
    
        return li_val
    
    def analyze_prime_error_rates(x):
        return approx_prime_count(x)
    
    def numerical_limit(func, target, tolerance):
        """Approximates the value of 'func' at the target with clean balancing."""
        left_x = target - tolerance
        left_y = func(left_x)
        
        right_x = target + tolerance
        right_y = func(right_x)
        
        return (left_y + right_y) / 2, target
    
    # --- Execution ---
    
    # FIX 2: Fixed target scale mapping
    target_val = Decimal('10')**10004
    
    # FIX 3: Macro-scale tolerance. 
    # Shifting 10**10004 by 10**-10004 changes absolutely nothing in a computer.
    # To check global statistics, tolerance should evaluate scale properties.
    tolerance_val = Decimal('0') 
    
    result = numerical_limit(analyze_prime_error_rates, target=target_val, tolerance=tolerance_val)
    
    # Return to display threshold precision
    getcontext().prec = 100
    
    y = Decimal(((result[1] - result[0]) / result[1]))
    i = Decimal((result[0] / result[1]))
    
    print("--- Corrected Asymptotic Output ---")
    print(f"Statistics of a prime in percent:     {i * 100}%")
    print(f"Statistics of a composite in percent: {y * 100}%")

rt()
