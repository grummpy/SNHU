"""Code walkthrough for the CS 505 combinatorics activity.

Run this file in PyCharm, or use the companion Jupyter notebook.
Only Python's standard library is required.
"""

from math import comb, factorial


def permutations(n, r=None):
    """Ordered arrangements: n! when r is omitted; otherwise n!/(n-r)!"""
    r = n if r is None else r
    return factorial(n) // factorial(n - r)


def combinations(n, r):
    """Unordered selections: n choose r."""
    return comb(n, r)


def stars_and_bars(total, boxes, minimum=0):
    """Distribute identical objects into distinct boxes with a shared minimum."""
    remaining = total - boxes * minimum
    if remaining < 0:
        return 0
    return comb(remaining + boxes - 1, boxes - 1)


def mississippi_six_letter_words(show_patterns=False):
    """Count length-6 strings using at most M1, I4, S4, and P2."""
    total = 0
    patterns = []
    for m in range(0, 2):
        for i in range(0, 5):
            for s in range(0, 5):
                for p in range(0, 3):
                    if m + i + s + p == 6:
                        arrangements = factorial(6) // (
                            factorial(m) * factorial(i) * factorial(s) * factorial(p)
                        )
                        total += arrangements
                        patterns.append(((m, i, s, p), arrangements))
    return (total, patterns) if show_patterns else total


def main():
    print("1. Arrange 10 people:", factorial(10))
    print("2. Select 5 from 20:", combinations(20, 5))
    print("3. Select 2 cards from 52:", combinations(52, 2))
    print("4. Six-letter MISSISSIPPI strings:", mississippi_six_letter_words())
    print("7. Six balls into six boxes:", stars_and_bars(6, 6))
    print("8. Fifteen candies, minimum 3 each:", stars_and_bars(15, 3, minimum=3))
    print("9. Nonnegative x1+x2+x3=20:", stars_and_bars(20, 3))
    print("10. Positive x1+x2+x3=10:", stars_and_bars(10, 3, minimum=1))


if __name__ == "__main__":
    main()

