import json
from pathlib import Path


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.splitlines()]}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in text.splitlines()]}


cells = [
    md("""# CS 505 Combinatorics: guided solution notebook

This notebook can solve and verify the numerical problems in the activity. Run the cells from top to bottom. The Markdown explains **why** each formula applies; the code performs the arithmetic."""),
    md("""## Reusable formulas

- A **permutation** is used when order matters: $P(n,r)=n!/(n-r)!$.
- A **combination** is used when order does not matter: $C(n,r)=n!/[r!(n-r)!]$.
- **Stars and bars** distributes identical objects among distinct recipients: $C(n+k-1,k-1)$ for nonnegative allocations."""),
    code("""from math import comb, factorial

def permutations(n, r=None):
    r = n if r is None else r
    return factorial(n) // factorial(n-r)

def combinations(n, r):
    return comb(n, r)

def stars_and_bars(total, boxes, minimum=0):
    remaining = total - boxes * minimum
    return 0 if remaining < 0 else comb(remaining + boxes - 1, boxes - 1)"""),
    md("""## 1. Arrange 10 people in a line

Every position matters. There are 10 choices for the first position, 9 for the second, and so on, giving $10!$."""),
    code("factorial(10)  # 3,628,800"),
    md("""## 2. Select a committee of 5 from 20

A committee has no first or second position, so order does not matter. Use $C(20,5)$."""),
    code("combinations(20, 5)  # 15,504"),
    md("""## 3. Select 2 cards from 52

Selecting ace then king is the same two-card selection as king then ace, so use $C(52,2)$."""),
    code("combinations(52, 2)  # 1,326"),
    md("""## 4. Form 6-letter strings from MISSISSIPPI

Available multiplicities are M=1, I=4, S=4, and P=2. For every valid count pattern $(m,i,s,p)$ with sum 6, the number of arrangements is $6!/(m!i!s!p!)$. Summing all valid patterns enforces the available-letter limits."""),
    code("""def mississippi_six_letter_words(show_patterns=False):
    total, patterns = 0, []
    for m in range(2):       # 0 or 1 M
        for i in range(5):   # 0 through 4 I's
            for s in range(5):
                for p in range(3):
                    if m + i + s + p == 6:
                        ways = factorial(6) // (
                            factorial(m) * factorial(i) * factorial(s) * factorial(p)
                        )
                        total += ways
                        patterns.append(((m, i, s, p), ways))
    return (total, patterns) if show_patterns else total

mississippi_six_letter_words()  # 1,610"""),
    md("""## 5-6. Applications and the key distinction

Permutations model ranked outcomes, schedules, passwords without repeated symbols, and seating orders. Combinations model committees, sampled records, lottery selections, and feature subsets. Ask one diagnostic question: **Would changing only the order create a different outcome?** If yes, use a permutation; if no, use a combination."""),
    md("""## 7. Six identical balls into six distinct boxes

Let $x_j$ be the number of balls in box $j$. Empty boxes are allowed, so solve $x_1+\\cdots+x_6=6$ with nonnegative integers. Stars and bars gives $C(11,5)$."""),
    code("stars_and_bars(6, 6)  # 462"),
    md("""## 8. Fifteen identical candies to 3 children, at least 3 each

Give each child 3 candies first, using 9. The remaining 6 candies may be distributed freely, so solve $y_1+y_2+y_3=6$. The result is $C(8,2)$."""),
    code("stars_and_bars(15, 3, minimum=3)  # 28"),
    md("""## 9. Nonnegative solutions to x1+x2+x3=20

The variables may be zero, so stars and bars gives $C(20+3-1,3-1)=C(22,2)$."""),
    code("stars_and_bars(20, 3)  # 231"),
    md("""## 10. Positive solutions to x1+x2+x3=10

Positive means each variable is at least 1. Set $y_j=x_j-1$, leaving $y_1+y_2+y_3=7$. The answer is $C(9,2)$."""),
    code("stars_and_bars(10, 3, minimum=1)  # 36"),
    md("""## 11. Handling constraints

- **Lower bounds:** allocate each required minimum first, then apply stars and bars to the remainder.
- **Strict positivity:** substitute $y_i=x_i-1$.
- **Upper bounds:** use inclusion-exclusion to subtract allocations that exceed a maximum.
- **Fixed/forbidden values:** condition on the allowed cases or use generating functions/dynamic programming for irregular restrictions."""),
    md("""## 12. Real-world stars-and-bars applications

Examples include allocating identical budget units among projects, distributing identical inventory among stores, counting integer resource allocations among servers, dividing identical rewards among recipients, and counting possible category-frequency profiles in a dataset. The recipients must be distinct, while the allocated units are treated as identical."""),
    md("""## Final verification"""),
    code("""results = {
    "10 people": factorial(10),
    "committee": combinations(20, 5),
    "two cards": combinations(52, 2),
    "MISSISSIPPI": mississippi_six_letter_words(),
    "balls": stars_and_bars(6, 6),
    "candies": stars_and_bars(15, 3, 3),
    "nonnegative": stars_and_bars(20, 3),
    "positive": stars_and_bars(10, 3, 1),
}
results"""),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
Path("outputs/CS_505_Combinatorics_Walkthrough.ipynb").write_text(json.dumps(notebook, indent=2))
print("outputs/CS_505_Combinatorics_Walkthrough.ipynb")
