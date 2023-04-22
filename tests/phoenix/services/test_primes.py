import sys

from phoenix.services.primes import is_prime


def test_with_test_set(primes_testset):
    found_primes = []
    for number in range(0, 1000):
        if is_prime(number):
            found_primes.append(number)

    assert found_primes == primes_testset


def test_big_prime_number(big_prime_number):
    assert is_prime(big_prime_number)


def test_big_non_prime_number(big_non_prime_number):
    assert not is_prime(big_non_prime_number)
