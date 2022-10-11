import random


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x, y, N):
    # Base Case
    if y == 0:
        return 1  # O(N) + c
    z = mod_exp(x, y // 2, N)  # O(n^2) + c
    # Check if y is even or odd
    if y % 2 == 0:  # c
        return (z ** 2) % N  # O(n^2) + O(n^2) + c
    else:
        return x * (z ** 2) % N  # O(n^2) + O(n^2) + O(n^2) + c


def fprobability(k):
    # Probability of being correct with Fermat Algorithm
    return 1 - (1 / 2) ** k  # O(n) + O(n^2) + c


def mprobability(k):
    # Probability of being correct with Miller-Rabin Algorithm
    return 1 - (1 / 4) ** k  # O(n) + O(n^2) + c


def fermat(N, k):
    # Loop through k times choosing a different a each time
    for i in range(0, k):  # k
        # If the fermat algorithm ever returns composite then N is composite
        if fermat_helper(N) == "composite":  # O(n^2)
            return "composite"  # c
    # If the loop finishes without returning composite then N is prime
    return "prime"  # c


def fermat_helper(N):
    # Select a random number a
    a = random.randint(1, N)  # O(n)
    # check if a^(N-1) = 1%N
    if mod_exp(a, (N - 1), N) == 1:  # O(n^2)
        return "prime" # c
    else:
        return "composite" # c


def miller_rabin(N, k):
    # Loop through k times choosing a different a each time
    for i in range(0, k):  # k
        # Select a random number a
        a = random.randint(1, N)  # O(n)
        z = mr_helper(a, (N - 1), N)  # O(n^2)

        # If the miller-rabin algorithm ever returns composite then N is composite
        if z == "composite":
            return "composite"  # c
    # If the loop finishes without returning composite then N is prime
    return "prime"  # c


def mr_helper(a, exp, N):
    # Continue to divide the exponent by 2 while it is even
    while exp % 2 == 0:  # O(n^2)
        # Perform modular exponentiation
        res = mod_exp(a, exp, N)  # O(n^2)
        # if mod_exp returns a 1 (not needed in if-else) keep going
        # else if a -1 (shown below) return and pick a new number a
        # else return composite
        if res == (N - 1):  # O(n)
            return "prime"  # c
        elif res > 1:  # O(n)
            return "composite"  # c
        # Divide the exponent by 2
        exp = exp // 2  # O(n^2)

    # If every result of mod_exp is a 1 then return prime
    return "prime"  # c
