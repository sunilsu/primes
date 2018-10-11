import math
from concurrent.futures import ProcessPoolExecutor

# TODO make this configurable
# number of cores
N_PROCS = 8
pool = ProcessPoolExecutor(N_PROCS)


class PrimesList:
    """
    Class that holds the range of numbers and computes the prime list
    proxy for a long running task.
    """

    def __init__(self, start_num, end_num):
        self.start_num = start_num
        self.end_num = end_num

    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0 and n > 2:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def primes_list(self):
        """
        parallelize using ProcessPoolExecutor to find primes in a range
        :return: list of primes in range
        """
        it = range(self.start_num, self.end_num + 1)
        primes = pool.map(PrimesList.is_prime, it)
        primes = [n for n, p in zip(it, primes) if p]
        print(primes)
        return primes

