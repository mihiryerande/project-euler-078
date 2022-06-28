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

# Triangular grid to keep track of partitions counted
# PARTITION_WAYS[i][j] is the
#   number of ways to partition `i`
#   where the parts cannot exceed `j+1`.
# No partitions exist where max part is 0, which is why `j` is shifted.
PARTITION_COUNTS = []


def partition_count_from_grid(n, max_part):
    """
    Returns the computed value of number of partitions of `n`
      where the parts in any such partition do not exceed `max_part`,
      if this value has already been computed and stored in the grid,
      else None.

    Args:
        n        (int): Non-negative integer
        max_part (int): Maximum allowed value of any part

    Returns:
        (Optional[int]):
            Number of partitions of `n` having maximum part value at most `max_part`, if already memoized.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n >= 0
    assert max_part is None or type(max_part) == int and max_part >= 0

    global PARTITION_COUNTS

    max_part = max(1, min(n, max_part or n))
    if n < len(PARTITION_COUNTS) and max_part - 1 < len(PARTITION_COUNTS[n]):
        return PARTITION_COUNTS[n][max_part - 1]
    else:
        return None


def partition_count(n_0, max_part_0=None):
    """
    Returns the number of partitions of `n`
      where the parts in any such partition do not exceed `max_part`.
    Note that this also includes partitions having no parts of size `max_part`.

    Args:
        n_0        (int): Non-negative integer
        max_part_0 (int): Maximum allowed value of any part

    Returns:
        (int): Number of partitions of `n` having maximum part value at most `max_part`.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n_0) == int and n_0 >= 0
    assert max_part_0 is None or type(max_part_0) == int and max_part_0 >= 0

    # No partitions of `n_0` having parts greater than `n_0` itself.
    # So just skip down to `max_part_0` as `n_0`, as that's the desired answer anyway.
    max_part_0 = max(1, min(n_0, max_part_0 or n_0))

    # Idea:
    #     Attempt to use `max_part` as much as possible to achieve `n`.
    #     Siphon off `max_part` one-by-one, using smaller partition sizes to fill the gap.
    #     To avoid redundant computation, maintain computed counts in `PARTITION_COUNTS`
    #
    #     Also had to rewrite using a stack to avoid hitting max recursion depth.

    global PARTITION_COUNTS
    query_stack = [(n_0, max_part_0)]

    while len(query_stack) > 0:
        n, max_part = query_stack.pop()

        if partition_count_from_grid(n, max_part) is None:
            # Extend triangular grid with empty/null values to avoid indexing issues
            PARTITION_COUNTS += [[] for _ in range(n+1-len(PARTITION_COUNTS))]
            PARTITION_COUNTS[n] += [None for _ in range(max_part-len(PARTITION_COUNTS[n]))]

            if n == 0 or max_part == 1:
                # Base cases:
                #   * n = 0        -> Doesn't really make sense, but let it be 1 to satisfy higher calls
                #   * max_part = 1 -> Only one such partition, which is simply (1+...+1), i.e. `1` added `n` times
                PARTITION_COUNTS[n][max_part-1] = 1
            else:
                # Recurrent cases to be added,
                #   by decomposing this partitioning into partitions of lesser numbers/parts
                ways = 0
                sub_stack = []  # Substack of lower args not yet computed

                # Use as much of `max_part` as possible
                next_max_part = max_part - 1
                for remaining_sum in range(n, -1, -max_part):
                    # Check if this lower call has already been computed
                    ways_this = partition_count_from_grid(remaining_sum, next_max_part)
                    if ways_this is None:
                        this_max_part = max(1, min(remaining_sum, next_max_part))
                        sub_stack.append((remaining_sum, this_max_part))
                    elif len(sub_stack) == 0:
                        ways += ways_this
                    else:
                        continue

                if len(sub_stack) > 0:
                    # Can't yet memoize the partition count, as we need the lower values first
                    query_stack.append((n, max_part))  # Need to check this again later
                    query_stack += sub_stack  # Compute the lower values first
                else:
                    # No missing entries in grid, so memoize newly summed count
                    PARTITION_COUNTS[n][max_part-1] = ways
        else:
            continue

    return PARTITION_COUNTS[n_0][max_part_0-1]


def main(f):
    """
    Returns the least number `n` for which
      the number of partitions of `n`, p(n), is divisible by factor `f`.

    Args:
        f (int): Natural number

    Returns:
        (int, int):
            Tuple of ...
              * First `n` s.t. `f` divides p(n)
              * p(n)

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(f) == int and f > 0

    # Idea:
    #     Refer to [https://en.wikipedia.org/wiki/Partition_(number_theory)]
    #     Essentially just counting the number of partitions of `n`.
    #     Since no closed-form expression is known,
    #       just search until first valid `n` is found.

    n = 1
    while True:
        p_n = partition_count(n)
        if p_n % f == 0:
            return n, p_n
        else:
            n += 1
            continue


if __name__ == '__main__':
    partition_divisible_factor = int(input('Enter a natural number: '))
    partition_n, partition_count = main(partition_divisible_factor)
    print('Least value of `n` for which p(n) divisible by {}:'.format(partition_divisible_factor))
    print('  n     = {}'.format(partition_n))
    print('  p({}) = {}'.format(partition_n, partition_count))
