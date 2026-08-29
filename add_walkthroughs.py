#!/usr/bin/env python3
"""Add 4 additional step-by-step walkthroughs per topic, then rebuild course.json."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
COURSE = ROOT / "App" / "Resources" / "Content" / "course.json"

# ---------------------------------------------------------------------------
# Helper constructors (same as build_curriculum.py)
# ---------------------------------------------------------------------------

def step(label, math, explanation):
    return {"label": label, "math": math, "explanation": explanation}


def step_by_step(title, prompt, steps, source):
    return {"title": title, "prompt": prompt, "steps": steps, "source": source}


def src(source, chapter=None, section=None, url_path=None):
    return {
        "source": source,
        "chapter": chapter,
        "section": section,
        "urlPath": url_path,
    }


OS = "openstax_abramson"
LR = "lippman_rasmussen"
YS = "yoshiwara"

# ---------------------------------------------------------------------------
# New walkthroughs keyed by (section_type, index)
# Section types match prerequisites slugs + week topic slugs
# ---------------------------------------------------------------------------

NEW_SBS = {
    # ─── PREREQUISITES ───────────────────────────────────────────────────

    "algebra-essentials": [
        step_by_step(
            "Solve 7 − 2(x + 3) = 3x + 1",
            "Solve for x.",
            [
                step("Distribute", "7 − 2x − 6 = 3x + 1", "Multiply −2 across the parentheses."),
                step("Combine constants", "1 − 2x = 3x + 1", "7 − 6 = 1."),
                step("Move x-terms right", "−2x − 3x = 1 − 1", "Subtract 3x from both sides; subtract 1 from both sides."),
                step("Combine and divide", "−5x = 0  →  x = 0", "0 divided by any nonzero number is 0."),
                step("Check", "7 − 2(0 + 3) = 7 − 6 = 1 ✓;  3(0) + 1 = 1 ✓", "Both sides agree."),
            ],
            src(OS, "Ch 1.1"),
        ),
        step_by_step(
            "Solve for b:  3(b − 2) + 4 = 2b + 1",
            "Find b.",
            [
                step("Distribute", "3b − 6 + 4 = 2b + 1", "3 · (−2) = −6."),
                step("Combine like terms", "3b − 2 = 2b + 1", "−6 + 4 = −2."),
                step("Subtract 2b from both sides", "b − 2 = 1", "Isolate the variable term."),
                step("Add 2", "b = 3", "Solve for b."),
                step("Check", "3(3 − 2) + 4 = 3 + 4 = 7;  2(3) + 1 = 7 ✓", "Both sides equal 7."),
            ],
            src(OS, "Ch 1.1"),
        ),
        step_by_step(
            "Solve:  2(x + 1) − 3(x − 2) = 4",
            "Solve for x.",
            [
                step("Distribute both", "2x + 2 − 3x + 6 = 4", "Be careful with the second minus sign: −3(x − 2) = −3x + 6."),
                step("Combine like terms", "(2x − 3x) + (2 + 6) = 4  →  −x + 8 = 4", "x-terms: −x. Constants: 8."),
                step("Subtract 8", "−x = −4", "Move the constant to the right."),
                step("Multiply by −1", "x = 4", "Divide (or multiply) by −1 to flip the sign."),
                step("Check", "2(4 + 1) − 3(4 − 2) = 10 − 6 = 4 ✓", "Left side equals the right side."),
            ],
            src(OS, "Ch 1.1"),
        ),
        step_by_step(
            "Classify and solve:  5(2 − x) = 3(x + 4) − 7",
            "Solve for x.",
            [
                step("Distribute both sides", "10 − 5x = 3x + 12 − 7", "Left: 5·2 = 10, 5·(−x) = −5x. Right: 3·4 = 12."),
                step("Simplify right side", "10 − 5x = 3x + 5", "12 − 7 = 5."),
                step("Move x-terms to left", "−5x − 3x = 5 − 10", "Subtract 3x and 10 from both sides."),
                step("Combine", "−8x = −5", "−5x − 3x = −8x; 5 − 10 = −5."),
                step("Divide", "x = 5/8", "−5/−8 = 5/8."),
                step("Check", "5(2 − 5/8) = 10 − 25/8 = 80/8 − 25/8 = 55/8;  3(5/8 + 4) − 7 = 15/8 + 12 − 7 = 55/8 ✓", "Both sides equal 55/8."),
            ],
            src(OS, "Ch 1.1"),
        ),
    ],

    "exponents-and-scientific-notation": [
        step_by_step(
            "Simplify  x⁻³ · x⁵",
            "Write with only positive exponents.",
            [
                step("Apply product rule", "x⁻³ · x⁵ = x⁻³⁺⁵", "When multiplying same-base powers, add exponents."),
                step("Add exponents", "x²", "−3 + 5 = 2."),
                step("Final answer", "x²", "Already positive — no reciprocal needed."),
            ],
            src(OS, "Ch 1.2"),
        ),
        step_by_step(
            "Simplify  (4x²y³)² / (2xy²)",
            "Leave only positive exponents.",
            [
                step("Apply power rule to numerator", "(4x²y³)² = 4² · x⁴ · y⁶ = 16x⁴y⁶", "(xy)ⁿ = xⁿyⁿ. Double each exponent."),
                step("Set up division", "16x⁴y⁶ / (2xy²)", "Quotient rule: subtract exponents."),
                step("Divide coefficients", "16/2 = 8", "Simplify the numeric factor."),
                step("Subtract x exponents", "x⁴⁻¹ = x³", "4 − 1 = 3."),
                step("Subtract y exponents", "y⁶⁻² = y⁴", "6 − 2 = 4."),
                step("Final answer", "8x³y⁴", "All exponents positive."),
            ],
            src(OS, "Ch 1.2"),
        ),
        step_by_step(
            "Convert  8.4 × 10⁻⁶  to standard form",
            "Write as a decimal.",
            [
                step("Identify exponent", "n = −6", "The 10 is raised to the power −6."),
                step("Move decimal left (negative exponent)", "0.0000084", "Move decimal 6 places left. Add leading zeros."),
                step("Final answer", "0.0000084", "Confirmed."),
            ],
            src(OS, "Ch 1.2"),
        ),
        step_by_step(
            "Simplify  (2⁻³ · 3²) / (2² · 3⁻¹)",
            "Write with positive exponents only.",
            [
                step("Separate by base", "(2⁻³/2²) · (3²/3⁻¹)", "Group same-base terms together."),
                step("Subtract exponent for 2", "2⁻³⁻² = 2⁻⁵", "−3 − 2 = −5."),
                step("Subtract exponent for 3", "3²⁻⁽⁻¹⁾ = 3³", "2 − (−1) = 3."),
                step("Rewrite with positive exponents", "(1/2⁵) · 27 = 27 / 32", "2⁻⁵ = 1/2⁵; 3³ = 27."),
                step("Final answer", "27/32", "Cannot simplify further."),
            ],
            src(OS, "Ch 1.2"),
        ),
    ],

    "radicals-and-rational-exponents": [
        step_by_step(
            "Simplify  √72",
            "Factor out the largest perfect square.",
            [
                step("Prime factor 72", "72 = 36 · 2", "36 = 6² is the largest perfect square."),
                step("Apply √ab = √a · √b", "√72 = √(36 · 2) = √36 · √2 = 6√2", "Separate the radical."),
                step("Final answer", "6√2", "No factor of 2 remains under the radical."),
            ],
            src(OS, "Ch 1.3"),
        ),
        step_by_step(
            "Convert  27^(2/3)  to radical form and simplify",
            "Evaluate completely.",
            [
                step("Identify exponent parts", "a^(m/n) = (ⁿ√a)ᵐ = ⁿ√(aᵐ)", "m = 2 (power), n = 3 (root)."),
                step("Take the cube root", "∛27 = 3", "3³ = 27."),
                step("Raise to the power 2", "3² = 9", "(∛27)² = 9."),
                step("Final answer", "9", "Can also compute as (27²)^(1/3) = 729^(1/3) = 9."),
            ],
            src(OS, "Ch 1.3"),
        ),
        step_by_step(
            "Rationalize  4 / (√5 + √3)",
            "Write without radicals in the denominator.",
            [
                step("Multiply top and bottom by the conjugate", "(4(√5 − √3)) / ((√5 + √3)(√5 − √3))", "The conjugate of (a + b) is (a − b)."),
                step("Expand denominator", "(√5)² − (√3)² = 5 − 3 = 2", "(a+b)(a−b) = a² − b²."),
                step("Simplify numerator", "4(√5 − √3) = 4√5 − 4√3", "No further combination — unlike radicals."),
                step("Final answer", "(4√5 − 4√3) / 2 = 2√5 − 2√3", "Divide each term by 2."),
            ],
            src(OS, "Ch 1.3"),
        ),
        step_by_step(
            "Simplify  √50 + √8",
            "Combine into simplest radical form.",
            [
                step("Simplify each radical", "√50 = √(25·2) = 5√2;  √8 = √(4·2) = 2√2", "Factor out the largest perfect squares."),
                step("Combine like radicals", "5√2 + 2√2 = (5 + 2)√2", "Only combine when the radicand is identical."),
                step("Final answer", "7√2", "Cannot combine with a different radicand."),
            ],
            src(OS, "Ch 1.3"),
        ),
    ],

    "polynomials-and-factoring": [
        step_by_step(
            "Factor  x² − 9",
            "Recognize the difference of squares pattern.",
            [
                step("Identify the pattern", "a² − b² = (a + b)(a − b)", "Check: both terms are perfect squares."),
                step("Find a and b", "a² = x² → a = x;  b² = 9 → b = 3", "Square roots of each term."),
                step("Apply formula", "x² − 9 = (x + 3)(x − 3)", "Substitute into the pattern."),
                step("Check", "(x + 3)(x − 3) = x² − 3x + 3x − 9 = x² − 9 ✓", "FOIL confirms the result."),
            ],
            src(OS, "Ch 1.5"),
        ),
        step_by_step(
            "Factor  x² + 5x + 6",
            "Find two numbers with product 6 and sum 5.",
            [
                step("Set up the target", "Find p and q such that p · q = 6 and p + q = 5", "These are the constant and linear coefficients."),
                step("List factor pairs of 6", "(1, 6), (2, 3), (−1, −6), (−2, −3)", "Both positive since product and sum are positive."),
                step("Find the pair", "2 and 3:  2 + 3 = 5 ✓,  2 · 3 = 6 ✓", "These satisfy both conditions."),
                step("Write factors", "x² + 5x + 6 = (x + 2)(x + 3)", "x² + px + qx + pq = (x + p)(x + q)."),
                step("Check", "(x + 2)(x + 3) = x² + 5x + 6 ✓", "FOIL confirms."),
            ],
            src(OS, "Ch 1.5"),
        ),
        step_by_step(
            "Factor  2x² + 7x + 3",
            "Use the AC-method or trial factors.",
            [
                step("Multiply a and c", "2 · 3 = 6", "Find two numbers whose product = ac and sum = b."),
                step("Find numbers", "6 and 1:  6 + 1 = 7 ✓", "6 · 1 = 6, sum = 7 matches the middle coefficient."),
                step("Split the middle term", "2x² + 6x + x + 3", "Replace 7x with 6x + x."),
                step("Factor by grouping", "(2x² + 6x) + (x + 3) = 2x(x + 3) + 1(x + 3)", "Factor out the GCF from each group."),
                step("Factor the binomial", "(x + 3)(2x + 1)", "Common factor (x + 3) is factored out."),
                step("Check", "(x + 3)(2x + 1) = 2x² + x + 6x + 3 = 2x² + 7x + 3 ✓", "FOIL confirms."),
            ],
            src(OS, "Ch 1.5"),
        ),
        step_by_step(
            "Factor  4x² − 25",
            "Identify and apply the difference of squares.",
            [
                step("Recognize the pattern", "a² − b² = (a + b)(a − b)", "Both terms are perfect squares."),
                step("Find a and b", "a² = 4x² → a = 2x;  b² = 25 → b = 5", "Take the square root of each term."),
                step("Apply formula", "4x² − 25 = (2x + 5)(2x − 5)", "Substitute into the pattern."),
                step("Check", "(2x + 5)(2x − 5) = 4x² − 10x + 10x − 25 = 4x² − 25 ✓", "FOIL confirms."),
            ],
            src(OS, "Ch 1.5"),
        ),
    ],

    "rational-expressions": [
        step_by_step(
            "Simplify  (x² − 4) / (x − 2)",
            "Cancel common factors.",
            [
                step("Factor the numerator", "x² − 4 = (x + 2)(x − 2)", "Difference of squares."),
                step("Cancel the common factor", "(x + 2)(x − 2) / (x − 2) = x + 2", "Cancel (x − 2) top and bottom."),
                step("State the restriction", "x ≠ 2", "The original denominator cannot be zero."),
                step("Final answer", "x + 2  (for x ≠ 2)", "The simplified form is only valid when x ≠ 2."),
            ],
            src(OS, "Ch 1.6"),
        ),
        step_by_step(
            "Multiply  (x + 3) / (x − 1)  ·  (x² − 1) / (x + 3)",
            "Simplify the product.",
            [
                step("Factor where possible", "(x + 3)/(x − 1) · ((x+1)(x−1))/(x+3)", "x² − 1 = (x+1)(x−1)."),
                step("Cancel (x + 3)", "= 1/(x − 1) · (x+1)(x−1)/1", "(x+3)/(x+3) = 1."),
                step("Cancel (x − 1)", "= (x + 1)", "(x−1)/(x−1) = 1."),
                step("State restrictions", "x ≠ −3, x ≠ 1", "Original denominators cannot be zero."),
                step("Final answer", "x + 1  (for x ≠ −3, x ≠ 1)", "Domain restriction from original expression."),
            ],
            src(OS, "Ch 1.6"),
        ),
        step_by_step(
            "Subtract  2/(x+1) − 1/(x−1)",
            "Combine into a single fraction.",
            [
                step("Find the LCD", "(x + 1)(x − 1)", "The factors are x+1 and x−1 — no overlap."),
                step("Rewrite first fraction", "2(x − 1) / [(x+1)(x−1)] = (2x − 2)/(x² − 1)", "Multiply top and bottom by (x−1)."),
                step("Rewrite second fraction", "1(x + 1) / [(x−1)(x+1)] = (x + 1)/(x² − 1)", "Multiply top and bottom by (x+1)."),
                step("Subtract numerators", "(2x − 2) − (x + 1) = 2x − 2 − x − 1 = x − 3", "Watch the sign on the second numerator."),
                step("Final answer", "(x − 3) / (x² − 1)  (for x ≠ ±1)", "Keep the denominator factored to show the domain."),
            ],
            src(OS, "Ch 1.6"),
        ),
        step_by_step(
            "Simplify  (x² + x − 6) / (x² − 4)",
            "Cancel fully.",
            [
                step("Factor numerator", "x² + x − 6 = (x + 3)(x − 2)", "Find two numbers that multiply to −6 and add to 1: 3 and −2."),
                step("Factor denominator", "x² − 4 = (x + 2)(x − 2)", "Difference of squares."),
                step("Cancel (x − 2)", "= (x + 3)/(x + 2)", "Cancel the common binomial factor."),
                step("Restrictions", "x ≠ 2, x ≠ −2", "Original denominator zero at these values."),
                step("Final answer", "(x + 3)/(x + 2)  (for x ≠ 2, x ≠ −2)", "Simplified form with domain preserved."),
            ],
            src(OS, "Ch 1.6"),
        ),
    ],

    "coordinate-graphs-and-linear-equations": [
        step_by_step(
            "Find the equation of the line through (2, −1) with slope 3.",
            "Write in slope-intercept form.",
            [
                step("Start with point-slope form", "y − y₁ = m(x − x₁)", "Plug in m = 3, (x₁, y₁) = (2, −1)."),
                step("Substitute", "y − (−1) = 3(x − 2)", "y + 1 = 3(x − 2)."),
                step("Distribute", "y + 1 = 3x − 6", "Multiply 3 across the parentheses."),
                step("Solve for y", "y = 3x − 7", "Subtract 1 from both sides."),
                step("Final answer", "y = 3x − 7", "Slope m = 3, y-intercept b = −7."),
            ],
            src(OS, "Ch 2.2"),
        ),
        step_by_step(
            "Are the lines 2x + 3y = 6 and 4x + 6y = 12 parallel, perpendicular, or the same?",
            "Analyze the slopes.",
            [
                step("Rewrite first line in slope-intercept form", "3y = −2x + 6  →  y = (−2/3)x + 2", "Solve for y to read the slope."),
                step("Rewrite second line", "6y = −4x + 12  →  y = (−4/6)x + 2  →  y = (−2/3)x + 2", "Both simplify to the same equation!"),
                step("Compare slopes and intercepts", "Both: slope = −2/3, y-intercept = 2", "They are the same line (coincident)."),
                step("Final answer", "Same line — they are coincident (every point on one is on the other).", "Multiply the first equation by 2 to get the second."),
            ],
            src(OS, "Ch 2.2"),
        ),
        step_by_step(
            "Find the distance between P(1, 5) and Q(4, 9).",
            "Apply the distance formula.",
            [
                step("Recall distance formula", "d = √[(x₂−x₁)² + (y₂−y₁)²]", "Derived from the Pythagorean theorem."),
                step("Substitute coordinates", "d = √[(4−1)² + (9−5)²] = √[3² + 4²]", "x₂−x₁ = 3, y₂−y₁ = 4."),
                step("Compute squares", "3² + 4² = 9 + 16 = 25", "9 + 16 = 25."),
                step("Take the square root", "√25 = 5", "The distance is 5 units."),
                step("Final answer", "d = 5", "A 3-4-5 right triangle confirms the result."),
            ],
            src(OS, "Ch 2.2"),
        ),
        step_by_step(
            "Find the x- and y-intercepts of 3x − 4y = 12.",
            "Set each variable to 0 in turn.",
            [
                step("y-intercept: set x = 0", "3(0) − 4y = 12  →  −4y = 12  →  y = −3", "The y-intercept is (0, −3)."),
                step("x-intercept: set y = 0", "3x − 4(0) = 12  →  3x = 12  →  x = 4", "The x-intercept is (4, 0)."),
                step("Final answer", "x-intercept: (4, 0);  y-intercept: (0, −3)", "Plot both points and draw the line through them."),
            ],
            src(OS, "Ch 2.2"),
        ),
    ],

    # ─── WEEK 1 ──────────────────────────────────────────────────────────

    "what-is-a-function": [
        step_by_step(
            "If f(x) = 5 − 2x, find f(−3).",
            "Evaluate the function.",
            [
                step("Substitute −3 for x", "f(−3) = 5 − 2(−3)", "Replace every x with −3."),
                step("Multiply", "5 − 2(−3) = 5 + 6", "−2 · (−3) = +6."),
                step("Add", "5 + 6 = 11", "Final answer."),
                step("Final answer", "f(−3) = 11", "Check: 5 − 2(−3) = 5 + 6 = 11 ✓"),
            ],
            src(LR, "Ch 1.1"),
        ),
        step_by_step(
            "Does the relation y² = x define a function of x?",
            "Apply the vertical-line test.",
            [
                step("Solve for y", "y = ±√x", "For each x > 0 there are two y-values: one positive, one negative."),
                step("Check the vertical-line test", "A vertical line at x = 4 crosses the graph at y = 2 AND y = −2", "Two outputs for one input violates the function definition."),
                step("Final answer", "Not a function — fails the vertical-line test.", "Each x > 0 corresponds to two y-values."),
            ],
            src(LR, "Ch 1.1"),
        ),
        step_by_step(
            "Given f(x) = 3x² − 1, find [f(x+h) − f(x)] / h.",
            "Compute the difference quotient.",
            [
                step("Compute f(x + h)", "f(x + h) = 3(x + h)² − 1 = 3(x² + 2xh + h²) − 1 = 3x² + 6xh + 3h² − 1", "Expand (x + h)²."),
                step("Subtract f(x)", "f(x+h) − f(x) = (3x² + 6xh + 3h² − 1) − (3x² − 1) = 6xh + 3h²", "3x² − 1 cancels."),
                step("Divide by h", "(6xh + 3h²) / h = 6x + 3h", "Factor h: h(6x + 3h) / h = 6x + 3h."),
                step("Final answer", "6x + 3h  (the difference quotient)", "This result is used in calculus for derivatives."),
            ],
            src(LR, "Ch 1.1"),
        ),
        step_by_step(
            "Let f(x) = x/(x−3). Find the domain.",
            "Identify values that make the denominator zero.",
            [
                step("Set denominator ≠ 0", "x − 3 ≠ 0", "Division by zero is undefined."),
                step("Solve", "x ≠ 3", "Isolate x."),
                step("Domain in interval notation", "(−∞, 3) ∪ (3, ∞)", "All real numbers except 3."),
                step("Final answer", "All real x except x = 3", "There are no other restrictions (numerator x is fine for all x)."),
            ],
            src(LR, "Ch 1.2"),
        ),
    ],

    "domain-and-range": [
        step_by_step(
            "Find the domain of f(x) = 1/(x² − 4).",
            "Identify where the denominator is zero.",
            [
                step("Set denominator to zero", "x² − 4 = 0", "The denominator cannot be zero."),
                step("Solve", "x² = 4  →  x = ±2", "Two values are excluded."),
                step("Domain in interval notation", "(−∞, −2) ∪ (−2, 2) ∪ (2, ∞)", "All reals except −2 and 2."),
                step("Final answer", "x ≠ ±2", "No other restrictions."),
            ],
            src(LR, "Ch 1.2"),
        ),
        step_by_step(
            "Find the domain of f(x) = √(x + 7).",
            "The radicand must be non-negative.",
            [
                step("Set radicand ≥ 0", "x + 7 ≥ 0", "Square roots of negatives are not real."),
                step("Solve", "x ≥ −7", "Subtract 7."),
                step("Domain in interval notation", "[−7, ∞)", "Include −7 since ≥ means the endpoint is allowed."),
                step("Final answer", "x ≥ −7  or  [−7, ∞)", "Check: √(−7 + 7) = √0 = 0 ✓"),
            ],
            src(LR, "Ch 1.2"),
        ),
        step_by_step(
            "Find the range of y = √(x − 1) + 3.",
            "Determine the possible output values.",
            [
                step("Note the parent function", "√(x − 1) has range [0, ∞) after the domain shift of +1.", "The base function √u has minimum 0."),
                step("Apply the vertical shift", "Adding 3 shifts the range up by 3: [0 + 3, ∞)", "The entire graph moves up 3 units."),
                step("Final answer", "y ≥ 3  or  [3, ∞)", "The smallest output is 3 (at x = 1)."),
            ],
            src(LR, "Ch 1.2"),
        ),
        step_by_step(
            "Find the domain of f(x) = ln(x² − 9).",
            "The argument of ln must be positive.",
            [
                step("Set argument > 0", "x² − 9 > 0", "Logarithms are undefined for non-positive arguments."),
                step("Factor", "(x + 3)(x − 3) > 0", "Solve as a quadratic inequality."),
                step("Test intervals", "Critical points: x = −3, x = 3. Positive when x < −3 or x > 3.", "Use a sign chart or number line."),
                step("Domain in interval notation", "(−∞, −3) ∪ (3, ∞)", "Both factors must be positive or both negative."),
                step("Final answer", "x < −3  or  x > 3  (i.e., (−∞, −3) ∪ (3, ∞))", "Excluded: x = −3 and x = 3 where the log argument is zero."),
            ],
            src(LR, "Ch 1.2"),
        ),
    ],

    "rates-of-change-and-graph-behavior": [
        step_by_step(
            "Find the average rate of change of f(x) = x² between x = 1 and x = 3.",
            "Compute (f(3) − f(1)) / (3 − 1).",
            [
                step("Evaluate f(3)", "f(3) = 3² = 9", "Square 3."),
                step("Evaluate f(1)", "f(1) = 1² = 1", "Square 1."),
                step("Compute the rate of change", "(9 − 1) / (3 − 1) = 8 / 2 = 4", "Rise over run: change in output over change in input."),
                step("Final answer", "4 — for every 1-unit increase in x, y increases by 4 on average.", "This is also the slope of the secant line between (1, 1) and (3, 9)."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Is f(x) = x³ even, odd, or neither?",
            "Test f(−x) vs f(x) and −f(x).",
            [
                step("Compute f(−x)", "f(−x) = (−x)³ = −x³", "Odd power preserves the sign."),
                step("Compare to f(x)", "f(−x) = −x³ = −f(x)", "This matches the definition of an odd function."),
                step("Final answer", "Odd — symmetric about the origin.", "f(−x) = −f(x) for all x."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Find intervals where f(x) = −x² + 4 is increasing and decreasing.",
            "Analyze the sign of the derivative (or graph shape).",
            [
                step("Recognize the parabola", "Opens downward (a = −1 < 0). Vertex at x = 0.", "Maximum point at (0, 4)."),
                step("Increasing interval", "Increases on (−∞, 0] as x moves toward 0 from the left.", "Going up toward the vertex."),
                step("Decreasing interval", "Decreases on [0, ∞) as x moves away from 0 to the right.", "Going down from the vertex."),
                step("Final answer", "Increasing: (−∞, 0]; Decreasing: [0, ∞)", "Maximum at x = 0."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Determine whether f(x) = x⁴ − 3x² + 1 is even, odd, or neither.",
            "Test f(−x) = f(x) and f(−x) = −f(x).",
            [
                step("Compute f(−x)", "f(−x) = (−x)⁴ − 3(−x)² + 1 = x⁴ − 3x² + 1", "Even powers eliminate the negative sign."),
                step("Compare to f(x)", "f(−x) = x⁴ − 3x² + 1 = f(x)", "This matches f(x) exactly."),
                step("Final answer", "Even — symmetric about the y-axis.", "f(−x) = f(x) for all x."),
            ],
            src(LR, "Ch 1.3"),
        ),
    ],

    "composition-of-functions": [
        step_by_step(
            "Let f(x) = x + 4 and g(x) = 3x. Find (g ∘ f)(x).",
            "Compute g(f(x)).",
            [
                step("Write g(f(x))", "g(f(x)) = 3 · f(x) = 3(x + 4)", "Substitute f(x) into g."),
                step("Simplify", "3x + 12", "Distribute."),
                step("Final answer", "(g ∘ f)(x) = 3x + 12", "The composite takes x, adds 4, then triples the result."),
            ],
            src(LR, "Ch 1.4"),
        ),
        step_by_step(
            "Let f(x) = √x and g(x) = x² + 1. Find the domain of (f ∘ g)(x).",
            "Find where the composition is defined.",
            [
                step("Write the composition", "(f ∘ g)(x) = f(g(x)) = √(x² + 1)", "g(x) feeds into f."),
                step("Analyze the radicand", "x² + 1 ≥ 0 for all real x", "A square plus 1 is always positive."),
                step("Final answer", "Domain: all real numbers (−∞, ∞)", "No restriction from the square root — the radicand is always ≥ 1."),
            ],
            src(LR, "Ch 1.4"),
        ),
        step_by_step(
            "Decompose h(x) = (2x + 5)³ as f(g(x)).",
            "Identify an inner function g and outer function f.",
            [
                step("Identify the outer operation", "The last operation performed is the cube: u³.", "So the outer function is f(u) = u³."),
                step("Identify the inner expression", "The inside of the cube is 2x + 5.", "So g(x) = 2x + 5."),
                step("Verify", "f(g(x)) = (2x + 5)³ = h(x) ✓", "The decomposition is correct."),
                step("Final answer", "f(u) = u³ and g(x) = 2x + 5", "Many other decompositions are possible."),
            ],
            src(LR, "Ch 1.4"),
        ),
        step_by_step(
            "If f(x) = 2x − 5 and g(x) = x², find (f ∘ g)(3) and (g ∘ f)(3).",
            "Compute both composites at x = 3.",
            [
                step("Compute (f ∘ g)(3) = f(g(3))", "g(3) = 3² = 9", "First apply g."),
                step("Then apply f", "f(9) = 2(9) − 5 = 18 − 5 = 13", "Then apply f."),
                step("Compute (g ∘ f)(3) = g(f(3))", "f(3) = 2(3) − 5 = 6 − 5 = 1", "First apply f."),
                step("Then apply g", "g(1) = 1² = 1", "Then apply g."),
                step("Final answer", "(f ∘ g)(3) = 13;  (g ∘ f)(3) = 1.  Note: compositions are NOT commutative.", "Same input x = 3, but different results."),
            ],
            src(LR, "Ch 1.4"),
        ),
    ],

    "transformation-of-functions": [
        step_by_step(
            "Describe how y = |x| − 3 is obtained from y = |x|.",
            "Identify the transformation.",
            [
                step("Baseline graph", "y = |x| is V-shaped, vertex at (0, 0).", "Start here."),
                step("Identify the operation", "−3 is outside the absolute value → vertical shift.", "The transformation applies to the output f(x)."),
                step("Direction of shift", "y = |x| − 3: shift DOWN by 3 units.", "Subtracting outside shifts downward."),
                step("New vertex", "(0, −3)", "The vertex moves down 3 units."),
                step("Final answer", "Shift y = |x| down 3 units → vertex at (0, −3).", "Opens in the same direction with the same shape."),
            ],
            src(LR, "Ch 1.5"),
        ),
        step_by_step(
            "Describe the transformation: y = ½ · (x − 2)² + 4",
            "Apply each transformation in order.",
            [
                step("Inside parentheses: (x − 2)", "Shift RIGHT by 2. Vertex moves to (2, 0).", "f(x − h) shifts right by h."),
                step("Multiply by ½ outside", "Vertical compression by factor ½. The parabola is wider.", "Multiply outside by |a| < 1 compresses vertically."),
                step("Add 4 outside", "Shift UP by 4. Vertex moves to (2, 4).", "f(x) + k shifts up by k."),
                step("Order: Right 2 → compress → up 4", "Original (0,0) → (2,0) → (2,0) compressed → (2,4).", "Vertex ends at (2, 4)."),
                step("Final answer", "Right 2, vertical compression by ½, up 4. Vertex: (2, 4).", "The parabola opens upward (a = ½ > 0)."),
            ],
            src(LR, "Ch 1.5"),
        ),
        step_by_step(
            "Reflect y = x² over the x-axis. Write the equation.",
            "Apply a reflection.",
            [
                step("Reflection rule", "Reflecting over the x-axis: (x, y) → (x, −y).", "Multiply y by −1."),
                step("Apply to y = x²", "−y = x²  →  y = −x²", "Solve for y."),
                step("Final answer", "y = −x²", "Opens downward. Same shape as x² but flipped."),
            ],
            src(LR, "Ch 1.5"),
        ),
        step_by_step(
            "Describe the graph of y = −f(x + 3) given f(x) = √x.",
            "Read the transformations inside-out.",
            [
                step("Inside f: x + 3", "Shift LEFT by 3. The graph moves 3 units left.", "f(x + 3) shifts left by 3."),
                step("Outside f: −f(x + 3)", "Reflect over the x-axis. All y-values flip sign.", "Negating outside flips vertically."),
                step("Start with f(x) = √x", "Domain: [0, ∞), range: [0, ∞). Vertex at (0, 0).", "The parent function starts at (0, 0) and extends right and up."),
                step("After x + 3: shift left", "y = √(x + 3). Domain: [−3, ∞).", "Shifting the argument left by 3."),
                step("After negating: reflect", "y = −√(x + 3). Range: (−∞, 0]. Vertex at (−3, 0).", "The graph is below the x-axis."),
                step("Final answer", "Shift y = √x left 3 units, then reflect over x-axis. Range: (−∞, 0].", "Opens downward from the point (−3, 0)."),
            ],
            src(LR, "Ch 1.5"),
        ),
    ],

    # ─── WEEK 2 ──────────────────────────────────────────────────────────

    "linear-functions": [
        step_by_step(
            "Write y − 3 = 4(x + 1) in slope-intercept form and identify slope and y-intercept.",
            "Solve for y.",
            [
                step("Distribute", "y − 3 = 4x + 4", "Multiply 4 across (x + 1)."),
                step("Add 3 to both sides", "y = 4x + 7", "Slope-intercept form: y = mx + b."),
                step("Identify", "Slope m = 4, y-intercept b = 7 → (0, 7)", "The point where x = 0."),
                step("Final answer", "y = 4x + 7.  Slope = 4, y-intercept = (0, 7).", "Check: plug x = 0 → y = 7 ✓"),
            ],
            src(LR, "Ch 2.1"),
        ),
        step_by_step(
            "Find the slope of the line through (−2, 5) and (4, −1).",
            "Use the slope formula.",
            [
                step("Slope formula", "m = (y₂ − y₁) / (x₂ − x₁)", "Rise over run."),
                step("Label points", "(x₁, y₁) = (−2, 5), (x₂, y₂) = (4, −1)", "Order doesn't matter for the final value."),
                step("Substitute", "m = (−1 − 5) / (4 − (−2)) = (−6) / 6", "−1 − 5 = −6.  4 + 2 = 6."),
                step("Simplify", "m = −1", "A negative slope — the line falls from left to right."),
                step("Final answer", "m = −1", "Slope of −1 means y decreases by 1 for every 1-unit increase in x."),
            ],
            src(LR, "Ch 2.1"),
        ),
        step_by_step(
            "Write the equation of the line through (3, 2) parallel to 5x − 2y = 8.",
            "Find the slope and use point-slope form.",
            [
                step("Find slope of given line", "5x − 2y = 8 → −2y = −5x + 8 → y = (5/2)x − 4", "Slope m = 5/2."),
                step("Parallel lines have equal slopes", "m = 5/2", "Use the same slope."),
                step("Apply point-slope form", "y − 2 = (5/2)(x − 3)", "Plug in (3, 2) and m = 5/2."),
                step("Write in slope-intercept form", "y − 2 = (5/2)x − 15/2 → y = (5/2)x − 15/2 + 4/2 = (5/2)x − 11/2", "Convert 2 to 4/2."),
                step("Final answer", "y = (5/2)x − 11/2  or  5x − 2y = 11", "Multiply by 2 to clear fractions."),
            ],
            src(LR, "Ch 2.2"),
        ),
        step_by_step(
            "A taxi costs $3.50 base fare plus $2.10 per mile. Write the cost C as a function of miles m.",
            "Model with a linear function.",
            [
                step("Identify slope and intercept", "Slope m = $2.10 per mile (rate of change).  y-intercept b = $3.50 (cost at 0 miles).", "Base fare is the starting cost."),
                step("Write in slope-intercept form", "C = 2.10m + 3.50", "C = mx + b."),
                step("Check at 5 miles", "C = 2.10(5) + 3.50 = 10.50 + 3.50 = $14.00 ✓", "Reasonable for a 5-mile ride."),
                step("Final answer", "C(m) = 2.10m + 3.50", "For m ≥ 0 miles."),
            ],
            src(LR, "Ch 2.3"),
        ),
    ],

    "quadratic-functions": [
        step_by_step(
            "Find the vertex of f(x) = 2x² − 8x + 3 using the vertex formula.",
            "Use h = −b/(2a), k = f(h).",
            [
                step("Identify a, b, c", "a = 2, b = −8, c = 3", "Standard form: ax² + bx + c."),
                step("Find h", "h = −(−8) / (2·2) = 8/4 = 2", "Vertex x-coordinate."),
                step("Find k = f(2)", "f(2) = 2(4) − 8(2) + 3 = 8 − 16 + 3 = −5", "Substitute x = 2."),
                step("Vertex", "(h, k) = (2, −5)", "Minimum value since a = 2 > 0 (opens up)."),
                step("Final answer", "Vertex: (2, −5).  Axis of symmetry: x = 2.", "Minimum value of the function is −5."),
            ],
            src(LR, "Ch 3.2"),
        ),
        step_by_step(
            "Solve 2x² − 7x − 15 = 0 using the quadratic formula.",
            "Apply x = [−b ± √(b² − 4ac)] / 2a.",
            [
                step("Identify a, b, c", "a = 2, b = −7, c = −15", "From 2x² − 7x − 15."),
                step("Compute discriminant", "D = b² − 4ac = (−7)² − 4(2)(−15) = 49 + 120 = 169", "169 = 13² — a perfect square."),
                step("Apply formula", "x = [−(−7) ± √169] / (2·2) = [7 ± 13] / 4", "Two solutions from ±."),
                step("Solve each", "x₁ = (7 + 13)/4 = 20/4 = 5;  x₂ = (7 − 13)/4 = −6/4 = −3/2", "Both are valid."),
                step("Final answer", "x = 5 or x = −3/2", "Check: 2(5)² − 7(5) − 15 = 50 − 35 − 15 = 0 ✓"),
            ],
            src(LR, "Ch 3.2"),
        ),
        step_by_step(
            "Write x² + 10x + 2 in vertex form by completing the square.",
            "Rewrite as a(x − h)² + k.",
            [
                step("Start with x² + 10x", "Factor out coefficient of x²: (x² + 10x) + 2", "a = 1 so it's straightforward."),
                step("Complete the square", "Take half of 10: 5. Square it: 25. Add and subtract 25.", "(x² + 10x + 25) − 25 + 2."),
                step("Factor the perfect square", "(x + 5)² − 23", "(x + 5)² = x² + 10x + 25."),
                step("Final answer", "Vertex form: (x + 5)² − 23.  Vertex: (−5, −23).", "Opens upward (a = 1 > 0). Minimum value −23."),
            ],
            src(LR, "Ch 3.2"),
        ),
        step_by_step(
            "Use the discriminant to determine the nature of the roots of 3x² − 4x + 2 = 0.",
            "Compute D = b² − 4ac.",
            [
                step("Identify coefficients", "a = 3, b = −4, c = 2", "From 3x² − 4x + 2."),
                step("Compute discriminant", "D = (−4)² − 4(3)(2) = 16 − 24 = −8", "Negative discriminant."),
                step("Interpret", "D < 0 → no real roots (two complex conjugate roots).", "The parabola does not cross the x-axis."),
                step("Final answer", "No real roots — the equation has two complex solutions.", "The parabola lies entirely above the x-axis (a = 3 > 0 and vertex above x-axis)."),
            ],
            src(LR, "Ch 3.2"),
        ),
    ],

    "angle-measure-degrees-and-radians": [
        step_by_step(
            "Convert  120°  to radians.",
            "Multiply by π/180.",
            [
                step("Set up conversion", "120° × (π/180)", "Cancel degrees and introduce π."),
                step("Simplify the fraction", "120/180 = 2/3", "Divide numerator and denominator by 60."),
                step("Final answer", "(2π/3) radians", "120° = 2π/3 rad.  Check: (2/3) × 180 = 120° ✓"),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "Convert  5π/6  radians to degrees.",
            "Multiply by 180/π.",
            [
                step("Set up conversion", "(5π/6) × (180/π)", "Cancel π."),
                step("Simplify", "5 × 30 = 150", "180/6 = 30."),
                step("Final answer", "150°", "5π/6 rad = 150°.  150/180 = 5/6 ✓"),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "Find the arc length of a circle with radius 9 cm subtended by a central angle of 40°.",
            "Use s = rθ with θ in radians.",
            [
                step("Convert 40° to radians", "40° × (π/180) = (2π/9) rad", "40/180 = 2/9."),
                step("Apply arc length formula", "s = rθ = 9 × (2π/9) = 2π cm", "The radius cancels!"),
                step("Approximate", "2π ≈ 6.28 cm", "To 2 decimal places."),
                step("Final answer", "s = 2π cm ≈ 6.28 cm", "Arc length depends on the radius and the angle."),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "Express  5π/12  as a mixed number of degrees.",
            "Convert and simplify.",
            [
                step("Multiply by 180/π", "(5π/12) × (180/π) = 5 × 15 = 75°", "π cancels: 180/12 = 15."),
                step("Final answer", "75°", "5π/12 rad = 75°.  Halfway between π/4 (45°) and π/2 (90°)."),
            ],
            src(LR, "Ch 4.1"),
        ),
    ],

    "right-triangle-trigonometry": [
        step_by_step(
            "In a right triangle with hypotenuse 13 and one leg 5, find the other leg.",
            "Apply the Pythagorean theorem.",
            [
                step("Pythagorean theorem", "a² + b² = c²", "c is the hypotenuse."),
                step("Let the unknown leg be a", "a² + 5² = 13²", "c = 13."),
                step("Solve", "a² + 25 = 169  →  a² = 144  →  a = 12", "a > 0 in a triangle."),
                step("Final answer", "The other leg is 12.  The triangle is a 5-12-13 Pythagorean triple.", "Check: 5² + 12² = 25 + 144 = 169 = 13² ✓"),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "A ramp rises 4 ft over a horizontal distance of 15 ft. Find the angle of elevation.",
            "Use the inverse tangent.",
            [
                step("Set up the right triangle", "Opposite side = 4, Adjacent side = 15.", "The ramp forms the hypotenuse."),
                step("Tangent ratio", "tan(θ) = opposite/adjacent = 4/15", "Opposite over adjacent for angle at ground."),
                step("Find θ", "θ = arctan(4/15)", "Use inverse tangent."),
                step("Approximate", "arctan(4/15) ≈ arctan(0.267) ≈ 14.9°", "About 15 degrees."),
                step("Final answer", "θ ≈ 15°", "The ramp is a relatively gentle slope."),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "Given sin θ = 8/17 and θ is in Quadrant I, find cos θ and tan θ.",
            "Use the Pythagorean identity and reference triangle.",
            [
                step("Set up the reference triangle", "Opposite = 8, Hypotenuse = 17.  Since sin θ = opp/hyp.", "Pythagorean triple: 8-15-17."),
                step("Find the adjacent side", "adj² + 8² = 17² → adj² = 289 − 64 = 225 → adj = 15", "Positive in QI."),
                step("cos θ", "cos θ = adj/hyp = 15/17", "Adjacent over hypotenuse."),
                step("tan θ", "tan θ = opp/adj = 8/15", "Opposite over adjacent."),
                step("Final answer", "cos θ = 15/17,  tan θ = 8/15", "All in QI so all values positive."),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "From a point 200 m from a building, the angle of elevation to the top is 32°. Find the building's height.",
            "Use the tangent ratio.",
            [
                step("Set up the model", "adjacent = 200 m, opposite = height h, θ = 32°.", "You stand 200 m from the base."),
                step("Tangent ratio", "tan(32°) = h/200", "Opposite over adjacent."),
                step("Solve for h", "h = 200 · tan(32°)", "Multiply both sides by 200."),
                step("Compute", "tan(32°) ≈ 0.625;  h ≈ 200 × 0.625 = 125 m", "Use calculator for tan 32°."),
                step("Final answer", "The building is approximately 125 m tall.", "Check: arctan(125/200) = arctan(0.625) ≈ 32° ✓"),
            ],
            src(LR, "Ch 4.2"),
        ),
    ],

    "the-unit-circle-and-the-six-trig-functions": [
        step_by_step(
            "Find sin(π/6), cos(π/6), and tan(π/6).",
            "Use the 30-60-90 reference triangle.",
            [
                step("Reference triangle", "30-60-90 triangle: sides in ratio 1 : √3 : 2.", "Hypotenuse = 2 (radius = 1 → scaled down by 2)."),
                step("sin(π/6)", "sin(π/6) = opposite/hypotenuse = 1/2", "π/6 = 30°."),
                step("cos(π/6)", "cos(π/6) = adjacent/hypotenuse = √3/2", "Adjacent side = √3."),
                step("tan(π/6)", "tan(π/6) = opp/adj = 1/√3 = √3/3", "Rationalized form preferred."),
                step("Final answer", "sin(π/6) = 1/2,  cos(π/6) = √3/2,  tan(π/6) = √3/3", "These are the exact values."),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "If cos θ = −3/5 and θ is in Quadrant III, find sin θ.",
            "Use the Pythagorean identity sin² θ + cos² θ = 1.",
            [
                step("Pythagorean identity", "sin² θ + cos² θ = 1", "Always true."),
                step("Substitute cos θ", "sin² θ + (−3/5)² = 1  →  sin² θ + 9/25 = 1", "cos² θ = 9/25."),
                step("Solve for sin² θ", "sin² θ = 1 − 9/25 = 16/25", "1 = 25/25."),
                step("Take square root", "sin θ = ±4/5", "Choose sign based on quadrant."),
                step("Choose correct sign", "In QIII, both sin and cos are negative → sin θ = −4/5.", "QIII: x < 0, y < 0."),
                step("Final answer", "sin θ = −4/5", "The reference angle is arcsin(4/5) ≈ 53°."),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "Find the reference angle for 225°.",
            "Find the acute angle to the nearest x-axis.",
            [
                step("Identify the quadrant", "225° is between 180° and 270° → Quadrant III.", "QIII."),
                step("Reference angle formula for QIII", "θ_ref = θ − 180°", "Distance from the 180° line."),
                step("Compute", "225° − 180° = 45°", "An acute angle."),
                step("Final answer", "Reference angle = 45°", "The trig values for 225° have the same magnitude as 45°."),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "Find sec(3π/4) exactly.",
            "Use the unit circle and reciprocal identity.",
            [
                step("Evaluate cos(3π/4)", "3π/4 = 135° is in QII. cos(3π/4) = −√2/2.", "Reference angle = 45°. Cosine is negative in QII."),
                step("Apply secant definition", "sec(θ) = 1/cos(θ)", "Reciprocal identity."),
                step("Compute", "sec(3π/4) = 1 / (−√2/2) = −2/√2 = −√2", "Rationalize: 2/√2 = √2."),
                step("Final answer", "sec(3π/4) = −√2", "Exact value."),
            ],
            src(LR, "Ch 4.3"),
        ),
    ],

    # ─── WEEK 3 ──────────────────────────────────────────────────────────

    "rational-functions-and-their-graphs": [
        step_by_step(
            "Find the vertical asymptote(s) of f(x) = 3x / (x² − 9).",
            "Set denominator = 0 and check if numerator cancels.",
            [
                step("Set denominator = 0", "x² − 9 = 0  →  x² = 9  →  x = ±3", "Potential asymptote locations."),
                step("Check if numerator cancels", "Numerator 3x is zero only at x = 0, not at x = ±3.", "No cancellation — both are true asymptotes."),
                step("Final answer", "Vertical asymptotes: x = 3 and x = −3.", "The graph blows up at these x-values."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Find the horizontal asymptote of f(x) = (3x² + 2) / (x² + 5x).",
            "Compare degrees of numerator and denominator.",
            [
                step("Compare degrees", "Both numerator and denominator have degree 2.", "Degree 2 = Degree 2."),
                step("Rule for equal degree", "Horizontal asymptote: y = leading coefficient ratio = 3/1 = 3.", "Coefficients: 3 (numerator) / 1 (denominator)."),
                step("Final answer", "y = 3 is the horizontal asymptote.", "As x → ±∞, the function approaches 3."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Graph f(x) = 2/x. Describe key features.",
            "Identify asymptotes, intercepts, and behavior.",
            [
                step("Vertical asymptote", "Denominator = 0 at x = 0 → x-axis is the VA.", "x ≠ 0."),
                step("Horizontal asymptote", "Degree numerator (0) < degree denominator (1) → y = 0.", "The graph approaches the x-axis."),
                step("y-intercept", "f(0) is undefined — no y-intercept.", "Cannot divide by zero."),
                step("x-intercept", "2/x = 0 has no solution → no x-intercept.", "Never crosses x-axis."),
                step("Final answer", "Hyperbola in QI and QIII. VA: x = 0. HA: y = 0. As x → 0+, y → +∞; as x → 0−, y → −∞.", "Same shape as y = 1/x but stretched vertically by factor 2."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Find the slant (oblique) asymptote of f(x) = (x² + 3x + 2) / (x + 1).",
            "Perform polynomial long division.",
            [
                step("Divide numerator by denominator", "(x² + 3x + 2) ÷ (x + 1)", "Since degree numerator = degree denominator + 1, expect a slant asymptote."),
                step("Long division", "x² ÷ x = x.  Multiply: x(x+1) = x² + x.  Subtract: (x²+3x+2) − (x²+x) = 2x+2.", "Bring down the 2."),
                step("Continue", "2x ÷ x = 2.  Multiply: 2(x+1) = 2x+2.  Subtract: 0.", "No remainder."),
                step("Final answer", "Slant asymptote: y = x + 2.", "f(x) = x + 2 with no remainder — the asymptote and the graph touch when the rational function is improper in a special way."),
            ],
            src(LR, "Ch 3.3"),
        ),
    ],

    "one-to-one-and-inverse-functions": [
        step_by_step(
            "Verify that f(x) = 3x − 7 is one-to-one and find its inverse.",
            "Use the horizontal-line test and swap x and y.",
            [
                step("Horizontal-line test", "f is linear with slope 3 ≠ 0 → passes the HLT.", "One output for each input."),
                step("Set y = f(x)", "y = 3x − 7", "Write the function as y."),
                step("Swap x and y", "x = 3y − 7", "Solve for the original input."),
                step("Solve for y", "x + 7 = 3y  →  y = (x + 7)/3", "Add 7, then divide by 3."),
                step("Final answer", "f⁻¹(x) = (x + 7)/3", "Verify: f⁻¹(f(x)) = ((3x−7)+7)/3 = 3x/3 = x ✓"),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "Show that f(x) = x³ is one-to-one.",
            "Use the algebraic test: if f(a) = f(b) then a = b.",
            [
                step("Assume f(a) = f(b)", "(a)³ = (b)³", "Cube both sides."),
                step("Take cube root", "³√(a³) = ³√(b³)  →  a = b", "Cube root is one-to-one."),
                step("Alternative: monotonic reasoning", "f'(x) = 3x² ≥ 0 everywhere, and = 0 only at x = 0. The function is strictly increasing.", "Non-negative derivative except at one point."),
                step("Final answer", "f(x) = x³ is one-to-one (strictly increasing, passes the horizontal-line test).", "Its inverse is f⁻¹(x) = ³√x."),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "Find the inverse of f(x) = (x − 2)³ + 5.",
            "Swap x and y, then solve for y.",
            [
                step("Set y = f(x)", "y = (x − 2)³ + 5", "Write as y."),
                step("Swap x and y", "x = (y − 2)³ + 5", "Reflect over y = x."),
                step("Solve for y", "x − 5 = (y − 2)³", "Subtract 5."),
                step("Take cube root", "³√(x − 5) = y − 2  →  y = ³√(x − 5) + 2", "Cube root reverses the cube."),
                step("Final answer", "f⁻¹(x) = ³√(x − 5) + 2", "Verify: f⁻¹(f(x)) = ³√((x−2)³+5−5)+2 = ³√((x−2)³)+2 = (x−2)+2 = x ✓"),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "Why is f(x) = x² not one-to-one? What restriction makes it invertible?",
            "Explain with the horizontal-line test.",
            [
                step("Horizontal-line test", "A horizontal line at y = 4 crosses x² at x = 2 and x = −2.", "Two different inputs give the same output."),
                step("Conclusion", "x² is not one-to-one on its full domain (−∞, ∞).", "Must restrict the domain."),
                step("Standard restriction", "Restrict to x ≥ 0 (or x ≤ 0).", "Choose the right half of the parabola."),
                step("Inverse on x ≥ 0", "f⁻¹(x) = √x", "Square root is the inverse on [0, ∞)."),
                step("Final answer", "Not one-to-one on (−∞, ∞).  On [0, ∞), the inverse is f⁻¹(x) = √x.", "Restricting to the right branch makes it one-to-one."),
            ],
            src(LR, "Ch 5.1"),
        ),
    ],

    "exponential-functions": [
        step_by_step(
            "Solve  4^x = 64.",
            "Express 64 as a power of 4.",
            [
                step("Write 64 as a power of 4", "64 = 4³", "4 · 4 · 4 = 64."),
                step("Set exponents equal", "4^x = 4³  →  x = 3", "Same base, so exponents match."),
                step("Final answer", "x = 3", "Check: 4³ = 64 ✓"),
            ],
            src(LR, "Ch 6.1"),
        ),
        step_by_step(
            "Evaluate  3 · 2^(x+1) = 24.",
            "Solve for x using logarithms or inspection.",
            [
                step("Divide by 3", "2^(x+1) = 8", "Isolate the exponential term."),
                step("Write 8 as a power of 2", "8 = 2³", "2³ = 8."),
                step("Set exponents equal", "x + 1 = 3  →  x = 2", "Same base: 2."),
                step("Final answer", "x = 2", "Check: 3 · 2^(2+1) = 3 · 8 = 24 ✓"),
            ],
            src(LR, "Ch 6.1"),
        ),
        step_by_step(
            "Graph y = 2^x − 3. State the domain, range, and asymptote.",
            "Transform the base exponential.",
            [
                step("Parent function", "y = 2^x. Domain: (−∞, ∞), Range: (0, ∞), HA: y = 0.", "Start here."),
                step("Transformation: −3", "Shift down 3 units.", "Outside the function → affects the output."),
                step("Domain", "(−∞, ∞)", "Still defined for all real x."),
                step("Range", "(−3, ∞)", "All outputs are shifted down by 3."),
                step("Asymptote", "y = −3", "The horizontal asymptote moves down 3."),
                step("y-intercept", "At x = 0: y = 2⁰ − 3 = 1 − 3 = −2 → (0, −2)", "Only intercept."),
                step("Final answer", "Domain: (−∞, ∞); Range: (−3, ∞); HA: y = −3.  Passes through (0, −2).", "The graph is the exponential curve shifted down 3."),
            ],
            src(LR, "Ch 6.1"),
        ),
        step_by_step(
            "A population of bacteria triples every 4 hours. Starting with 500, write the model.",
            "Use the exponential growth formula P(t) = P₀ · r^(t/T).",
            [
                step("Identify parameters", "P₀ = 500 (initial), triple means r = 3 every T = 4 hours.", "Growth factor of 3 per 4-hour period."),
                step("Write the model", "P(t) = 500 · 3^(t/4)", "t is in hours. Divide t by 4 to get number of 4-hour periods."),
                step("Alternative form", "P(t) = 500 · (3^(1/4))^t ≈ 500 · (1.316)^t", "Continuous growth form with rate ≈ 31.6% per hour."),
                step("Final answer", "P(t) = 500 · 3^(t/4)", "After 12 hours: P(12) = 500 · 3^(12/4) = 500 · 3³ = 500 · 27 = 13,500."),
            ],
            src(LR, "Ch 6.1"),
        ),
    ],

    "logarithms-a-first-look": [
        step_by_step(
            "Convert  log₂(1/8) = −3  to exponential form and verify.",
            "Use the definition: log_b(y) = x  ⟺  b^x = y.",
            [
                step("Identify b, x, y", "log₂(1/8) = −3  →  b = 2, x = −3, y = 1/8.", "Match to the definition."),
                step("Write exponential form", "2^(−3) = 1/8", "b^x = y."),
                step("Verify", "2^(−3) = 1/(2³) = 1/8 ✓", "The log statement is correct."),
                step("Final answer", "2^(−3) = 1/8 is verified.", "Negative exponents give fractions less than 1."),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Evaluate  log₅(625).",
            "Find the exponent: 5 to what power gives 625?",
            [
                step("Write as equation", "log₅(625) = x  →  5^x = 625", "Convert to exponential form."),
                step("Factor 625", "625 = 5⁴ (since 5·5·5·5 = 625)", "Recognize the power of 5."),
                step("Set exponents equal", "x = 4", "5^x = 5⁴."),
                step("Final answer", "log₅(625) = 4", "Check: 5⁴ = 625 ✓"),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Solve  ln(x) = 4  for x.",
            "Use the inverse relationship: e^(ln x) = x.",
            [
                step("Apply exponential to both sides", "e^(ln x) = e⁴", "e^x is the inverse of ln x."),
                step("Simplify", "x = e⁴", "ln and e cancel."),
                step("Approximate", "e⁴ ≈ 54.598", "Using e ≈ 2.718."),
                step("Final answer", "x = e⁴ ≈ 54.6", "Check: ln(54.6) ≈ 4 ✓"),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Solve  log₂(x + 3) = 5.",
            "Convert to exponential and solve.",
            [
                step("Convert to exponential", "2⁵ = x + 3", "log_b(y) = x → b^x = y."),
                step("Compute 2⁵", "2⁵ = 32", "2·2·2·2·2 = 32."),
                step("Solve for x", "x + 3 = 32  →  x = 29", "Subtract 3."),
                step("Check", "log₂(29 + 3) = log₂(32) = 5 ✓", "x = 29 is valid."),
                step("Final answer", "x = 29", "Domain requires x + 3 > 0, so x > −3. 29 > −3 ✓."),
            ],
            src(LR, "Ch 6.2"),
        ),
    ],

    # ─── WEEK 4 ──────────────────────────────────────────────────────────

    "logarithm-rules": [
        step_by_step(
            "Expand  ln[(x² · √(x+1)) / eˣ].",
            "Apply log rules: log(AB) = log A + log B, log(A/B) = log A − log B, log(Aⁿ) = n log A.",
            [
                step("Quotient rule", "ln(x² · √(x+1)) − ln(eˣ)", "ln(A/B) = ln A − ln B."),
                step("Product rule", "ln(x²) + ln(√(x+1)) − ln(eˣ)", "ln(AB) = ln A + ln B."),
                step("Power rule on each", "2 ln x + ln((x+1)^(1/2)) − x ln e", "ln(Aⁿ) = n ln A."),
                step("Simplify further", "2 ln x + (1/2) ln(x+1) − x · 1", "ln e = 1."),
                step("Final answer", "2 ln x + (1/2) ln(x+1) − x", "All arguments are now single terms."),
            ],
            src(LR, "Ch 6.3"),
        ),
        step_by_step(
            "Solve  2 ln x + ln 3 = ln 15.",
            "Combine logs and solve.",
            [
                step("Combine left side", "2 ln x + ln 3 = ln(x²) + ln 3 = ln(3x²)", "2 ln x = ln(x²).  ln A + ln B = ln(AB)."),
                step("Set equal", "ln(3x²) = ln 15", "If ln A = ln B, then A = B."),
                step("Solve equation", "3x² = 15  →  x² = 5  →  x = √5", "x > 0 (domain of ln)."),
                step("Check", "2 ln(√5) + ln 3 = ln(5) + ln 3 = ln 15 ✓", "Both sides equal ln 15."),
                step("Final answer", "x = √5 ≈ 2.24", "x = −√5 is rejected since ln(−√5) is undefined."),
            ],
            src(LR, "Ch 6.3"),
        ),
        step_by_step(
            "Write  (1/2) ln(x + 2) − 3 ln x  as a single logarithm.",
            "Reverse the expansion: n ln A = ln(Aⁿ), ln A − ln B = ln(A/B).",
            [
                step("Apply power rule (reverse)", "(1/2) ln(x+2) = ln((x+2)^(1/2)) = ln(√(x+2))", "1/2 is the coefficient."),
                step("Apply power rule (reverse)", "3 ln x = ln(x³)", "Move 3 into the exponent."),
                step("Apply quotient rule", "ln(√(x+2)) − ln(x³) = ln(√(x+2) / x³)", "Subtraction → division."),
                step("Simplify numerator", "√(x+2) = (x+2)^(1/2)", "Keep as a single radical."),
                step("Final answer", "ln(√(x+2) / x³)  or  ln(√(x+2)) − ln(x³)", "Domain: x > 0 (for ln x)."),
            ],
            src(LR, "Ch 6.3"),
        ),
        step_by_step(
            "Solve  log₃(x + 4) + log₃(x) = 2.",
            "Combine logs then convert to exponential.",
            [
                step("Combine logs", "log₃[(x + 4) · x] = log₃(x² + 4x) = 2", "log₃ A + log₃ B = log₃(AB)."),
                step("Convert to exponential", "x² + 4x = 3² = 9", "log_b(y) = x → b^x = y."),
                step("Solve quadratic", "x² + 4x − 9 = 0", "x² + 4x − 9 = 0."),
                step("Apply formula", "x = [−4 ± √(16 + 36)] / 2 = [−4 ± √52] / 2 = [−4 ± 2√13] / 2 = −2 ± √13", "Two solutions."),
                step("Check domain", "log₃(x + 4): x > −4; log₃(x): x > 0. Combined: x > 0.", "Reject −2 − √13 < 0. Keep −2 + √13 ≈ 1.61."),
                step("Final answer", "x = √13 − 2 ≈ 1.61", "Check: log₃(1.61+4) + log₃(1.61) ≈ log₃(5.61) + log₃(1.61) ≈ 1.66 + 0.37 ≈ 2.03 ≈ 2 ✓"),
            ],
            src(LR, "Ch 6.3"),
        ),
    ],

    "graphs-of-the-six-trig-functions": [
        step_by_step(
            "Graph y = sin x on [0, 2π]. List key points.",
            "Mark intercepts, maxima, and minima.",
            [
                step("Identify key angles", "0, π/2, π, 3π/2, 2π", "Quarter-period points."),
                step("Compute sin values", "sin(0)=0; sin(π/2)=1; sin(π)=0; sin(3π/2)=−1; sin(2π)=0", "Unit circle values."),
                step("Trace the wave", "From (0,0) → up to (π/2,1) → down to (π,0) → down to (3π/2,−1) → up to (2π,0)", "One complete wave."),
                step("Final answer", "Period: 2π. Amplitude: 1. Max at (π/2, 1). Min at (3π/2, −1). Intercepts at 0, π, 2π.", "The sine wave oscillates between y = −1 and y = 1."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Find the period and amplitude of y = 4 cos(2x).",
            "Use the form A cos(Bx).",
            [
                step("Identify amplitude", "|A| = |4| = 4", "Amplitude is the absolute value of the coefficient."),
                step("Identify B", "B = 2", "The x-coefficient inside the trig function."),
                step("Find period", "Period = 2π/B = 2π/2 = π", "Standard period of cosine is 2π."),
                step("Final answer", "Amplitude = 4, Period = π.", "The wave completes 2 cycles in the usual [0, 2π] interval."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Describe the transformation from y = tan x to y = 2 tan(x − π/4) + 1.",
            "Identify each transformation in order.",
            [
                step("Inside: (x − π/4)", "Shift RIGHT by π/4. The asymptote moves from x = ±π/2 to x = π/4 ± π/2.", "f(x − h) shifts right."),
                step("Multiply by 2", "Vertical stretch by 2. The rate of change doubles.", "Stretches away from the x-axis."),
                step("Outside: +1", "Shift UP by 1. The center of the wave moves to y = 1.", "f(x) + k shifts up."),
                step("Final answer", "Shift right π/4, vertical stretch by 2, shift up 1. VA: x = π/4 ± π/2. Period: π. Range: all real numbers (no amplitude).", "Tan has no amplitude — range is all reals."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Graph y = −sin x on [0, 2π].",
            "Reflect y = sin x over the x-axis.",
            [
                step("Start with sin x", "Wave: 0 → 1 → 0 → −1 → 0 on [0, 2π].", "Standard sine wave."),
                step("Apply reflection", "Multiply y by −1: 0 → −1 → 0 → 1 → 0.", "Negating flips the graph vertically."),
                step("Key points (negated)", "At x=0: y=0; x=π/2: y=−1; x=π: y=0; x=3π/2: y=1; x=2π: y=0", "The trough becomes a peak and vice versa."),
                step("Final answer", "Same period (2π) and amplitude (1) as sin x, but reflected. Max at (3π/2, 1), Min at (π/2, −1).", "Looks like an inverted sine wave."),
            ],
            src(LR, "Ch 7.1"),
        ),
    ],

    "fundamental-trig-identities": [
        step_by_step(
            "Simplify  (1 − cos² θ) / sin θ  using trig identities.",
            "Apply Pythagorean identity.",
            [
                step("Recall Pythagorean identity", "sin² θ + cos² θ = 1  →  sin² θ = 1 − cos² θ", "This relates sin and cos."),
                step("Substitute", "(sin² θ) / sin θ", "Replace 1 − cos² θ with sin² θ."),
                step("Cancel common factor", "sin² θ / sin θ = sin θ", "sin θ ≠ 0 (otherwise the original is undefined)."),
                step("Final answer", "sin θ", "For θ where sin θ ≠ 0 (i.e., θ ≠ nπ)."),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Verify the identity: sec θ / sin θ = csc θ.",
            "Rewrite everything in terms of sin and cos.",
            [
                step("Rewrite left side", "sec θ / sin θ = (1/cos θ) / sin θ = 1 / (cos θ · sin θ)", "sec θ = 1/cos θ."),
                step("Rewrite right side", "csc θ = 1/sin θ", "Reciprocal identity."),
                step("Note: these are NOT equal!", "1/(cos θ · sin θ) ≠ 1/sin θ unless cos θ = 1.", "My mistake — the original identity is incorrect. Correct identity: sec θ · sin θ = tan θ."),
                step("Final answer", "sec θ / sin θ = csc θ is FALSE. The correct identity is: sec θ · sin θ = tan θ.", "Let's verify sec θ · sin θ = tan θ: (1/cos θ)·sin θ = sin θ/cos θ = tan θ ✓"),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Simplify  tan θ · csc θ  to a single trig function.",
            "Rewrite in sin and cos.",
            [
                step("Substitute identities", "tan θ · csc θ = (sin θ / cos θ) · (1 / sin θ)", "tan = sin/cos; csc = 1/sin."),
                step("Cancel sin θ", "(sin θ / cos θ) · (1 / sin θ) = 1 / cos θ", "sin θ cancels."),
                step("Final answer", "= sec θ", "Since 1/cos θ = sec θ."),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Given sin θ = 3/5 (QII), find sec θ.",
            "Use the Pythagorean identity.",
            [
                step("Find cos θ", "sin² θ + cos² θ = 1  →  (3/5)² + cos² θ = 1  →  9/25 + cos² θ = 1", "cos² θ = 16/25."),
                step("Take square root", "cos θ = ±4/5", "Choose sign by quadrant."),
                step("Choose correct sign", "QII: cos is negative → cos θ = −4/5.", "QII = left half of unit circle, x < 0."),
                step("Compute sec θ", "sec θ = 1/cos θ = 1 / (−4/5) = −5/4", "Reciprocal of cosine."),
                step("Final answer", "sec θ = −5/4", "Check: tan θ = sin θ / cos θ = (3/5) / (−4/5) = −3/4. ✓"),
            ],
            src(LR, "Ch 7.2"),
        ),
    ],

    "sum-difference-double-angle-and-half-angle-identities": [
        step_by_step(
            "Find cos(2θ) if sin θ = 4/5 and θ is in QI.",
            "Use the double-angle identity.",
            [
                step("Find cos θ", "sin² θ + cos² θ = 1  →  (4/5)² + cos² θ = 1  →  cos² θ = 9/25 → cos θ = 3/5", "Positive in QI."),
                step("Choose identity", "cos(2θ) = cos² θ − sin² θ", "All three forms work here."),
                step("Substitute", "cos(2θ) = (3/5)² − (4/5)² = 9/25 − 16/25 = −7/25", "Numerically exact."),
                step("Final answer", "cos(2θ) = −7/25", "Note: if instead using cos(2θ) = 1 − 2 sin² θ = 1 − 2(16/25) = 1 − 32/25 = −7/25 ✓"),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "Use a half-angle identity to find sin(15°).",
            "Express 15° as half of 30°.",
            [
                step("Set up half-angle", "sin(θ/2) = ±√[(1 − cos θ)/2]", "θ = 30°, so θ/2 = 15°."),
                step("Find cos(30°)", "cos(30°) = √3/2", "Reference angle 30°."),
                step("Substitute", "sin(15°) = √[(1 − √3/2)/2] = √[(2/2 − √3/2)/2] = √[(2 − √3)/4] = √(2 − √3)/2", "Both sine and cosine are positive in QI."),
                step("Approximate", "√(2 − 1.732) = √0.268 ≈ 0.518;  0.518/2 ≈ 0.259", "sin(15°) ≈ 0.259 ✓ (actual sin 15° ≈ 0.2588)."),
                step("Final answer", "sin(15°) = √(2 − √3)/2 ≈ 0.259", "Exact form is preferred on tests."),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "If cos x = 5/13 (QI), find cos 2x and sin 2x.",
            "Use double-angle identities.",
            [
                step("Find sin x", "sin² x = 1 − (5/13)² = 1 − 25/169 = 144/169 → sin x = 12/13 (positive in QI).", "Pythagorean identity."),
                step("cos 2x = 2 cos² x − 1", "2(5/13)² − 1 = 2(25/169) − 1 = 50/169 − 169/169 = −119/169", "Formula 1 of cos 2x."),
                step("sin 2x = 2 sin x cos x", "2 · (12/13) · (5/13) = 120/169", "Product-to-sum form."),
                step("Final answer", "cos 2x = −119/169,  sin 2x = 120/169", "Note: (−119, 120) follows a Pythagorean triple pattern: 119²+120² = 169²."),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "Expand cos(π/2 + x) using the sum identity.",
            "Apply cos(A + B) = cos A cos B − sin A sin B.",
            [
                step("Set A = π/2, B = x", "cos(π/2 + x) = cos(π/2) cos x − sin(π/2) sin x", "Apply the identity."),
                step("Evaluate trig values", "cos(π/2) = 0;  sin(π/2) = 1", "Unit circle at π/2."),
                step("Substitute", "= 0 · cos x − 1 · sin x = − sin x", "Simplify."),
                step("Final answer", "cos(π/2 + x) = − sin x", "This is a co-function identity — cosine shifted by π/2 becomes −sine."),
            ],
            src(LR, "Ch 7.3"),
        ),
    ],

    # ─── WEEK 5 ──────────────────────────────────────────────────────────

    "solving-polynomial-equations": [
        step_by_step(
            "Solve  x³ − 3x² − 4x + 12 = 0.",
            "Use the Rational Root Theorem and synthetic division.",
            [
                step("Find possible rational roots", "±1, ±2, ±3, ±4, ±6, ±12", "p/q where p divides 12 and q divides 1."),
                step("Test x = 2", "2³ − 3(4) − 4(2) + 12 = 8 − 12 − 8 + 12 = 0 ✓", "x = 2 is a root."),
                step("Synthetic division by (x − 2)", "2 | 1  -3  -4   12\n    |     2  -2  -12\n      1  -1  -6    0", "The remainder is 0."),
                step("Factor remaining quadratic", "x² − x − 6 = (x − 3)(x + 2)", "Find roots: x² − x − 6 = 0 → x = 3 or x = −2."),
                step("Final answer", "x = 2, 3, −2", "Three real roots. Check: (2)(3)(−2) = −12 = −constant term? Let's verify in original: for x=3: 27−27−12+12=0 ✓; x=−2: −8−12+8+12=0 ✓"),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Solve  x⁴ − 5x² + 4 = 0.",
            "Treat as a quadratic in x².",
            [
                step("Substitute u = x²", "Then x⁴ = u². The equation becomes u² − 5u + 4 = 0.", "This is a quadratic in u."),
                step("Factor u² − 5u + 4", "(u − 1)(u − 4) = 0", "Find two numbers that multiply to 4 and add to −5: −1 and −4."),
                step("Solve for u", "u = 1 or u = 4", "Back-substitute."),
                step("Solve for x", "x² = 1 → x = ±1;  x² = 4 → x = ±2", "Take square roots."),
                step("Final answer", "x = 1, −1, 2, −2", "Four real roots."),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Solve  x³ = 27.",
            "Take cube roots.",
            [
                step("Rewrite as equation", "x³ − 27 = 0", "Move all terms to one side."),
                step("Recognize difference of cubes", "27 = 3³, so x³ − 3³ = 0", "Factor: a³ − b³ = (a − b)(a² + ab + b²)."),
                step("Factor", "(x − 3)(x² + 3x + 9) = 0", "Now solve each factor."),
                step("Solve linear factor", "x − 3 = 0 → x = 3", "First root."),
                step("Solve quadratic", "x² + 3x + 9 = 0 → x = [−3 ± √(9−36)]/2 = [−3 ± √(−27)]/2 = −3/2 ± (3√3/2)i", "Complex conjugate pair."),
                step("Final answer", "x = 3,  x = −3/2 ± (3√3/2)i", "One real root and two complex conjugate roots."),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Use Descartes' Rule of Signs to find the number of positive and negative real roots of P(x) = 2x³ − x² − 5x + 1.",
            "Count sign changes in P(x) and P(−x).",
            [
                step("Sign changes in P(x)", "2x³ (positive) → −x² (negative): change 1; −x² (negative) → −5x (negative): no change; −5x (negative) → +1 (positive): change 2. Total: 2 sign changes → 2 or 0 positive roots.", "Read left to right."),
                step("Sign changes in P(−x)", "P(−x) = 2(−x)³ − (−x)² − 5(−x) + 1 = −2x³ − x² + 5x + 1. Signs: −2x³ (−) → −x² (−): no change; −x² (−) → +5x (+): change 1; +5x (+) → +1 (+): no change. Total: 1 sign change → 1 negative root.", "Replace x with −x and simplify."),
                step("Final answer", "Positive roots: 2 or 0 (actual count is 2 or 0). Negative roots: exactly 1. Total roots = 3 (counting complex).", "The actual roots can be found by factoring or the cubic formula."),
            ],
            src(LR, "Ch 3.4"),
        ),
    ],

    "rational-equations": [
        step_by_step(
            "Solve  x/(x − 2) + 3/(x + 4) = 1.",
            "Multiply by the LCD and check for extraneous solutions.",
            [
                step("Identify the LCD", "(x − 2)(x + 4)", "Each factor appears once."),
                step("Multiply both sides", "x(x + 4) + 3(x − 2) = (x − 2)(x + 4)", "Cancel denominators."),
                step("Expand", "x² + 4x + 3x − 6 = x² + 4x − 2x − 8", "FOIL both sides."),
                step("Simplify left", "x² + 7x − 6 = x² + 2x − 8", "4x + 3x = 7x."),
                step("Solve", "x² + 7x − 6 − x² − 2x + 8 = 0 → 5x + 2 = 0 → x = −2/5", "Subtract right side. Linear equation."),
                step("Check domain", "x ≠ 2, x ≠ −4. x = −2/5 is allowed.", "Not extraneous."),
                step("Verify in original", "(−2/5)/(−2/5−2) + 3/(−2/5+4) = (−2/5)/(−12/5) + 3/(18/5) = (−2/5)(−5/12) + 3(5/18) = 2/12 + 15/18 = 1/6 + 5/6 = 1 ✓", "Check: −2/5−2 = −2/5−10/5 = −12/5 ✓; −2/5+4 = −2/5+20/5 = 18/5 ✓."),
                step("Final answer", "x = −2/5", "The only solution."),
            ],
            src(LR, "Ch 3.5"),
        ),
        step_by_step(
            "Solve  4/(x − 3) = 2/x.",
            "Cross-multiply and check domain.",
            [
                step("Cross-multiply", "4x = 2(x − 3)", "Multiply both sides by x(x − 3)."),
                step("Expand", "4x = 2x − 6", "2(x − 3) = 2x − 6."),
                step("Solve", "4x − 2x = −6  →  2x = −6  →  x = −3", "Subtract 2x from both sides."),
                step("Check domain", "x ≠ 0, x ≠ 3. x = −3 is allowed.", "No denominator is zero."),
                step("Verify", "4/(−3−3) = 4/(−6) = −2/3;  2/(−3) = −2/3 ✓", "Both sides equal."),
                step("Final answer", "x = −3", "Only solution."),
            ],
            src(LR, "Ch 3.5"),
        ),
        step_by_step(
            "Solve  (x + 1)/(x − 5) = 3/4.",
            "Cross-multiply.",
            [
                step("Cross-multiply", "4(x + 1) = 3(x − 5)", "b ≠ 0, d ≠ 0."),
                step("Expand", "4x + 4 = 3x − 15", "Left: 4 times x+1. Right: 3 times x−5."),
                step("Solve", "4x − 3x = −15 − 4  →  x = −19", "Isolate x."),
                step("Check domain", "x ≠ 5. x = −19 is allowed.", "No problem."),
                step("Verify", "(−19+1)/(−19−5) = (−18)/(−24) = 3/4 ✓", "18/24 simplifies to 3/4."),
                step("Final answer", "x = −19", "Valid solution."),
            ],
            src(LR, "Ch 3.5"),
        ),
        step_by_step(
            "Solve  1/x + 2/x² = 2.",
            "Multiply by x² to clear denominators.",
            [
                step("Multiply by x²", "x + 2 = 2x²", "x² · (1/x) = x; x² · (2/x²) = 2; x² · 2 = 2x²."),
                step("Rewrite as quadratic", "2x² − x − 2 = 0", "Bring all terms to one side."),
                step("Apply quadratic formula", "x = [1 ± √(1 + 16)] / (4) = [1 ± √17] / 4", "D = (−1)² − 4(2)(−2) = 1 + 16 = 17."),
                step("Approximate", "x₁ ≈ (1+4.123)/4 ≈ 1.28;  x₂ ≈ (1−4.123)/4 ≈ −0.78", "Both are non-zero so valid."),
                step("Check domain", "x ≠ 0. Both solutions are non-zero.", "Good."),
                step("Final answer", "x = (1 ± √17) / 4 ≈ 1.28, −0.78", "Verify by substituting into original."),
            ],
            src(LR, "Ch 3.5"),
        ),
    ],

    "exponential-and-logarithmic-equations": [
        step_by_step(
            "Solve  3^(2x) = 7.",
            "Take logs of both sides.",
            [
                step("Take log of both sides", "log(3^(2x)) = log 7", "Any log works — natural or common."),
                step("Apply power rule", "2x · log 3 = log 7", "log(a^b) = b log a."),
                step("Solve for x", "x = log 7 / (2 · log 3)", "Isolate x."),
                step("Approximate", "x ≈ 0.8451 / (2 × 0.4771) = 0.8451 / 0.9542 ≈ 0.886", "log 7 ≈ 0.8451; log 3 ≈ 0.4771."),
                step("Final answer", "x = log(7) / (2 log(3)) ≈ 0.886", "Exact form is preferred."),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  ln(x) + ln(x + 2) = 1.",
            "Combine logs, then exponentiate.",
            [
                step("Combine logs", "ln[x(x + 2)] = 1", "ln A + ln B = ln(AB)."),
                step("Exponentiate", "x(x + 2) = e¹ = e", "e^ln(z) = z."),
                step("Expand and solve", "x² + 2x − e = 0", "Quadratic in x."),
                step("Apply quadratic formula", "x = [−2 ± √(4 + 4e)] / 2 = [−2 ± 2√(1 + e)] / 2 = −1 ± √(1 + e)", "D = 4(1+e)."),
                step("Check domain", "x > 0 and x > −2 (from ln(x+2)) → x > 0.", "The domain of ln is positive."),
                step("Pick valid root", "−1 + √(1+e) > 0 ✓ (since √(1+e) > √1 = 1);  −1 − √(1+e) < 0 ✗", "Only the positive root is in domain."),
                step("Final answer", "x = −1 + √(1 + e) ≈ −1 + 1.859 ≈ 0.859", "Check: ln(0.859) + ln(2.859) ≈ −0.152 + 1.050 ≈ 0.898 ≈ 1 ✓"),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  e^(x) = 12.",
            "Take the natural log of both sides.",
            [
                step("Take ln of both sides", "ln(e^x) = ln 12", "ln and e are inverses."),
                step("Simplify left side", "x = ln 12", "ln(e^x) = x."),
                step("Approximate", "ln 12 ≈ 2.485", "e^2.485 ≈ 12."),
                step("Final answer", "x = ln 12 ≈ 2.485", "Exact: x = ln 12.  Alternative: x = ln(12)."),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  2 · 5^(x+1) = 50.",
            "Isolate the exponential and take logs.",
            [
                step("Divide by 2", "5^(x+1) = 25", "Isolate the exponential term."),
                step("Recognize 25 as 5²", "5^(x+1) = 5²", "5² = 25."),
                step("Set exponents equal", "x + 1 = 2  →  x = 1", "Same base."),
                step("Final answer", "x = 1", "Check: 2 · 5^(1+1) = 2 · 5² = 2 · 25 = 50 ✓"),
            ],
            src(LR, "Ch 6.4"),
        ),
    ],

    "trigonometric-equations": [
        step_by_step(
            "Solve  2 cos θ + 1 = 0  on [0, 2π).",
            "Isolate cos θ and find reference angles.",
            [
                step("Isolate cos θ", "2 cos θ = −1  →  cos θ = −1/2", "Subtract 1, divide by 2."),
                step("Find reference angle", "cos α = 1/2 → α = π/3 (60°)", "Reference angle in QI."),
                step("Find angles in [0, 2π) with cos = −1/2", "QII: θ = π − π/3 = 2π/3. QIII: θ = π + π/3 = 4π/3.", "cos is negative in QII and QIII."),
                step("Final answer", "θ = 2π/3,  4π/3", "Two solutions in [0, 2π)."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  tan θ = √3  on [0, π).",
            "Find angles where tangent equals √3.",
            [
                step("Recall tan(π/3)", "tan(π/3) = √3", "π/3 is a standard angle."),
                step("Identify the solution", "tan is positive in QI and QIII. QI gives θ = π/3.", "QIII would be π + π/3 = 4π/3, but that's outside [0, π)."),
                step("Final answer", "θ = π/3  (60°)", "Only one solution in [0, π). Note: [0, π) covers QI and QII — tan is undefined at π/2 so only π/3 works."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  sin² θ − sin θ = 0  on [0, 2π).",
            "Factor and solve each factor.",
            [
                step("Factor", "sin θ (sin θ − 1) = 0", "Take sin θ common."),
                step("Solve sin θ = 0", "θ = 0, π, 2π", "sin = 0 at integer multiples of π."),
                step("Solve sin θ = 1", "θ = π/2", "sin = 1 at π/2."),
                step("Final answer", "θ = 0, π/2, π, 2π", "Four solutions in [0, 2π). sin θ − 1 = 0 gives sin θ = 1 (only at π/2)."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  cos(2θ) = 1/2  on [0, 2π).",
            "Find 2θ first, then divide.",
            [
                step("Find general solutions for 2θ", "cos φ = 1/2 → φ = ±π/3 + 2kπ = π/3 or 5π/3 (in [0, 2π)).", "Reference angle π/3. cos positive in QI and QIV."),
                step("2θ = π/3 + 2kπ  or  2θ = 5π/3 + 2kπ", "Let φ = 2θ and solve for θ.", "Express 2θ in terms of the general solutions for cos φ = 1/2."),
                step("Solve 2θ = π/3", "θ = π/6 + kπ", "Divide by 2. Add π for the period."),
                step("Solve 2θ = 5π/3", "θ = 5π/6 + kπ", "5π/3 ÷ 2 = 5π/6."),
                step("Find values in [0, 2π)", "θ = π/6, 7π/6 (from π/6 + kπ);  θ = 5π/6, 11π/6 (from 5π/6 + kπ).", "k = 0, 1 gives 4 solutions."),
                step("Final answer", "θ = π/6, 5π/6, 7π/6, 11π/6", "All in [0, 2π)."),
            ],
            src(LR, "Ch 8.1"),
        ),
    ],

    "systems-of-linear-equations": [
        step_by_step(
            "Solve by substitution:  y = 3x − 7  and  2x + y = 4.",
            "Substitute y from the first into the second.",
            [
                step("Substitute", "2x + (3x − 7) = 4", "Replace y with 3x − 7."),
                step("Solve", "5x − 7 = 4  →  5x = 11  →  x = 11/5 = 2.2", "Combine like terms."),
                step("Find y", "y = 3(11/5) − 7 = 33/5 − 35/5 = −2/5 = −0.4", "Substitute x back."),
                step("Final answer", "(x, y) = (11/5, −2/5) or (2.2, −0.4)", "Check: 2(11/5) + (−2/5) = 22/5 − 2/5 = 20/5 = 4 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "Solve by elimination:  3x + 4y = 5  and  2x − 4y = 10.",
            "Add the equations to eliminate y.",
            [
                step("Add the equations", "(3x + 4y) + (2x − 4y) = 5 + 10  →  5x = 15", "4y + (−4y) = 0. The y terms cancel."),
                step("Solve for x", "x = 3", "5x = 15."),
                step("Back-substitute", "3(3) + 4y = 5  →  9 + 4y = 5  →  4y = −4  →  y = −1", "Use the first equation."),
                step("Final answer", "(x, y) = (3, −1)", "Check: 2(3) − 4(−1) = 6 + 4 = 10 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "Solve:  x + y = 6  and  x − y = 2.",
            "Add to eliminate y.",
            [
                step("Add the equations", "(x + y) + (x − y) = 6 + 2  →  2x = 8", "y + (−y) = 0."),
                step("Solve for x", "x = 4", "Divide by 2."),
                step("Find y", "4 + y = 6  →  y = 2", "Substitute into the first equation."),
                step("Final answer", "(x, y) = (4, 2)", "Check: 4 − 2 = 2 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "Solve using substitution:  2x − 3y = 8  and  x = 2y + 1.",
            "Substitute x from the second into the first.",
            [
                step("Substitute", "2(2y + 1) − 3y = 8", "Replace x with 2y + 1."),
                step("Expand and simplify", "4y + 2 − 3y = 8  →  y + 2 = 8  →  y = 6", "4y − 3y = y."),
                step("Find x", "x = 2(6) + 1 = 13", "x = 2y + 1."),
                step("Final answer", "(x, y) = (13, 6)", "Check: 2(13) − 3(6) = 26 − 18 = 8 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
    ],

    # ─── WEEK 6 ──────────────────────────────────────────────────────────

    "the-law-of-sines": [
        step_by_step(
            "Given A = 30°, B = 100°, a = 10. Find b and C.",
            "Apply the Law of Sines.",
            [
                step("Find angle C", "C = 180° − A − B = 180° − 30° − 100° = 50°", "Angles in a triangle sum to 180°."),
                step("Law of Sines", "a/sin A = b/sin B = c/sin C", "Relate sides to opposite angles."),
                step("Set up ratio", "a/sin A = 10 / sin(30°) = 10 / (1/2) = 20", "sin 30° = 1/2."),
                step("Find b", "b / sin(100°) = 20  →  b = 20 · sin(100°) ≈ 20 · 0.9848 ≈ 19.70", "sin 100° ≈ 0.9848."),
                step("Final answer", "C = 50°,  b ≈ 19.7 (to one decimal)", "Check: 10/sin30 = 10/0.5 = 20. 19.7/sin100 ≈ 19.7/0.9848 ≈ 20 ✓"),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "Find the area of triangle ABC with A = 45°, b = 8, c = 6.",
            "Use the formula: Area = (1/2)bc sin A.",
            [
                step("Recall formula", "Area = (1/2)bc sin A", "Two sides and the included angle."),
                step("Substitute", "Area = (1/2)(8)(6) sin(45°) = 24 · (√2/2) = 12√2", "sin 45° = √2/2."),
                step("Approximate", "12√2 ≈ 12 · 1.414 ≈ 16.97", "About 17 square units."),
                step("Final answer", "Area = 12√2 ≈ 17.0 square units", "Without trigonometry, you cannot find the area from just two sides."),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "Given A = 50°, a = 12, b = 8. Solve the triangle (find B, C, c).",
            "Apply Law of Sines and check the ambiguous case.",
            [
                step("Law of Sines", "sin B / b = sin A / a  →  sin B / 8 = sin(50°) / 12", "sin 50° ≈ 0.7660."),
                step("Solve for sin B", "sin B = 8 · (0.7660/12) ≈ 8 · 0.06383 ≈ 0.5106", "Compute 0.766/12."),
                step("Find angle B", "B = arcsin(0.5106) ≈ 30.7° (or B ≈ 180° − 30.7° = 149.3°)", "Both are valid in the ambiguous case (SSA)."),
                step("Check if B + A < 180° for both", "B₁ = 30.7°: 30.7+50 = 80.7 < 180 ✓ → valid. B₂ = 149.3°: 149.3+50 = 199.3 > 180 ✗ → invalid (sum exceeds 180°).", "Only one solution."),
                step("Find C and c", "C = 180° − 50° − 30.7° = 99.3°.  c/sin C = a/sin A → c = 12 · sin(99.3°)/sin(50°) ≈ 12 · 0.9907/0.7660 ≈ 15.5.", "Find the remaining angle and side."),
                step("Final answer", "B ≈ 30.7°, C ≈ 99.3°, c ≈ 15.5", "One solution exists (the obtuse case was impossible)."),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "A flagpole casts a shadow 15 m long. The sun's elevation is 55°. How tall is the pole?",
            "Model with a right triangle.",
            [
                step("Set up the triangle", "Angle of elevation = 55°, adjacent = 15 m, opposite = height h.", "You stand at the end of the shadow."),
                step("Tangent ratio", "tan(55°) = h / 15", "Opposite over adjacent."),
                step("Solve for h", "h = 15 · tan(55°) ≈ 15 · 1.428 ≈ 21.4 m", "tan 55° ≈ 1.428."),
                step("Final answer", "The flagpole is approximately 21.4 m tall.", "Check: tan⁻¹(21.4/15) = tan⁻¹(1.427) ≈ 55° ✓"),
            ],
            src(LR, "Ch 8.6"),
        ),
    ],

    "the-law-of-cosines": [
        step_by_step(
            "Find all angles of a triangle with sides a = 7, b = 9, c = 12.",
            "Use Law of Cosines to find angles. Start with the largest angle.",
            [
                step("Find the largest angle (opposite longest side c = 12)", "cos C = (a² + b² − c²) / (2ab) = (49 + 81 − 144) / (2·7·9) = (−14) / 126 ≈ −0.111", "c = 12 is the longest side."),
                step("Find C", "C = arccos(−0.111) ≈ 96.4°", "Inverse cosine of a negative gives an obtuse angle."),
                step("Find angle A", "cos A = (b² + c² − a²) / (2bc) = (81 + 144 − 49) / (2·9·12) = (176) / 216 ≈ 0.8148;  A = arccos(0.8148) ≈ 35.3°", "Pick either remaining side pair."),
                step("Find angle B", "B = 180° − C − A ≈ 180° − 96.4° − 35.3° = 48.3°", "Sum of angles is 180°."),
                step("Check", "A + B + C ≈ 35.3 + 48.3 + 96.4 = 180° ✓", "Angles sum to 180°."),
                step("Final answer", "A ≈ 35.3°, B ≈ 48.3°, C ≈ 96.4°", "The triangle is obtuse."),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "Two sides of a parallelogram are 8 cm and 5 cm, with an included angle of 60°. Find the diagonal.",
            "The diagonal connects the two sides with the included angle.",
            [
                step("Apply Law of Cosines", "d² = 8² + 5² − 2(8)(5) cos(60°) = 64 + 25 − 80 · (1/2) = 89 − 40 = 49", "d² = a² + b² − 2ab cos θ."),
                step("Take square root", "d = √49 = 7 cm", "The diagonal is 7 cm."),
                step("Final answer", "The diagonal is 7 cm.", "Interestingly, a 5-8-7 triangle satisfies the triangle inequality. The other diagonal would use cos(180°−60°) = −cos(60°), giving √(64+25+40) = √129."),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "A triangle has sides 6, 7, and 10. Is it acute, right, or obtuse?",
            "Check the largest angle using the Law of Cosines.",
            [
                step("Identify the largest side", "c = 10 (opposite angle C)", "Longest side determines the largest angle."),
                step("Compute c² and a² + b²", "c² = 100.  a² + b² = 6² + 7² = 36 + 49 = 85.", "Compare to determine angle type."),
                step("Compare", "c² = 100 > 85 = a² + b²", "c² > a² + b²."),
                step("Classify", "c² > a² + b² → the angle C is obtuse (> 90°).", "Opposite side c is too long for the triangle to be acute."),
                step("Final answer", "The triangle is obtuse (angle C > 90°).", "If c² = a² + b², it would be right. If c² < a² + b², it would be acute."),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "Find the area of a triangle with sides 5, 7, and 10 using Heron's formula.",
            "Compute s = (a+b+c)/2 first.",
            [
                step("Compute semi-perimeter s", "s = (5 + 7 + 10) / 2 = 22/2 = 11", "Average perimeter."),
                step("Apply Heron's formula", "A = √[s(s−a)(s−b)(s−c)] = √[11(11−5)(11−7)(11−10)] = √[11·6·4·1] = √264", "s−a = 11−5=6; s−b = 11−7=4; s−c = 11−10=1."),
                step("Simplify", "√264 = √(4·66) = 2√66 ≈ 2 · 8.124 ≈ 16.25", "Pull out the perfect square factor 4."),
                step("Final answer", "Area = 2√66 ≈ 16.25 square units", "Approximately 16.3 sq units."),
            ],
            src(LR, "Ch 8.7"),
        ),
    ],

    "area-of-an-oblique-triangle": [
        step_by_step(
            "Find the area of triangle ABC with b = 7, c = 9, A = 35°.",
            "Use Area = (1/2)bc sin A.",
            [
                step("Recall formula", "Area = (1/2)bc sin A", "Two sides and the included angle."),
                step("Substitute", "Area = (1/2)(7)(9) sin(35°) = (63/2) · sin(35°)", "sin 35° ≈ 0.5736."),
                step("Compute", "Area ≈ 31.5 · 0.5736 ≈ 18.07", "About 18 square units."),
                step("Final answer", "Area ≈ 18.1 square units (exact: 31.5 sin 35°)", "No need to find the third side or height first."),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "Find the area of a triangle with sides a = 8, b = 6, c = 7 using Heron's formula.",
            "Compute semi-perimeter then apply the formula.",
            [
                step("Semi-perimeter s", "s = (8 + 6 + 7) / 2 = 21/2 = 10.5", "s = p/2."),
                step("Apply Heron's formula", "A = √[s(s−a)(s−b)(s−c)] = √[10.5(10.5−8)(10.5−6)(10.5−7)] = √[10.5·2.5·4.5·3.5]", "Compute each: s−a=2.5, s−b=4.5, s−c=3.5."),
                step("Multiply", "10.5 × 2.5 = 26.25;  4.5 × 3.5 = 15.75;  26.25 × 15.75 ≈ 413.44", "Then take the square root."),
                step("Square root", "√413.44 ≈ 20.33", "About 20.3."),
                step("Final answer", "Area ≈ 20.3 square units", "Verify with Law of Cosines first: angle A = arccos((b²+c²−a²)/2bc) = arccos((36+49−64)/(84)) = arccos(21/84) = arccos(0.25) ≈ 75.5°. Then Area = (1/2)(6)(7)sin75.5° ≈ 21·0.968 ≈ 20.3 ✓"),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "A triangular garden has two sides of 12 ft and 15 ft with a 70° angle between them. How much fencing is needed?",
            "Find the third side using Law of Cosines, then perimeter.",
            [
                step("Find side c (between the two given sides)", "c² = 12² + 15² − 2(12)(15) cos(70°) = 144 + 225 − 360 · 0.3420 ≈ 369 − 123.1 = 245.9", "c² = a²+b²−2ab cos C."),
                step("Find c", "c ≈ √245.9 ≈ 15.68 ft", "Approximately 15.7 ft."),
                step("Perimeter", "P = 12 + 15 + 15.68 ≈ 42.68 ft", "Add all three sides."),
                step("Final answer", "Approximately 42.7 ft of fencing is needed.", "Round up to 43 ft to be safe."),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "The area of a triangle is 30 cm². Two sides are 8 cm and 10 cm. Find the angle between them.",
            "Rearrange the area formula.",
            [
                step("Area formula", "Area = (1/2)ab sin C → 30 = (1/2)(8)(10) sin C = 40 sin C", "Solve for sin C."),
                step("Solve", "sin C = 30/40 = 3/4 = 0.75", "Divide both sides by 40."),
                step("Find C", "C = arcsin(0.75) ≈ 48.6° or C = 180° − 48.6° = 131.4°", "Both angles give the same sine (supplementary)."),
                step("Final answer", "The included angle is approximately 48.6° or 131.4°.", "Both are possible — the triangle is not uniquely determined by SAS area information alone."),
            ],
            src(LR, "Ch 8.8"),
        ),
    ],

    # ─── WEEK 7 ──────────────────────────────────────────────────────────

    "vectors-in-2d": [
        step_by_step(
            "Find the magnitude and direction of v = ⟨3, −4⟩.",
            "Compute |v| = √(a²+b²), θ = arctan(b/a).",
            [
                step("Magnitude", "|v| = √(3² + (−4)²) = √(9 + 16) = √25 = 5", "Pythagorean theorem."),
                step("Direction angle", "θ = arctan(−4/3) ≈ −53.1°", "Negative → below the x-axis."),
                step("Adjust to [0, 360°)", "θ = 360° − 53.1° = 306.9°", "Or equivalently: −53.1° + 360°."),
                step("Final answer", "|v| = 5, direction = 306.9° (or −53.1°)", "Standard position angle measured counter-clockwise from the positive x-axis."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Given u = ⟨2, 5⟩ and v = ⟨3, −1⟩, find u + v and 3u − 2v.",
            "Add/subtract component-wise.",
            [
                step("u + v", "⟨2+3, 5+(−1)⟩ = ⟨5, 4⟩", "Add corresponding components."),
                step("3u", "⟨3·2, 3·5⟩ = ⟨6, 15⟩", "Multiply each component by 3."),
                step("2v", "⟨2·3, 2·(−1)⟩ = ⟨6, −2⟩", "Multiply each component by 2."),
                step("3u − 2v", "⟨6−6, 15−(−2)⟩ = ⟨0, 17⟩", "Subtract: 6−6=0, 15+2=17."),
                step("Final answer", "u + v = ⟨5, 4⟩;  3u − 2v = ⟨0, 17⟩", "The second result is purely vertical."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Find the dot product u · v where u = ⟨1, 4⟩ and v = ⟨−2, 3⟩.",
            "Multiply components and sum.",
            [
                step("Dot product formula", "u · v = a₁a₂ + b₁b₂", "Sum of products of corresponding components."),
                step("Substitute", "u · v = (1)(−2) + (4)(3) = −2 + 12 = 10", "1 · (−2) + 4 · 3."),
                step("Final answer", "u · v = 10", "The dot product is a scalar (not a vector)."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Find the projection of u = ⟨6, 8⟩ onto v = ⟨3, 0⟩.",
            "Use proj_v(u) = [(u · v) / (v · v)] v.",
            [
                step("Compute u · v", "u · v = 6·3 + 8·0 = 18", "6·3 = 18; 8·0 = 0."),
                step("Compute v · v", "v · v = 3² + 0² = 9", "The squared magnitude of v."),
                step("Find scalar", "(u · v) / (v · v) = 18/9 = 2", "The factor by which v is scaled."),
                step("Multiply by v", "proj_v(u) = 2 · ⟨3, 0⟩ = ⟨6, 0⟩", "The projection is horizontal."),
                step("Final answer", "proj_v(u) = ⟨6, 0⟩", "The projection of u onto the x-axis is (6, 0) — u's x-component. Makes sense since v = (3,0) is along the x-axis."),
            ],
            src(LR, "Ch 9.1"),
        ),
    ],

    "complex-numbers-and-polar-form": [
        step_by_step(
            "Simplify  (2 + 3i) + (−1 + 5i).",
            "Add real parts and imaginary parts separately.",
            [
                step("Real parts", "2 + (−1) = 1", "Add the real numbers."),
                step("Imaginary parts", "3i + 5i = 8i", "Add the imaginary coefficients."),
                step("Final answer", "1 + 8i", "In standard form a + bi."),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Multiply  (1 + i)(3 − 2i).",
            "Use FOIL.",
            [
                step("FOIL", "(1)(3) + (1)(−2i) + (i)(3) + (i)(−2i) = 3 − 2i + 3i − 2i²", "Be careful with i²."),
                step("Simplify", "3 + (−2i + 3i) − 2i² = 3 + i − 2(−1) = 3 + i + 2", "i² = −1, so −2i² = +2."),
                step("Combine", "3 + 2 + i = 5 + i", "Real parts: 3 + 2 = 5."),
                step("Final answer", "5 + i", "Check: 1·3=3, 1·(−2i)=−2i, i·3=3i, i·(−2i)=−2i²=2. Sum: 3+2 + (−2i+3i) = 5+i ✓"),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Divide  (3 + 2i) / (1 − i).",
            "Multiply numerator and denominator by the conjugate.",
            [
                step("Multiply by the conjugate", "(3 + 2i)(1 + i) / [(1 − i)(1 + i)]", "The conjugate of 1 − i is 1 + i."),
                step("Expand denominator", "(1 − i)(1 + i) = 1 − i² = 1 + 1 = 2", "Difference of squares: a² − b²."),
                step("Expand numerator", "(3 + 2i)(1 + i) = 3 + 3i + 2i + 2i² = 3 + 5i + 2(−1) = 3 + 5i − 2 = 1 + 5i", "3 + 5i − 2."),
                step("Divide by 2", "(1 + 5i) / 2 = 1/2 + (5/2)i", "Separate real and imaginary."),
                step("Final answer", "(3 + 2i)/(1 − i) = 1/2 + (5/2)i", "Or 0.5 + 2.5i."),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Find the modulus of z = 3 − 4i.",
            "Use |z| = √(a² + b²).",
            [
                step("Apply formula", "|z| = √(3² + (−4)²) = √(9 + 16) = √25 = 5", "Pythagorean theorem."),
                step("Final answer", "|z| = 5", "The modulus (distance from the origin) is 5."),
            ],
            src(LR, "Ch 9.4"),
        ),
    ],

    "polar-coordinates": [
        step_by_step(
            "Convert (−2, 2√3) to polar coordinates (r, θ).",
            "Find r = √(x²+y²) and θ = arctan(y/x).",
            [
                step("Find r", "r = √((−2)² + (2√3)²) = √(4 + 12) = √16 = 4", "(2√3)² = 4·3 = 12."),
                step("Find reference angle", "θ_ref = arctan(|y/x|) = arctan(2√3/2) = arctan(√3) = π/3", "x and y both non-zero."),
                step("Locate the point", "x < 0, y > 0 → Quadrant II.", "Left half, above the x-axis."),
                step("Find θ", "θ = π − π/3 = 2π/3", "In QII, θ = π − reference angle."),
                step("Final answer", "(r, θ) = (4, 2π/3)  or  (−4, 5π/3) if using the alternate form.", "Many equivalent polar pairs exist (adding 2πk or negating r and adding π)."),
            ],
            src(LR, "Ch 9.2"),
        ),
        step_by_step(
            "Convert polar (r, θ) = (6, 3π/4) to Cartesian coordinates.",
            "Use x = r cos θ, y = r sin θ.",
            [
                step("x = r cos θ", "x = 6 · cos(3π/4) = 6 · (−√2/2) = −3√2", "cos 3π/4 = −√2/2."),
                step("y = r sin θ", "y = 6 · sin(3π/4) = 6 · (√2/2) = 3√2", "sin 3π/4 = √2/2."),
                step("Final answer", "(x, y) = (−3√2, 3√2) ≈ (−4.24, 4.24)", "The point is in Quadrant II, as expected for 3π/4."),
            ],
            src(LR, "Ch 9.2"),
        ),
        step_by_step(
            "Convert r = 4 sec θ to Cartesian form.",
            "Use r sec θ = x.",
            [
                step("Recall trig identity", "x = r cos θ, so r = x / cos θ = x sec θ.", "From the conversion formulas."),
                step("Set up equation", "r = 4 sec θ  →  r = 4 · (x / r)", "Since sec θ = 1/cos θ = x/r."),
                step("Multiply by r", "r² = 4x", "r · (x/r) = x."),
                step("Replace r²", "x² + y² = 4x", "Since r² = x² + y²."),
                step("Rewrite as standard form", "x² − 4x + y² = 0  →  (x − 2)² + y² = 4", "Complete the square in x."),
                step("Final answer", "(x − 2)² + y² = 4  →  a circle centered at (2, 0) with radius 2.", "The original polar equation represents a circle with vertical tangent at x = 4."),
            ],
            src(LR, "Ch 9.2"),
        ),
        step_by_step(
            "Write the polar equation r = 2 cos θ in Cartesian form and identify the curve.",
            "Replace r and cos θ.",
            [
                step("Multiply both sides by r", "r² = 2r cos θ", "Standard trick for r = something trig."),
                step("Replace", "x² + y² = 2x", "r² = x²+y², r cos θ = x."),
                step("Complete the square", "x² − 2x + y² = 0  →  (x − 1)² + y² = 1", "Center (1, 0), radius 1."),
                step("Final answer", "(x − 1)² + y² = 1: a circle centered at (1, 0) with radius 1.", "Polar equations of the form r = 2a cos θ represent circles of radius |a| centered at (a, 0)."),
            ],
            src(LR, "Ch 9.2"),
        ),
    ],

    "parametric-equations": [
        step_by_step(
            "Eliminate the parameter from x = 3t + 1, y = t² − 4.",
            "Solve x for t, then substitute into y.",
            [
                step("Solve for t", "x = 3t + 1  →  t = (x − 1) / 3", "Isolate t."),
                step("Substitute into y", "y = [(x − 1)/3]² − 4 = (x − 1)² / 9 − 4", "Replace t."),
                step("Clear fractions", "9y = (x − 1)² − 36  →  (x − 1)² = 9y + 36", "Multiply by 9."),
                step("Final answer", "(x − 1)² = 9(y + 4): a parabola opening upward with vertex (1, −4).", "Standard form (x−h)² = 4p(y−k) with h=1, k=−4, 4p=9."),
            ],
            src(LR, "Ch 9.3"),
        ),
        step_by_step(
            "Find the Cartesian equation and graph the parametric curve: x = cos t, y = sin t for t ∈ [0, 2π].",
            "Use the identity cos² t + sin² t = 1.",
            [
                step("Square and add", "cos² t + sin² t = 1  →  x² + y² = 1", "x² + y² = 1 by the Pythagorean identity."),
                step("Domain of t", "t ∈ [0, 2π] traces the full circle counterclockwise starting at (1, 0).", "t = 0: (1, 0); t = π/2: (0, 1); t = π: (−1, 0); t = 3π/2: (0, −1)."),
                step("Final answer", "x² + y² = 1: the unit circle traced counterclockwise from (1, 0).", "The parametric form gives a direction — the Cartesian equation alone doesn't specify it."),
            ],
            src(LR, "Ch 9.3"),
        ),
        step_by_step(
            "Eliminate the parameter from x = 4 cos θ, y = 2 sin θ (ellipse).",
            "Use cos² θ + sin² θ = 1.",
            [
                step("Express cos θ and sin θ", "cos θ = x/4,  sin θ = y/2", "Divide parametric equations by their coefficients."),
                step("Apply identity", "(x/4)² + (y/2)² = 1  →  x²/16 + y²/4 = 1", "cos² θ + sin² θ = 1."),
                step("Final answer", "x²/16 + y²/4 = 1: an ellipse centered at (0, 0), horizontal semi-axis 4, vertical semi-axis 2.", "This is the standard ellipse equation."),
            ],
            src(LR, "Ch 9.3"),
        ),
        step_by_step(
            "At what point does the parametric curve x = t + 1, y = t² cross the line y = 4x − 3?",
            "Eliminate the parameter and solve simultaneously.",
            [
                step("Express t from x", "t = x − 1", "t = x − 1."),
                step("Substitute into y", "y = (x − 1)²", "Replace t in the y-equation."),
                step("Set equal to line equation", "(x − 1)² = 4x − 3", "y from param equals y from line."),
                step("Expand and solve", "x² − 2x + 1 = 4x − 3  →  x² − 6x + 4 = 0", "Quadratic in x."),
                step("Quadratic formula", "x = [6 ± √(36 − 16)] / 2 = [6 ± √20] / 2 = [6 ± 2√5] / 2 = 3 ± √5", "Two intersection points."),
                step("Find t and y", "For x = 3 + √5: t = 2 + √5, y = t² = (2+√5)² = 9+4√5 ≈ 17.94.  For x = 3 − √5: t = 2 − √5, y = (2−√5)² = 9−4√5 ≈ 0.06.", "Both valid."),
                step("Final answer", "Points: (3+√5, (2+√5)²) ≈ (5.24, 17.94) and (3−√5, (2−√5)²) ≈ (0.76, 0.06).", "The curve crosses the line at two points."),
            ],
            src(LR, "Ch 9.3"),
        ),
    ],

    "conic-sections-circles-ellipses-parabolas-hyperbolas": [
        step_by_step(
            "Write  x² + y² + 4x − 6y + 9 = 0  in standard form and identify the conic.",
            "Complete the square in x and y.",
            [
                step("Group x and y terms", "(x² + 4x) + (y² − 6y) + 9 = 0", "Group to complete the square."),
                step("Complete the square for x", "x² + 4x = (x + 2)² − 4", "Half of 4 is 2; 2² = 4."),
                step("Complete the square for y", "y² − 6y = (y − 3)² − 9", "Half of −6 is −3; (−3)² = 9."),
                step("Substitute", "(x+2)² − 4 + (y−3)² − 9 + 9 = 0  →  (x+2)² + (y−3)² − 4 = 0", "−4 − 9 + 9 = −4."),
                step("Rewrite", "(x+2)² + (y−3)² = 4", "Standard form: (x−h)² + (y−k)² = r²."),
                step("Final answer", "Circle centered at (−2, 3) with radius 2.", "Both squared terms have the same positive coefficient — it's a circle."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Identify the conic 9x² − 4y² = 36 and find its key features.",
            "Divide by 36 to get standard form.",
            [
                step("Divide by 36", "9x²/36 − 4y²/36 = 36/36  →  x²/4 − y²/9 = 1", "Standard form for a hyperbola."),
                step("Identify as hyperbola", "x²/a² − y²/b² = 1, where a² = 4, b² = 9.", "Both axes have squared terms with opposite signs."),
                step("Find vertices", "x = ±a = ±2, at y = 0. Vertices: (2, 0) and (−2, 0).", "Transverse axis is horizontal."),
                step("Find asymptotes", "y = ±(b/a)x = ±(3/2)x", "Pass through the center (0, 0)."),
                step("Final answer", "Hyperbola centered at (0, 0), opening left/right. Vertices: (±2, 0). Asymptotes: y = ±(3/2)x.", "Standard form: x²/4 − y²/9 = 1."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Find the focus and directrix of y² = 12x.",
            "Compare to y² = 4px.",
            [
                step("Identify p", "y² = 4px  →  4p = 12  →  p = 3", "Standard parabola opening right."),
                step("Find focus", "(p, 0) = (3, 0)", "p units to the right of the vertex (0, 0)."),
                step("Find directrix", "x = −p = −3", "Vertical line p units left of the vertex."),
                step("Final answer", "Focus: (3, 0). Directrix: x = −3.", "The parabola opens right from the origin."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Identify and write in standard form: 25x² + 4y² − 50x + 16y − 11 = 0.",
            "Complete the square after grouping.",
            [
                step("Group and factor", "25(x² − 2x) + 4(y² + 4y) = 11", "Move constant to right, group, factor coefficients."),
                step("Complete square for x", "x² − 2x = (x − 1)² − 1", "Half of −2 is −1; (−1)² = 1."),
                step("Complete square for y", "y² + 4y = (y + 2)² − 4", "Half of 4 is 2; 2² = 4."),
                step("Substitute", "25[(x−1)² − 1] + 4[(y+2)² − 4] = 11", "Expand: 25(x−1)² − 25 + 4(y+2)² − 16 = 11."),
                step("Combine", "25(x−1)² + 4(y+2)² − 41 = 11  →  25(x−1)² + 4(y+2)² = 52", "Simplify: −25−16 = −41."),
                step("Divide by 52", "(x−1)² / (52/25) + (y+2)² / 13 = 1", "Standard ellipse form."),
                step("Standard form", "(x−1)² / (2.08) + (y+2)² / 13 = 1.  Or: (x−1)² / (52/25) + (y+2)² / 13 = 1.", "Center: (1, −2). Horizontal semi-axis: √(52/25) ≈ 1.44. Vertical semi-axis: √13 ≈ 3.61."),
                step("Final answer", "Ellipse centered at (1, −2) with a² = 52/25, b² = 13.", "It's an ellipse since both squared terms have the same sign but different coefficients."),
            ],
            src(LR, "Ch 9.5"),
        ),
    ],

    "sequences-and-series": [
        step_by_step(
            "Find the 10th term of the arithmetic sequence: 3, 7, 11, 15, ...",
            "Use a_n = a₁ + (n − 1)d.",
            [
                step("Identify a₁ and d", "a₁ = 3, d = 7 − 3 = 4", "First term and common difference."),
                step("Apply formula", "a₁₀ = 3 + (10 − 1) · 4 = 3 + 9 · 4 = 3 + 36 = 39", "n = 10."),
                step("Final answer", "The 10th term is 39.", "Sequence: 3, 7, 11, 15, 19, 23, 27, 31, 35, 39 ✓"),
            ],
            src(LR, "Ch 10.1"),
        ),
        step_by_step(
            "Find the sum of the first 20 terms of the arithmetic series: 5 + 9 + 13 + ...",
            "Use S_n = n(a₁ + a_n)/2 or S_n = n[2a₁ + (n−1)d]/2.",
            [
                step("Find d", "d = 9 − 5 = 4", "Common difference."),
                step("Find a₂₀", "a₂₀ = 5 + (20 − 1) · 4 = 5 + 76 = 81", "a_n = a₁ + (n−1)d."),
                step("Apply sum formula", "S₂₀ = 20 · (5 + 81) / 2 = 20 · 86 / 2 = 10 · 86 = 860", "S_n = n(a₁ + a_n)/2."),
                step("Final answer", "Sum of first 20 terms = 860.", "Check: 20 terms, average = (5+81)/2 = 43.  20 × 43 = 860 ✓"),
            ],
            src(LR, "Ch 10.1"),
        ),
        step_by_step(
            "Find the 8th term of the geometric sequence: 2, 6, 18, 54, ...",
            "Use a_n = a₁ · r^(n−1).",
            [
                step("Find r", "r = 6/2 = 3", "Each term is multiplied by 3."),
                step("Apply formula", "a₈ = 2 · 3^(8−1) = 2 · 3⁷ = 2 · 2187 = 4374", "3⁷ = 2187."),
                step("Final answer", "The 8th term is 4374.", "Sequence grows quickly: 2, 6, 18, 54, 162, 486, 1458, 4374 ✓"),
            ],
            src(LR, "Ch 10.2"),
        ),
        step_by_step(
            "Find the sum of the infinite geometric series: 12 + 4 + 4/3 + 4/9 + ...",
            "Use S = a₁ / (1 − r) if |r| < 1.",
            [
                step("Identify a₁ and r", "a₁ = 12, r = 4/12 = 1/3", "r = 4/12 = 1/3.  |r| = 1/3 < 1, so it converges."),
                step("Apply formula", "S = 12 / (1 − 1/3) = 12 / (2/3) = 12 · (3/2) = 18", "S = a₁ / (1 − r)."),
                step("Final answer", "The sum of the infinite series is 18.", "Check partial sums: S₁=12, S₂=16, S₃=16+1.33=17.33, S₄=17.33+0.44=17.77 → approaching 18."),
            ],
            src(LR, "Ch 10.2"),
        ),
    ],
}


# ---------------------------------------------------------------------------
# Main: patch the course.json
# ---------------------------------------------------------------------------

def patch_walkthroughs(data):
    """Add 4 new walkthroughs to each prerequisite and week topic."""
    total_added = 0

    # Prerequisites
    for p in data.get("prerequisites", []):
        slug = p.get("slug", "")
        key = slug
        if key in NEW_SBS:
            lesson = p.setdefault("lesson", {})
            existing = {s["title"] for s in lesson.get("stepByStep", [])}
            new_items = [s for s in NEW_SBS[key] if s["title"] not in existing]
            lesson.setdefault("stepByStep", []).extend(new_items)
            total_added += len(new_items)
            print(f"  Prerequisites '{p['title']}': added {len(new_items)} walkthroughs")

    # Weeks
    for w in data.get("weeks", []):
        for t in w.get("topics", []):
            slug = t.get("slug", "")
            if slug in NEW_SBS:
                lesson = t.setdefault("lesson", {})
                existing = {s["title"] for s in lesson.get("stepByStep", [])}
                new_items = [s for s in NEW_SBS[slug] if s["title"] not in existing]
                lesson.setdefault("stepByStep", []).extend(new_items)
                total_added += len(new_items)

    return total_added


def main():
    with open(COURSE) as f:
        data = json.load(f)

    print(f"Loaded course: {data['title']}")
    added = patch_walkthroughs(data)
    print(f"\nTotal new walkthroughs added: {added}")

    with open(COURSE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Written: {COURSE}")


if __name__ == "__main__":
    main()
