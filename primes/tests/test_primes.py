import pytest
from primes.primes import PrimesList


@pytest.mark.parametrize("test_input, expected", [
    (-1, False),
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (9, False),
    (23, True)
])
def test_is_prime(test_input, expected):
    assert PrimesList.is_prime(test_input) == expected


@pytest.mark.parametrize("start_num, end_num, expected", [
    (1, 1, []),
    (1, 2, [2]),
    (0, 3, [2, 3]),
    (4, 11, [5, 7, 11])
])
def test_primes_list(start_num, end_num, expected):
    p = PrimesList(start_num, end_num)
    assert p.primes_list() == expected
