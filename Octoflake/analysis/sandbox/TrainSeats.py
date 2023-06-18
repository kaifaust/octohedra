"""You're designing a program for making seating assignments on a train! The train has
`n` seats, arranged in a single row. Everyone who will be traveling on the train would
like to sit as far from the ends of the train, and from eachother as possible.

Given the value of `n` compute a list of length `n` that contains the numbers `[0, n -
1]` that represent in what order seats should be filled so the following is true:


1. As each person is seated, they are placed as far away from the already-filled seats
(and the ends of the train) as possible.

2. If there are multiple equivilant seats according to condition 1, they are seated in
the largest stretch of open seats avalible.

3. If there are multiple equivilant seats according to conditions 1 and 2, they are
placed in the seat with the lowest index.

As an example where `n=8`:

Printing seating of length 8
...X.... Seating someone in seat 3. (Seats 3 and 4 have 3 empty seats, so pick the lower index)
...X.X.. Seating someone in seat 5. (Seats 1, 5, and 6 have 1 empty seats, so pick the bigger gap and lower index)
.X.X.X.. Seating someone in seat 1. (Only seat 1 has 1 empty seat)
.X.X.XX. Seating someone in seat 6. (All remaining seats have neighbors, so pick the biggest gap and lower index)
XX.X.XX. Seating someone in seat 0. (All remaining seats are equivilant, so pick the lowest index)
XXXX.XX. Seating someone in seat 2. (And so on)
XXXXXXX. Seating someone in seat 4.
XXXXXXXX Seating someone in seat 7.


Some edge cases:

 - If `n=0` return the empty list.

"""

import time
from collections import deque
from heapq import heappush, heappop

"""
Brute Force
Time: O(n^3)
Space: O(n)

For each seating to generate, scan all seats and manually calculate the minimum distance
to an occupied seat/end of train and gap size.

I think there's definintly some refinements to this approach that
would get it to O(n^2)?

"""


def bruteForceSeatingSequence(n):
    return [seat for seat in bruteForceSeatingGenerator(n)]


def bruteForceSeatingGenerator(n):
    # Seats start unoccupied
    seats = [False] * n
    for _ in range(n):
        best_seat = -1

        # (distance to closest occupied seat, size of gap)
        best_distance = (
            -1,
            -1,
        )

        for potential_seat in range(n):

            # If someone is already sitting in the potential_seat, move on
            if seats[potential_seat]:
                continue

            left, right = potential_seat, potential_seat

            # Scan left until we hit an occupied seat or the end of the train
            while left >= 0 and not seats[left]:
                left -= 1

            # Scan right until we hit an occupied seat of the end of the train
            while right < n and not seats[right]:
                right += 1

            empty_left = potential_seat - left - 1
            empty_right = right - potential_seat - 1

            # (distance to closest occupied seat, size of gap)
            distance = (min(empty_left, empty_right), empty_left + empty_right)

            # Don't replace if there is a lower index seat with this distance
            if (distance > best_distance):
                best_seat, best_distance = potential_seat, distance
        seats[best_seat] = True
        yield best_seat


"""
Heap based
Time: O(n log n)
Space: O(n)

Keep track of a max-heap of the gaps between occupied seats (also
sorted from left to right). For each seating, pop the biggest/leftmost
gap, seat the person in the middle, and put the two resulting
intervals back into the heap.

"""


def heapSeatingSequence(n):
    return [seat for seat in heapSeatingGenerator(n)]


def heapSeatingGenerator(n):
    # (gap size (negative because heapq only does min-heaps), left end of gap, right end)

    gaps = [(-n, -1, n)]
    for _ in range(n):
        # Get the biggest, left-most gap
        m, l, r = heappop(gaps)

        # Seat someone in the middle (rounded down if the gap is of an even size)
        s = (r + l) // 2

        # put the resulting gaps back into the heap.
        heappush(gaps, (-(s - 1 - l), l, s))
        heappush(gaps, (-(r - 1 - s), s, r))
        yield s


"""
Queue based
Time: O(n)
Space O(n)

Hoooooboy. This one took me a full day and a half to figure out.

Theroum: We can consider this problem as a binary tree, where the gap of the full train
is the root node. We expand each node by placing a person in the seat at the center,
which splits the gap into two new gaps. There are only two sizes of gap at each level of
the tree, so to seat everyone, we need only consider one level in the tree at a time
(until the gaps are of size 2).


Lemma 1: Splitting a gap of size n and a gap of size n-1 both result in only two new
sizes of gap that themselves only differ by one.

When splitting a gap of size `n` when `n` is odd, then the new gaps are both of size `(
n - 1) / 2`. As an example:

......... # Gap of 9
....X.... # New gaps of 4 and 4

 If `n` is even, then the new gaps are of size `n / 2` and `n / 2 - 1`. As an example:

........ # Gap of 8
...X.... # New gaps of 3 and 4


If `n` is even. Then `n - 1` is odd, and the two gap sizes split as follows:

n     -> ( n / 2,  n / 2 - 1)
n - 1 -> ( ((n - 1) - 1) / 2 )
      -> ( (n - 2) / 2 )
      -> ( n / 2 - 1 )

Thus, splitting gaps of size `n` and `n - 1` results in only two sizes of gap if `n` is
even, and those gap sizes are `n/2` and `n/2 -1`, which only differ by one.

Let's look at the case where `n` is odd. Then `n - 1` is even, and the gaps split as follows:

n     -> ( (n - 1) / 2)
n - 1 -> ( (n - 1) / 2, (n - 1) / 2 - 1)

Thus splitting gaps of `n` and `n - 1` if `n` is odd results in only two sizes of gap, and those sizes are `( (n - 1) / 2, (n - 1) / 2 - 1)` which again, only differ by one.









"""


def queueSeatingSequence(n, debug=False):
    return [seat for seat in queueSeatingGenerator(n, debug)]


def appendIfNonEmpty(q, interval):
    l, r = interval
    if r - l > 1:
        q.append(interval)


def queueSeatingGenerator(n, debug=False):
    big = n + 1

    current_gen = deque()  # All gaps at this level, ordered left to right
    current_gen_big = deque()  # All big gaps at this level, ordered left to right
    current_gen_small = deque()  # All small gaps at this level l to r

    next_gen = deque([(-1, n)])
    next_gen_big = deque([(-1, n)])
    next_gen_small = deque([(-1, n)])

    for i in range(n):
        if not current_gen_small:  # If we've exhausted a level
            big = big // 2  # Next level's big size n / 2 or n / 2 -1
            current_gen = next_gen
            current_gen_big = next_gen_big
            current_gen_small = next_gen_small

            next_gen = deque()
            next_gen_big = deque()
            next_gen_small = deque()

            # print("Starting a new generation")
            # print(current_gen)
            # print(current_gen_big)
            # print(current_gen_small)

        # Expand all gaps, left to right, populating the next level
        if current_gen:
            l, r = current_gen.popleft()  # Get the leftmost gap at this level
            s = (r + l) // 2  # Compute the middle of that gap

            # Put the resulting gaps into the next level
            appendIfNonEmpty(next_gen, (l, s))

            # Put gaps into the appropriate size queue for the next level
            appendIfNonEmpty(next_gen, (s, r))
            for start, end in [
                (l, s),
                (s, r),
            ]:
                gap = end - 1 - start
                if gap == big:
                    appendIfNonEmpty(next_gen_big, (start, end))
                    if gap == 2:
                        appendIfNonEmpty(next_gen_small, (start + 1, end))
                else:
                    appendIfNonEmpty(next_gen_small, (start, end))

        if current_gen_big:
            # If we have any big gaps left, seat someone in the left-most gap
            l, r = current_gen_big.popleft()
            yield (r + l) // 2
        else:
            # We only have small gaps left, so seat someone in the leftmost small gap
            l, r = current_gen_small.popleft()
            yield (r + l) // 2


# n = 8
# bruteSeating = bruteForceSeatingSequence(n)
# printSeating(bruteSeating)

# queueSeating = queueSeatingSequence(n, True)
# printSeating(queueSeating)

# exit()


"""

Testing


"""


def printSeating(seating):
    n = len(seating)
    print(f"Printing seating of length {n}")
    seats = [False] * n
    for seat in seating:
        seats[seat] = True
        seating_chart = "".join(["X" if seat else "." for seat in seats])
        print(seating_chart, f"Seating someone in seat {seat}.")
    print()


def compare_results(max_train_size, print_seatings=False):
    for n in range(max_train_size + 1):
        bruteSeating = bruteForceSeatingSequence(n)
        heapSeating = heapSeatingSequence(n)
        queueSeating = queueSeatingSequence(n)
        is_correct = queueSeating == heapSeating == bruteSeating
        if is_correct:
            print(f"Consistant for {n}!")
            if print_seatings:
                printSeating(queueSeating)
        else:
            print(f"\nInconsistant for {n}!")
            print("Brute-force:")
            printSeating(bruteSeating)
            print("Heap-based:")
            printSeating(heapSeating)
            print("Queue-based:")
            printSeating(queueSeating)


compare_results(10)

exit()

BRUTE_FORCE_THRESHOLD = 1000


def compare_timing(n):
    print(f"Testing timing for train of length {n}.")
    if n <= BRUTE_FORCE_THRESHOLD:
        t_0 = time.time()
        for _ in bruteForceSeatingGenerator(n):
            pass
        t_f = time.time()
        print(f"Brute force time:\t {t_f - t_0}")
    else:
        print(
            f"Test too big ({n} > {BRUTE_FORCE_THRESHOLD}, skipping brute force cuz it'd take forever."
        )

    t_0 = time.time()
    for _ in queueSeatingGenerator(n):
        pass
    t_f = time.time()
    print(f"Heap based time:\t {t_f - t_0}")

    t_0 = time.time()
    for _ in queueSeatingGenerator(n):
        pass
    t_f = time.time()
    print(f"Queue based time:\t {t_f - t_0}")
    print()


for e in range(8):
    compare_timing(10 ** e * 2)
