# Problem 78:
#     Coin Partitions
#
# Description:
#     Let p(n) represent the number of different ways in which n coins can be separated into piles.
#     For example, five coins can be separated into piles in exactly seven different ways, so p(5) = 7.
#
#         00000
#         0000   0
#         000   00
#         000   0   0
#         00   00   0
#         00   0   0   0
#         0   0   0   0   0
#
#     Find the least value of n for which p(n) is divisible by one million.

def pentagonal(k: int) -> int:
    """
    Returns the generalized pentagonal number (g{k}).

    Args:
        k (int): Integer

    Returns:
        (int): Generalized pentagonal number g{k}

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(k) == int
    return k * (3*k - 1) // 2


def main(f: int) -> int:
    """
    Returns the least number `n` for which
      the number of partitions of `n`, p(n), is divisible by factor `f`.

    Args:
        f (int): Natural number

    Returns:
        (int): First `n` s.t. `f` divides p(n)

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(f) == int and f > 0

    # Problem:
    #     Refer to [https://en.wikipedia.org/wiki/Partition_(number_theory)]
    #     Essentially just counting the number of partitions of `n`,
    #       and then returning the first `n` which is divisible by `f`.
    #     No closed-form expression is known, so just need to search for first such `n`.

    # Idea 0:
    #     Attempted to calculate p(n) iteratively,
    #       using dynamic programming with a triangular grid to keep track of prior output,
    #       but that took too long.

    # Idea 1:
    #     Refer to [https://en.wikipedia.org/wiki/Pentagonal_number_theorem#Relation_with_partitions]
    #     Instead of previous dynamic programming method of partition-counting,
    #       use a recurrence related to the (generalized) pentagonal numbers
    #       to calculate each subsequent p(n) using prior output.
    #     Should be much less time- and memory-intensive than previously attempted method.

    # Idea 2:
    #     Only need to know if p(n) is divisible by `f`,
    #       i.e. p(n) = 0 [mod f].
    #     So just keep track of p(n) [mod f], and return `n` once we hit a 0.

    # Start with p(0) = 1 as base case for recurrence
    p = [1]

    n = 1
    while True:
        # Calculate p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + ...
        #   where 1, 2, 5, 7, etc, are the generalized pentagonal numbers.
        p_n = 0

        k = 0
        sign = -1
        while True:
            # k is { 1, -1, 2, -2, 3, -3, ... }
            k = -k if k > 0 else 1-k

            # sign is { +, +, -, -, +, +, -, -, ... }
            if k > 0:
                sign *= -1

            # p(x) = 0 for all x < 0, so stop when g_k exceeds n
            g_k = pentagonal(k)
            if g_k > n:
                break
            else:
                p_n += sign * p[n - g_k]
                p_n %= f
                continue

        if p_n == 0:
            return n
        else:
            p.append(p_n)
            n += 1
            continue


if __name__ == '__main__':
    partition_divisible_factor = int(input('Enter a natural number: '))
    partition_n = main(partition_divisible_factor)
    print('Least value of `n` for which p(n) divisible by {}:'.format(partition_divisible_factor))
    print('  n = {}'.format(partition_n))
