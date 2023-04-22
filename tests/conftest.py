import pathlib

import pytest


@pytest.fixture(scope="session")
def testdir():
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def testset_dir(testdir):
    return testdir / pathlib.Path("primes_lower_1000.txt")


@pytest.fixture(scope="session")
def big_prime_number():
    return 40000967


@pytest.fixture(scope="session")
def big_non_prime_number():
    return 40000969


@pytest.fixture(scope="session")
def primes_testset(testset_dir):
    with open(testset_dir, "r") as testset:
        return [int(d) for d in testset.read().split(",")]
