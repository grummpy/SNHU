"""
CS 505 Module Seven Boolean Algebra

Run this file in PyCharm. It uses only Python's standard library.

The program:
1. Solves and verifies each Boolean-algebra problem.
2. Prints every truth table in the PyCharm console.
3. Saves each truth table as a CSV file.
4. Creates boolean_outputs/boolean_algebra_report.html with colored tables
   and logic-circuit diagrams that open in any browser.
"""

from csv import writer
from itertools import product
from pathlib import Path
from html import escape


OUTPUT_FOLDER = Path(__file__).parent / "boolean_outputs"


def bit(value):
    """Convert True/False to the easier-to-read values 1/0."""
    return 1 if bool(value) else 0


def nand(left, right):
    """Return the NAND of two Boolean inputs."""
    return not (left and right)


def make_truth_table(variable_names, function):
    """Calculate all input combinations for a Boolean function."""
    rows = []
    for values in product([0, 1], repeat=len(variable_names)):
        boolean_values = tuple(bool(value) for value in values)
        output = bit(function(*boolean_values))
        rows.append((*values, output))
    return [*variable_names, "F"], rows


def print_table(title, headers, rows):
    """Print a small truth table in the PyCharm console."""
    print("\n" + title)
    print("-" * len(title))
    print(" | ".join(headers))
    print("-" * (4 * len(headers) - 1))
    for row in rows:
        print(" | ".join(str(value) for value in row))


def save_csv(filename, headers, rows):
    """Save a truth table so it can be opened in Excel or PyCharm."""
    path = OUTPUT_FOLDER / filename
    with path.open("w", newline="", encoding="utf-8") as file:
        csv_writer = writer(file)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)
    return path


def expressions_match(variable_count, first_function, second_function):
    """Prove two expressions match by checking every possible input row."""
    for values in product([False, True], repeat=variable_count):
        if bool(first_function(*values)) != bool(second_function(*values)):
            return False, values
    return True, None


def problem_1_simplify_expressions():
    """Problem 1: simplify and verify all four expressions."""

    original_a = lambda A, B, C: (
        not ((not A) and B and (not C))
    ) or (A and ((not B) or C))
    simple_a = lambda A, B, C: A or (not B) or C

    original_b = lambda A, B: ((not A) and B) or (A and (not B))
    simple_b = lambda A, B: A != B

    original_c = lambda A, B, C: (A or B) and ((not A) or C)
    simple_c = lambda A, B, C: (A and C) or ((not A) and B)

    original_d = lambda A, B, C: (A or B) and (A or C) and (B or C)
    simple_d = lambda A, B, C: (A and B) or (A and C) or (B and C)

    answers = [
        {
            "label": "1A",
            "original": "(A'BC')' + A(B' + C)",
            "steps": [
                "= A + B' + C + AB' + AC   (De Morgan and distribution)",
                "= A + B' + C   (absorption)",
            ],
            "simplified": "A + B' + C",
            "variables": 3,
            "original_function": original_a,
            "simple_function": simple_a,
        },
        {
            "label": "1B",
            "original": "A'B + AB'",
            "steps": ["= A XOR B"],
            "simplified": "A ⊕ B",
            "variables": 2,
            "original_function": original_b,
            "simple_function": simple_b,
        },
        {
            "label": "1C",
            "original": "(A + B)(A' + C)",
            "steps": [
                "= AA' + AC + A'B + BC",
                "= AC + A'B + BC",
                "= AC + A'B   (consensus theorem)",
            ],
            "simplified": "AC + A'B",
            "variables": 3,
            "original_function": original_c,
            "simple_function": simple_c,
        },
        {
            "label": "1D",
            "original": "(A + B)(A + C)(B + C)",
            "steps": [
                "= (A + BC)(B + C)",
                "= AB + AC + BC",
            ],
            "simplified": "AB + AC + BC",
            "variables": 3,
            "original_function": original_d,
            "simple_function": simple_d,
        },
    ]

    for answer in answers:
        valid, failed_values = expressions_match(
            answer["variables"],
            answer["original_function"],
            answer["simple_function"],
        )
        answer["verified"] = valid
        answer["failed_values"] = failed_values
        print(f"\n{answer['label']}: {answer['original']}")
        for step in answer["steps"]:
            print(step)
        print("Final answer:", answer["simplified"])
        print("Verified with every input:", valid)

    return answers


def problem_2_prove_equivalence():
    """Problem 2: prove the stated equivalence with algebra and a truth table."""
    left = lambda A, B, C: (A or B) and ((not A) or C)
    right = lambda A, B, C: (A and C) or ((not A) and B)
    valid, failed_values = expressions_match(3, left, right)

    headers = ["A", "B", "C", "Left", "Right", "Match"]
    rows = []
    for A, B, C in product([0, 1], repeat=3):
        left_value = bit(left(bool(A), bool(B), bool(C)))
        right_value = bit(right(bool(A), bool(B), bool(C)))
        rows.append((A, B, C, left_value, right_value,
                     "YES" if left_value == right_value else "NO"))

    print_table("Problem 2: Equivalence proof", headers, rows)
    print("Algebra: (A+B)(A'+C) = AA' + AC + A'B + BC = AC + A'B")
    print("Equivalent:", valid)
    save_csv("problem_2_equivalence.csv", headers, rows)
    return {
        "verified": valid,
        "failed_values": failed_values,
        "headers": headers,
        "rows": rows,
        "steps": "(A+B)(A'+C) = AA' + AC + A'B + BC = AC + A'B",
    }


def problem_3_nand_only():
    """Problem 3: implement F = AB' + A'C with only NAND gates."""

    def nand_circuit(A, B, C):
        not_b = nand(B, B)          # B'
        not_a = nand(A, A)          # A'
        product_1_bar = nand(A, not_b)   # (AB')'
        product_2_bar = nand(not_a, C)   # (A'C)'
        return nand(product_1_bar, product_2_bar)

    direct_function = lambda A, B, C: (
        (A and (not B)) or ((not A) and C)
    )

    headers = ["A", "B", "C", "NAND F", "Expected F", "Match"]
    rows = []
    for A, B, C in product([0, 1], repeat=3):
        nand_value = bit(nand_circuit(bool(A), bool(B), bool(C)))
        expected = bit(direct_function(bool(A), bool(B), bool(C)))
        rows.append((A, B, C, nand_value, expected,
                     "YES" if nand_value == expected else "NO"))

    print_table("Problem 3: NAND-only implementation", headers, rows)
    save_csv("problem_3_nand_only.csv", headers, rows)
    return {
        "headers": headers,
        "rows": rows,
        "verified": all(row[-1] == "YES" for row in rows),
        "steps": [
            "B' = NAND(B, B)",
            "A' = NAND(A, A)",
            "X = NAND(A, B') = (AB')'",
            "Y = NAND(A', C) = (A'C)'",
            "F = NAND(X, Y) = AB' + A'C",
        ],
    }


def problem_4_simplify_given_truth_table():
    """Problem 4: simplify the supplied truth table."""
    supplied_outputs = [1, 0, 0, 1, 0, 1, 1, 1]
    simplified = lambda A, B, C: (
        ((not A) and (not B) and (not C))
        or (A and B)
        or (A and C)
        or (B and C)
    )

    headers = ["A", "B", "C", "Given F", "Simplified F", "Match"]
    rows = []
    for index, values in enumerate(product([0, 1], repeat=3)):
        A, B, C = values
        calculated = bit(simplified(bool(A), bool(B), bool(C)))
        given = supplied_outputs[index]
        rows.append((A, B, C, given, calculated,
                     "YES" if given == calculated else "NO"))

    print_table("Problem 4: Simplified supplied truth table", headers, rows)
    print("Final answer: F = A'B'C' + AB + AC + BC")
    save_csv("problem_4_simplified_table.csv", headers, rows)
    return {
        "headers": headers,
        "rows": rows,
        "expression": "F = A'B'C' + AB + AC + BC",
        "verified": all(row[-1] == "YES" for row in rows),
    }


def problem_5_logic_circuit_svg():
    """Problem 5: return an SVG circuit for F = A'B'C' + AB + AC + BC."""
    return """
    <svg viewBox="0 0 1050 560" role="img" aria-label="Logic circuit">
      <style>
        .wire{stroke:#607d8b;stroke-width:4;fill:none}
        .gate{fill:#e3f0f8;stroke:#245b7a;stroke-width:3}
        .final{fill:#e3f4df;stroke:#2b7a3f;stroke-width:3}
        .label{font:22px Arial;fill:#173b57;font-weight:bold}
        .small{font:19px Arial;fill:#263238}
      </style>
      <text x="25" y="35" class="label">F = A'B'C' + AB + AC + BC</text>
      <text x="25" y="85" class="label">Available inputs</text>
      <text x="40" y="135" class="small">A, A', B, B', C, C'</text>
      <rect x="300" y="70" width="330" height="75" rx="15" class="gate"/>
      <text x="330" y="117" class="label">AND: A' · B' · C'</text>
      <rect x="300" y="180" width="330" height="75" rx="15" class="gate"/>
      <text x="365" y="227" class="label">AND: A · B</text>
      <rect x="300" y="290" width="330" height="75" rx="15" class="gate"/>
      <text x="365" y="337" class="label">AND: A · C</text>
      <rect x="300" y="400" width="330" height="75" rx="15" class="gate"/>
      <text x="365" y="447" class="label">AND: B · C</text>
      <path d="M630 108 H735 V270 H790" class="wire"/>
      <path d="M630 218 H735 V270" class="wire"/>
      <path d="M630 328 H735 V270" class="wire"/>
      <path d="M630 438 H735 V270" class="wire"/>
      <rect x="790" y="215" width="150" height="110" rx="22" class="final"/>
      <text x="840" y="280" class="label">OR</text>
      <path d="M940 270 H1010" class="wire"/>
      <text x="1018" y="278" class="label">F</text>
      <text x="25" y="525" class="small">Make A', B', and C' with NOT gates. The four AND outputs enter one OR gate.</text>
    </svg>
    """


def problem_6_truth_tables():
    """Problem 6: create the two requested three-variable truth tables."""
    expression_a = lambda A, B, C: (
        (A or (not B)) and ((not A) or C)
    )
    minterms = {0, 1, 2, 4, 7}
    expression_b = lambda A, B, C: (
        (4 * bit(A) + 2 * bit(B) + bit(C)) in minterms
    )

    headers_a, rows_a = make_truth_table(["A", "B", "C"], expression_a)
    headers_b, rows_b = make_truth_table(["A", "B", "C"], expression_b)
    print_table("Problem 6A: (A OR B') AND (A' OR C)", headers_a, rows_a)
    print_table("Problem 6B: Σ(0, 1, 2, 4, 7)", headers_b, rows_b)
    save_csv("problem_6a_truth_table.csv", headers_a, rows_a)
    save_csv("problem_6b_truth_table.csv", headers_b, rows_b)
    return [
        ("6A: (A OR B') AND (A' OR C)", headers_a, rows_a),
        ("6B: Σ(0, 1, 2, 4, 7)", headers_b, rows_b),
    ]


def problem_7_truth_tables():
    """Problem 7: create all five requested truth tables."""
    problems = [
        ("7A: A AND B", ["A", "B"], lambda A, B: A and B),
        ("7B: A OR B", ["A", "B"], lambda A, B: A or B),
        ("7C: NOT A", ["A", "B"], lambda A, B: not A),
        ("7D: A'B + AB' (XOR)", ["A", "B"],
         lambda A, B: ((not A) and B) or (A and (not B))),
        ("7E: A'BC + AB'C' + ABC", ["A", "B", "C"],
         lambda A, B, C: (
             ((not A) and B and C)
             or (A and (not B) and (not C))
             or (A and B and C)
         )),
    ]

    results = []
    for index, (title, variables, function) in enumerate(problems, start=1):
        headers, rows = make_truth_table(variables, function)
        print_table(title, headers, rows)
        save_csv(f"problem_7_{index}.csv", headers, rows)
        results.append((title, headers, rows))
    return results


def table_html(title, headers, rows):
    """Create a colored HTML truth table."""
    header_cells = "".join(f"<th>{escape(str(value))}</th>" for value in headers)
    body_rows = []
    for row in rows:
        cells = []
        for column_index, value in enumerate(row):
            class_name = ""
            if column_index == len(row) - 1 and value in (0, 1):
                class_name = " class='one'" if value == 1 else " class='zero'"
            elif value == "YES":
                class_name = " class='match'"
            elif value == "NO":
                class_name = " class='nomatch'"
            cells.append(f"<td{class_name}>{escape(str(value))}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<section><h2>{escape(title)}</h2><table><thead><tr>{header_cells}</tr></thead><tbody>{''.join(body_rows)}</tbody></table></section>"


def create_html_report(problem_1, problem_2, problem_3, problem_4,
                       problem_6, problem_7):
    """Create the browser-based visual report."""
    simplification_cards = []
    for answer in problem_1:
        steps = "<br>".join(escape(step) for step in answer["steps"])
        status = "Verified ✓" if answer["verified"] else "Check failed"
        simplification_cards.append(
            f"<div class='card'><h3>{answer['label']}: {escape(answer['original'])}</h3>"
            f"<p>{steps}</p><p><strong>Final: {escape(answer['simplified'])}</strong></p>"
            f"<span class='badge'>{status}</span></div>"
        )

    sections = [
        "<section><h2>Problem 1: Simplifications</h2><div class='cards'>"
        + "".join(simplification_cards) + "</div></section>",
        table_html("Problem 2: Equivalence verification",
                   problem_2["headers"], problem_2["rows"]),
        "<section><h2>Problem 3: NAND-only circuit</h2><ol>"
        + "".join(f"<li>{escape(step)}</li>" for step in problem_3["steps"])
        + "</ol>" + nand_svg() + "</section>",
        table_html("Problem 3: NAND verification",
                   problem_3["headers"], problem_3["rows"]),
        table_html("Problem 4: Supplied table vs. simplified expression",
                   problem_4["headers"], problem_4["rows"]),
        "<section><h2>Problem 5: Logic circuit</h2>"
        + problem_5_logic_circuit_svg() + "</section>",
    ]
    for title, headers, rows in problem_6 + problem_7:
        sections.append(table_html(title, headers, rows))

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CS 505 Boolean Algebra Visual Report</title>
<style>
body{{font-family:Arial,sans-serif;margin:0;background:#f4f7fa;color:#16232e}}
header{{background:#173b57;color:white;padding:28px 5%;}}
main{{max-width:1100px;margin:auto;padding:24px}}
section{{background:white;margin:20px 0;padding:22px;border-radius:14px;box-shadow:0 2px 9px #ccd5dc}}
h1,h2,h3{{color:#173b57}}
header h1{{color:white;margin:0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}}
.card{{background:#eef5fa;border-left:6px solid #2f6d93;padding:14px;border-radius:8px}}
.badge{{display:inline-block;background:#dff3e4;color:#1f6a37;padding:5px 9px;border-radius:12px;font-weight:bold}}
table{{border-collapse:collapse;width:100%;max-width:720px;margin:12px auto}}
th,td{{border:1px solid #9fb0bd;padding:8px;text-align:center}}
th{{background:#245b7a;color:white}}
.one,.match{{background:#dff3e4;font-weight:bold}}
.zero{{background:#f7e8e8}}
.nomatch{{background:#ffd5d5;font-weight:bold}}
svg{{width:100%;max-width:1000px;height:auto;background:#fbfdff;border:1px solid #d2dce3;border-radius:10px}}
footer{{padding:25px;text-align:center;color:#566875}}
</style>
</head>
<body>
<header><h1>CS 505 Module Seven: Boolean Algebra</h1><p>Calculated and visualized with Python</p></header>
<main>{''.join(sections)}</main>
<footer>Generated by boolean_algebra_pycharm.py</footer>
</body></html>"""
    report_path = OUTPUT_FOLDER / "boolean_algebra_report.html"
    report_path.write_text(html, encoding="utf-8")
    return report_path


def nand_svg():
    """Return a simple visual of the five NAND gates used in Problem 3."""
    return """
    <svg viewBox="0 0 1050 450" role="img" aria-label="NAND-only circuit">
      <style>
        .g{fill:#f3e8ff;stroke:#6a3d8f;stroke-width:3}
        .w{stroke:#667985;stroke-width:4;fill:none}
        .t{font:21px Arial;fill:#2d1740;font-weight:bold}
        .s{font:18px Arial;fill:#263238}
      </style>
      <text x="25" y="35" class="t">Five-NAND implementation of F = AB' + A'C</text>
      <rect x="60" y="80" width="190" height="70" rx="14" class="g"/>
      <text x="92" y="123" class="t">NAND(B,B)</text><text x="270" y="123" class="t">= B'</text>
      <rect x="60" y="190" width="190" height="70" rx="14" class="g"/>
      <text x="92" y="233" class="t">NAND(A,A)</text><text x="270" y="233" class="t">= A'</text>
      <rect x="400" y="80" width="220" height="70" rx="14" class="g"/>
      <text x="430" y="123" class="t">NAND(A,B')</text>
      <rect x="400" y="250" width="220" height="70" rx="14" class="g"/>
      <text x="425" y="293" class="t">NAND(A',C)</text>
      <path d="M620 115 H720 V205 H770" class="w"/>
      <path d="M620 285 H720 V205" class="w"/>
      <rect x="770" y="160" width="220" height="90" rx="16" class="g"/>
      <text x="810" y="213" class="t">Final NAND</text>
      <text x="810" y="285" class="s">Output = F</text>
      <text x="60" y="400" class="s">The last NAND applies De Morgan's law and changes the two complemented products into an OR.</text>
    </svg>
    """


def main():
    """Run every problem and build all output files."""
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    print("CS 505 Boolean Algebra Solver")
    print("Output folder:", OUTPUT_FOLDER)

    answer_1 = problem_1_simplify_expressions()
    answer_2 = problem_2_prove_equivalence()
    answer_3 = problem_3_nand_only()
    answer_4 = problem_4_simplify_given_truth_table()
    answer_6 = problem_6_truth_tables()
    answer_7 = problem_7_truth_tables()

    report = create_html_report(
        answer_1, answer_2, answer_3, answer_4, answer_6, answer_7
    )
    # These optional packages make polished PNG charts. The main assignment
    # still works without them.
    from package_visuals import create_boolean_package_visuals
    create_boolean_package_visuals(OUTPUT_FOLDER)
    print("\nFinished.")
    print("Open this visual report in a browser:")
    print(report)


if __name__ == "__main__":
    main()
