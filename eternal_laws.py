def enforce_odd(n):
    return max(5, 2 * ((n + 1) // 2) - 1)  # Force odd, min 5, scalable

def is_odd_positive(n):
    return n >= 5 and n % 2 == 1

# Example council size
council_size = enforce_odd(12)  # → 11
