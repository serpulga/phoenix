import math


def is_prime(number: int) -> bool:
    # Handle small numbers.
    if number <= 3:
        return number > 1
    if number <= 4:
        if number % 2 == 0 or number % 3 == 0:
            return False

    # A few rules to possibly discard large numbers.
    # https://byjus.com/maths/how-to-find-prime-numbers/
    digits = str(number)
    last_number = int(digits[-1])
    if last_number in [0, 2, 4, 6, 8]:
        # Numbers ending with 0, 2, 4, 6 and 8 are never prime numbers.
        return False
    elif number > 5 and last_number == 5:
        # Number greater than 5 and ends with 5 is always divisible by 5,
        # so they are not a prime number.
        return False
    elif sum([int(d) for d in digits]) % 3 == 0:
        # Numbers whose sum of digits are divisible by 3 are never
        # prime numbers.
        return False

    # 6K + 1 technique:
    # https://en.wikipedia.org/wiki/Primality_test
    limit = math.isqrt(number)
    for i in range(5, limit + 1, 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True
