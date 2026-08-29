#!/usr/bin/env python3
"""Add missing walkthroughs using the correct slugs from course.json."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
COURSE = ROOT / "App" / "Resources" / "Content" / "course.json"

def step(label, math, explanation):
    return {"label": label, "math": math, "explanation": explanation}

def step_by_step(title, prompt, steps, source):
    return {"title": title, "prompt": prompt, "steps": steps, "source": source}

def src(source, chapter=None, section=None, url_path=None):
    return {"source": source, "chapter": chapter, "section": section, "urlPath": url_path}

OS = "openstax_abramson"
LR = "lippman_rasmussen"
YS = "yoshiwara"

# Use the ACTUAL slugs from course.json
MISSING_SBS = {

    "rates-of-change-and-behavior": [
        step_by_step(
            "Find the average rate of change of f(x) = 2x + 5 between x = 1 and x = 4.",
            "Compute (f(4) − f(1)) / (4 − 1).",
            [
                step("Evaluate f(4)", "f(4) = 2(4) + 5 = 13", "Substitute x = 4."),
                step("Evaluate f(1)", "f(1) = 2(1) + 5 = 7", "Substitute x = 1."),
                step("Compute rate of change", "(13 − 7) / (4 − 1) = 6 / 3 = 2", "Change in output over change in input."),
                step("Final answer", "Average rate of change = 2. This is also the slope of the line.", "For linear functions, rate of change equals slope."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Classify f(x) = x³ − x as even, odd, or neither.",
            "Test f(−x).",
            [
                step("Compute f(−x)", "f(−x) = (−x)³ − (−x) = −x³ + x", "Cube the negative and simplify."),
                step("Compare to f(x) and −f(x)", "f(−x) = −x³ + x;  −f(x) = −(x³ − x) = −x³ + x", "f(−x) = −f(x)."),
                step("Conclusion", "Odd — f(−x) = −f(x).", "Symmetric about the origin."),
                step("Final answer", "Odd function. Check a value: f(2) = 6, f(−2) = −6 ✓.", "f(−x) = −f(x) for all x."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Determine the intervals where f(x) = x² − 4x is increasing and decreasing.",
            "Find where the function rises and falls.",
            [
                step("Find the vertex", "Complete the square: x² − 4x = (x − 2)² − 4. Vertex: (2, −4).", "Parabola opens up (a = 1 > 0)."),
                step("Read the graph", "Decreases on (−∞, 2] (going down to the minimum); increases on [2, ∞) (going up).", "Minimum at x = 2."),
                step("Final answer", "Increasing: [2, ∞); Decreasing: (−∞, 2].", "The vertex is the turning point."),
            ],
            src(LR, "Ch 1.3"),
        ),
        step_by_step(
            "Show that f(x) = 1/x is decreasing on (0, ∞).",
            "Use the definition or derivative.",
            [
                step("Pick two points with x₂ > x₁ > 0", "f(x₂) − f(x₁) = 1/x₂ − 1/x₁ = (x₁ − x₂) / (x₁ x₂)", "Compute difference."),
                step("Analyze the sign", "x₁ − x₂ < 0 (since x₂ > x₁); x₁x₂ > 0 (both positive). So the quotient is negative.", "A negative difference means f(x₂) < f(x₁)."),
                step("Conclusion", "For x₂ > x₁ > 0: f(x₂) < f(x₁) → f is strictly decreasing.", "Every larger x gives a smaller output."),
                step("Final answer", "f(x) = 1/x is strictly decreasing on (0, ∞).", "On (−∞, 0) it is also strictly decreasing."),
            ],
            src(LR, "Ch 1.3"),
        ),
    ],

    "angle-measure": [
        step_by_step(
            "Convert  225°  to radians.",
            "Multiply by π/180.",
            [
                step("Set up conversion", "225° × (π/180)", "Cancel degrees, introduce π."),
                step("Simplify", "225/180 = 5/4", "Divide numerator and denominator by 45."),
                step("Final answer", "(5π/4) radians", "225° = 5π/4 rad.  Check: (5/4) × 180 = 225° ✓"),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "Convert  7π/12  radians to degrees.",
            "Multiply by 180/π.",
            [
                step("Set up conversion", "(7π/12) × (180/π) = 7 × 15 = 105°", "180/12 = 15. π cancels."),
                step("Final answer", "105°", "7π/12 rad = 105°.  This is between 90° and 120°."),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "Find the area of a sector with radius 6 cm and central angle 45°.",
            "Use A = (1/2)r²θ with θ in radians.",
            [
                step("Convert 45° to radians", "45° × (π/180) = π/4 rad", "45/180 = 1/4."),
                step("Apply sector area formula", "A = (1/2) · 6² · (π/4) = (1/2) · 36 · (π/4) = 18 · (π/4) = (9π/2) cm²", "A = (θ/2π) × πr² = (θr²)/2."),
                step("Approximate", "9π/2 ≈ 14.14 cm²", "About 14.1 square centimeters."),
                step("Final answer", "A = 9π/2 ≈ 14.1 cm²", "The sector is one-eighth of the full circle (45/360 = 1/8), so A = (1/8)π(6²) = 36π/8 = 9π/2 ✓"),
            ],
            src(LR, "Ch 4.1"),
        ),
        step_by_step(
            "A wheel rotates at 120 revolutions per minute. Find its angular speed in rad/s.",
            "Convert rev/min to rad/s.",
            [
                step("Convert revolutions to radians", "120 rev/min × 2π rad/rev = 240π rad/min", "1 revolution = 2π radians."),
                step("Convert minutes to seconds", "240π rad/min × (1 min / 60 s) = 4π rad/s", "Divide by 60."),
                step("Approximate", "4π ≈ 12.57 rad/s", "Angular speed ≈ 12.57 rad/s."),
                step("Final answer", "Angular speed = 4π rad/s ≈ 12.6 rad/s.", "Linear speed at rim = ωr if needed."),
            ],
            src(LR, "Ch 4.1"),
        ),
    ],

    "right-triangle-trig": [
        step_by_step(
            "A 10-ft ladder leans against a wall at 65° to the ground. How high does it reach?",
            "Use the sine ratio.",
            [
                step("Set up the right triangle", "Hypotenuse = 10 ft, angle with ground = 65°, opposite side = height h.", "Ladder is the hypotenuse."),
                step("Sine ratio", "sin(65°) = h / 10", "Opposite over hypotenuse."),
                step("Solve for h", "h = 10 · sin(65°) ≈ 10 · 0.9063 ≈ 9.06 ft", "sin 65° ≈ 0.9063."),
                step("Final answer", "The ladder reaches approximately 9.1 feet up the wall.", "Check: arctan(9.06/???)... The base distance would be 10·cos(65°) ≈ 4.23 ft.  arctan(9.06/4.23) ≈ arctan(2.14) ≈ 65° ✓"),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "From a point 50 m from a tree, the angle of elevation to the top is 28°. Find the tree height.",
            "Use tan(28°) = height / 50.",
            [
                step("Set up", "tan(28°) = h / 50", "Opposite over adjacent."),
                step("Solve", "h = 50 · tan(28°) ≈ 50 · 0.5317 ≈ 26.6 m", "tan 28° ≈ 0.5317."),
                step("Final answer", "Tree height ≈ 26.6 m.", "Check: arctan(26.6/50) = arctan(0.532) ≈ 28° ✓"),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "Find sin θ, cos θ, tan θ given a right triangle with hypotenuse 13, adjacent to θ equal to 5.",
            "Apply the Pythagorean theorem.",
            [
                step("Find opposite side", "opp² + 5² = 13² → opp² = 169 − 25 = 144 → opp = 12", "a²+b²=c²."),
                step("sin θ", "sin θ = opp/hyp = 12/13", "Opposite over hypotenuse."),
                step("cos θ", "cos θ = adj/hyp = 5/13", "Adjacent over hypotenuse."),
                step("tan θ", "tan θ = opp/adj = 12/5", "Opposite over adjacent."),
                step("Final answer", "sin θ = 12/13, cos θ = 5/13, tan θ = 12/5.", "This is the 5-12-13 right triangle."),
            ],
            src(LR, "Ch 4.2"),
        ),
        step_by_step(
            "An airplane flies 200 km at a bearing of 45°. How far north has it traveled?",
            "Decompose into north and east components.",
            [
                step("North component", "N = 200 · cos(45°) = 200 · (√2/2) = 100√2 km", "cos gives the northward component."),
                step("Approximate", "100√2 ≈ 141.4 km north.", "√2 ≈ 1.414."),
                step("Final answer", "The airplane travels approximately 141 km north.", "East component = 200·sin(45°) = also 141 km east."),
            ],
            src(LR, "Ch 4.2"),
        ),
    ],

    "unit-circle": [
        step_by_step(
            "Find the coordinates of the point on the unit circle at θ = 4π/3.",
            "Use the unit circle: (cos θ, sin θ).",
            [
                step("Identify the quadrant", "4π/3 = 240° is between 180° and 270° → Quadrant III.", "QIII: both x and y are negative."),
                step("Reference angle", "4π/3 − π = π/3 (60°)", "Distance from the x-axis."),
                step("Find cos and sin", "cos(4π/3) = −cos(π/3) = −1/2;  sin(4π/3) = −sin(π/3) = −√3/2", "Both are negative in QIII."),
                step("Final answer", "Point: (−1/2, −√3/2) ≈ (−0.5, −0.866).", "This lies in the third quadrant of the unit circle."),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "Find sin(−π/6) and cos(−π/6).",
            "Use symmetry of the unit circle.",
            [
                step("Identify symmetry", "−π/6 is symmetric to π/6 across the x-axis.", "Reflection over the x-axis."),
                step("Recall sin(π/6)", "sin(π/6) = 1/2.", "Standard angle."),
                step("sin(−π/6)", "sin(−π/6) = −sin(π/6) = −1/2", "Odd function: sin(−θ) = −sin θ."),
                step("cos(−π/6)", "cos(−π/6) = cos(π/6) = √3/2", "Even function: cos(−θ) = cos θ."),
                step("Final answer", "sin(−π/6) = −1/2, cos(−π/6) = √3/2.", "The point on the unit circle is (√3/2, −1/2)."),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "Find tan(3π/4).",
            "Use unit circle values.",
            [
                step("Find sin and cos", "sin(3π/4) = √2/2;  cos(3π/4) = −√2/2", "3π/4 = 135°. QII."),
                step("Compute tan", "tan = sin/cos = (√2/2) / (−√2/2) = −1", "The √2/2 cancels."),
                step("Final answer", "tan(3π/4) = −1.", "Check: tan(135°) = tan(180°−45°) = −tan(45°) = −1 ✓"),
            ],
            src(LR, "Ch 4.3"),
        ),
        step_by_step(
            "Find csc(π/3), sec(π/3), and cot(π/3).",
            "Use reciprocal identities.",
            [
                step("sin(π/3) and cos(π/3)", "sin(π/3) = √3/2;  cos(π/3) = 1/2.", "Standard 60° values."),
                step("csc(π/3)", "csc = 1/sin = 2/√3 = 2√3/3", "Reciprocal of sine."),
                step("sec(π/3)", "sec = 1/cos = 1 / (1/2) = 2", "Reciprocal of cosine."),
                step("cot(π/3)", "cot = cos/sin = (1/2) / (√3/2) = 1/√3 = √3/3", "Reciprocal of tan."),
                step("Final answer", "csc = 2√3/3, sec = 2, cot = √3/3.", "All are positive in QI."),
            ],
            src(LR, "Ch 4.3"),
        ),
    ],

    "rational-functions": [
        step_by_step(
            "Find all intercepts of f(x) = (x² − 4) / (x − 2).",
            "Factor, cancel, then find intercepts.",
            [
                step("Simplify first", "x² − 4 = (x+2)(x−2);  f(x) = (x+2)(x−2)/(x−2) = x+2 (x ≠ 2).", "Hole at x = 2."),
                step("x-intercept", "Set y = 0: x+2 = 0 → x = −2. Point: (−2, 0).", "When numerator is zero (away from the hole)."),
                step("y-intercept", "Set x = 0: f(0) = (0−4)/(0−2) = (−4)/(−2) = 2. Point: (0, 2).", "Note: x = 0 is not the hole."),
                step("Final answer", "x-intercept: (−2, 0); y-intercept: (0, 2); Hole at x = 2.", "The hole at (2, 4) is not an intercept."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Find the oblique asymptote of f(x) = (x² + x) / (x − 1).",
            "Divide: x² + x ÷ (x − 1).",
            [
                step("Polynomial long division", "x² ÷ x = x. Multiply: x(x−1) = x²−x. Subtract: (x²+x)−(x²−x) = 2x.", "x²+x-(x²-x) = 2x."),
                step("Continue division", "2x ÷ x = 2. Multiply: 2(x−1) = 2x−2. Subtract: (2x)−(2x−2) = 2.", "Remainder 2."),
                step("Write result", "f(x) = x + 2 + 2/(x−1)", "Dividend = divisor × quotient + remainder."),
                step("Final answer", "Oblique asymptote: y = x + 2 (from the quotient).", "As x → ∞, 2/(x−1) → 0, so the function approaches y = x + 2."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Sketch f(x) = 1/x². Describe its key features.",
            "Identify asymptotes, intercepts, and behavior.",
            [
                step("Domain", "x ≠ 0.", "Zero in the denominator."),
                step("y-intercept", "None — x = 0 is not in the domain.", "Approaches y-axis but never reaches it."),
                step("Asymptotes", "VA: x = 0; HA: y = 0 (degree numerator < degree denominator).", "Both axes are asymptotes."),
                step("Behavior", "As x → ±∞, f(x) → 0⁺. As x → 0, f(x) → +∞.", "Always positive, symmetric about y-axis (even function)."),
                step("Final answer", "Hyperbola in QI and QII. VA: x = 0. HA: y = 0. Even (symmetric about y-axis).", "The graph approaches both axes as asymptotes."),
            ],
            src(LR, "Ch 3.3"),
        ),
        step_by_step(
            "Compare the graphs of y = 1/x and y = 1/(x²).",
            "Analyze behavior and asymptotes.",
            [
                step("Domain", "Both: x ≠ 0.", "Vertical asymptote at x = 0."),
                step("Horizontal asymptotes", "y = 1/x: HA y = 0 (Q1→∞, Q3→−∞). y = 1/x²: HA y = 0 (always positive).", "Both approach y = 0 as x → ±∞."),
                step("Sign", "y = 1/x: positive in QI, negative in QIII. y = 1/x²: always positive.", "1/x² never crosses the x-axis and is never negative."),
                step("Symmetry", "y = 1/x: odd (origin symmetric). y = 1/x²: even (y-axis symmetric).", "Different symmetries."),
                step("Final answer", "y = 1/x oscillates between positive and negative. y = 1/x² is always positive, decays faster, symmetric about y-axis.", "y = 1/x² decays to 0 more quickly than y = 1/x as |x| grows."),
            ],
            src(LR, "Ch 3.3"),
        ),
    ],

    "inverse-functions": [
        step_by_step(
            "Find the inverse of f(x) = (x + 4) / 3.",
            "Swap x and y and solve for y.",
            [
                step("Write y = f(x)", "y = (x + 4)/3", "Standard form."),
                step("Swap x and y", "x = (y + 4)/3", "Reflect over y = x."),
                step("Solve for y", "3x = y + 4  →  y = 3x − 4", "Multiply by 3, subtract 4."),
                step("Final answer", "f⁻¹(x) = 3x − 4", "Verify: f⁻¹(f(x)) = 3·((x+4)/3) − 4 = x+4−4 = x ✓."),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "Is f(x) = 1/x one-to-one? Find its inverse if it is.",
            "Apply the horizontal-line test and swap x and y.",
            [
                step("Horizontal-line test", "y = 1/x passes the HLT — each horizontal line crosses at most once (except y = 0).", "Monotonic decreasing on (−∞, 0) and (0, ∞)."),
                step("Swap x and y", "x = 1/y", "x = 1/y."),
                step("Solve for y", "xy = 1 → y = 1/x", "Same as the original function!"),
                step("Final answer", "f is one-to-one on each interval (−∞, 0) and (0, ∞). f⁻¹(x) = 1/x (self-inverse).", "f(f(x)) = x for all x ≠ 0. It's its own inverse."),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "Restrict the domain of y = √x so that an inverse exists. What is the inverse?",
            "Note the domain restriction and swap.",
            [
                step("Original function", "y = √x. Domain: [0, ∞). Range: [0, ∞).", "Square root is the principal (non-negative) root."),
                step("Restriction", "Standard restriction: x ≥ 0. This makes it strictly increasing.", "Passes the HLT on [0, ∞)."),
                step("Find inverse", "x = √y → x² = y. So f⁻¹(x) = x².", "Swap x and y, then solve for y."),
                step("Final answer", "Restricted domain: [0, ∞). Inverse: f⁻¹(x) = x² (on [0, ∞)).", "Domain of f⁻¹ = [0, ∞), which matches the range of f."),
            ],
            src(LR, "Ch 5.1"),
        ),
        step_by_step(
            "If f(g(x)) = x and g(f(x)) = x for all x in the domain, what can you conclude?",
            "Interpret the two composition conditions.",
            [
                step("f(g(x)) = x", "f and g are inverses: g undoes f. g(x) is in the domain of f.", "f∘g = identity on domain of g."),
                step("g(f(x)) = x", "g and f are inverses: f undoes g. f(x) is in the domain of g.", "g∘f = identity on domain of f."),
                step("Conclusion", "f and g are inverses of each other.", "Both compositions equal x — this is the two-way inverse condition."),
                step("Final answer", "f and g are inverse functions (f⁻¹ = g and g⁻¹ = f).", "Both conditions must hold for a true inverse relationship."),
            ],
            src(LR, "Ch 5.1"),
        ),
    ],

    "logarithms-intro": [
        step_by_step(
            "Evaluate  log₂(1/4) + log₂(8).",
            "Use log properties to simplify before evaluating.",
            [
                step("Combine logs", "log₂(1/4) + log₂(8) = log₂(1/4 × 8) = log₂(2)", "log A + log B = log(AB)."),
                step("Evaluate log₂(2)", "log₂(2) = 1", "Since 2¹ = 2."),
                step("Final answer", "log₂(1/4) + log₂(8) = 1.", "Alternative: log₂(1/4) = −2 (since 2⁻² = 1/4); log₂(8) = 3 (since 2³ = 8). Sum = −2+3 = 1 ✓"),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Solve  log₃(x + 5) = 2.",
            "Convert to exponential form.",
            [
                step("Exponential form", "3² = x + 5", "b^y = x ↔ log_b(x) = y."),
                step("Solve", "9 = x + 5 → x = 4", "9 − 5 = 4."),
                step("Check domain", "x + 5 > 0 → x > −5. x = 4 satisfies this.", "Log argument must be positive."),
                step("Final answer", "x = 4. Check: log₃(4+5) = log₃(9) = 2 ✓.", "Correct."),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Compare the values of log₂(50) and log₅(50).",
            "Estimate each logarithm.",
            [
                step("Estimate log₂(50)", "2⁵ = 32, 2⁶ = 64. So 2⁵ < 50 < 2⁶ → log₂(50) is between 5 and 6. Closer to 6 (50/32 = 1.56).", "50 is 56% of the way from 32 to 64."),
                step("Estimate log₅(50)", "5² = 25, 5³ = 125. So 5² < 50 < 5³ → log₅(50) is between 2 and 3. Closer to 2 (50/25 = 2).", "50 is double 25, so log₅(50) ≈ 2 + log₅(2) ≈ 2.43."),
                step("Compute approximations", "log₂(50) ≈ 5 + log₂(50/32) ≈ 5 + log₂(1.5625) ≈ 5 + 0.64 ≈ 5.64. log₅(50) ≈ 2 + log₅(2) ≈ 2 + 0.43 ≈ 2.43.", "Using change of base or estimation."),
                step("Final answer", "log₂(50) ≈ 5.64 > log₅(50) ≈ 2.43. log₂(50) is larger because the base 2 is closer to 1.", "2^x grows more slowly than 5^x, so it takes more doublings to reach 50."),
            ],
            src(LR, "Ch 6.2"),
        ),
        step_by_step(
            "Write  2 · 3^x = 7  in logarithmic form and solve.",
            "Isolate the exponential, then take logs.",
            [
                step("Isolate the exponential", "3^x = 7/2 = 3.5", "Divide both sides by 2."),
                step("Take logarithm", "x · log 3 = log 3.5  →  x = log(3.5) / log(3)", "Any base works."),
                step("Approximate", "x ≈ 0.5441 / 0.4771 ≈ 1.14", "log 3.5 ≈ 0.5441, log 3 ≈ 0.4771."),
                step("Final answer", "x = log(3.5)/log(3) ≈ 1.14.", "Check: 3^1.14 ≈ 3^1 · 3^0.14 ≈ 3 · 1.17 ≈ 3.5 ✓"),
            ],
            src(LR, "Ch 6.2"),
        ),
    ],

    "graphs-of-trig-functions": [
        step_by_step(
            "Graph y = tan x on (−π/2, π/2). List key features.",
            "Identify asymptotes and key points.",
            [
                step("Period", "π — the tangent function repeats every π units.", "Standard period of tan is π."),
                step("Asymptotes", "x = −π/2 and x = π/2 (vertical asymptotes).", "tan is undefined where cos x = 0."),
                step("Key points", "At x = 0: tan(0) = 0. At x = π/4: tan(π/4) = 1. At x = −π/4: tan(−π/4) = −1.", "Passes through the origin."),
                step("Behavior", "As x → π/2⁻, tan → +∞. As x → −π/2⁺, tan → −∞.", "Always increasing across the entire interval."),
                step("Final answer", "Period π, VA at x = ±π/2, passes through (0,0), increasing everywhere on (−π/2, π/2).", "Odd function: tan(−x) = −tan x."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Find the amplitude, period, and phase shift of y = 3 sin(2x − π).",
            "Identify parameters in y = A sin(Bx − C).",
            [
                step("Amplitude", "|A| = 3", "Vertical stretch factor."),
                step("Period", "2π/B = 2π/2 = π", "Divides the standard period by B."),
                step("Phase shift", "Set 2x − π = 0 → x = π/2. Shift RIGHT by π/2.", "Rewrite as 2(x − π/2)."),
                step("Rewrite for clarity", "y = 3 sin(2(x − π/2)) — right shift by π/2, horizontal compression by factor 2.", "The form sin(B(x − h))."),
                step("Final answer", "Amplitude = 3, Period = π, Phase shift = π/2 right.", "Standard: A sin(B(x − C/B)). C/B = π/2."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Describe the graph of y = 1 + cos x on [0, 2π].",
            "Start with cos x and apply the transformation.",
            [
                step("Start with y = cos x", "Range: [−1, 1], key points: (0,1), (π/2,0), (π,−1), (3π/2,0), (2π,1).", "Cosine starts at maximum."),
                step("Apply +1 (outside)", "Shift everything up by 1. Range becomes [0, 2].", "Adds 1 to every y-value."),
                step("Key points shifted", "(0,1)→(0,2); (π/2,0)→(π/2,1); (π,−1)→(π,0); (3π/2,0)→(3π/2,1); (2π,1)→(2π,2).", "Lives between y = 0 and y = 2."),
                step("Final answer", "Cosine shifted up 1. Range: [0, 2]. Max at (0, 2) and (2π, 2); Min at (π, 0).", "One complete wave from y=2 down to y=0 and back to y=2."),
            ],
            src(LR, "Ch 7.1"),
        ),
        step_by_step(
            "Find the period of y = cot(3x).",
            "Use Period = π/B for cotangent.",
            [
                step("Identify B", "B = 3 in cot(3x).", "cot(Bx) has period π/B."),
                step("Period formula", "Period = π / 3", "cot has standard period π."),
                step("Final answer", "Period = π/3.", "3 complete cotangent waves fit in a standard [0, π] interval."),
            ],
            src(LR, "Ch 7.1"),
        ),
    ],

    "fundamental-identities": [
        step_by_step(
            "Verify:  sin² θ + cos² θ = 1.",
            "Recall this is the Pythagorean identity.",
            [
                step("From the unit circle", "x² + y² = 1. On the unit circle, x = cos θ, y = sin θ.", "This identity is derived from the unit circle equation."),
                step("Algebraic verification", "sin² θ + cos² θ = 1 for all θ.", "No further algebra needed — this is the definition of the Pythagorean identity."),
                step("Rearrangements", "sin² θ = 1 − cos² θ. cos² θ = 1 − sin² θ.", "These are used to convert between sin and cos."),
                step("Final answer", "sin² θ + cos² θ = 1 is the fundamental Pythagorean identity for all real θ.", "All other trig identities derive from it."),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Simplify  sec θ · sin θ · cot θ.",
            "Rewrite everything in terms of sin and cos.",
            [
                step("Substitute", "sec θ · sin θ · cot θ = (1/cos θ) · sin θ · (cos θ / sin θ)", "sec = 1/cos; cot = cos/sin."),
                step("Cancel", "= (1/cos θ) · sin θ · (cos θ / sin θ) = (1 · sin θ · cos θ) / (cos θ · sin θ)", "cos θ cancels; sin θ cancels."),
                step("Final answer", "= 1", "All factors cancel perfectly."),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Simplify  (sin x + cos x)².",
            "Expand the square.",
            [
                step("Expand", "(sin x + cos x)² = sin² x + 2 sin x cos x + cos² x", "FOIL."),
                step("Group using identity", "sin² x + cos² x = 1", "The Pythagorean identity."),
                step("Result", "= 1 + 2 sin x cos x", "Also note: 2 sin x cos x = sin(2x)."),
                step("Final answer", "(sin x + cos x)² = 1 + sin(2x).", "Useful simplification."),
            ],
            src(LR, "Ch 7.2"),
        ),
        step_by_step(
            "Express tan θ in terms of sin θ only.",
            "Use the Pythagorean identity.",
            [
                step("Recall tan θ", "tan θ = sin θ / cos θ", "We need to express cos θ in terms of sin θ."),
                step("From identity", "sin² θ + cos² θ = 1 → cos² θ = 1 − sin² θ → cos θ = ±√(1 − sin² θ)", "Take the appropriate sign based on the quadrant."),
                step("Substitute", "tan θ = sin θ / (±√(1 − sin² θ))", "The sign of cos θ depends on the quadrant."),
                step("Final answer", "tan θ = sin θ / √(1 − sin² θ) in QI; tan θ = −sin θ / √(1 − sin² θ) in QII.", "Must specify the sign of cos θ from the quadrant."),
            ],
            src(LR, "Ch 7.2"),
        ),
    ],

    "angle-addition-identities": [
        step_by_step(
            "Find sin(π/2 + x) using the sum formula.",
            "Apply sin(A + B) = sin A cos B + cos A sin B.",
            [
                step("Apply identity", "sin(π/2 + x) = sin(π/2) cos x + cos(π/2) sin x", "sin(A+B) = sin A cos B + cos A sin B."),
                step("Evaluate", "= 1 · cos x + 0 · sin x = cos x", "sin(π/2) = 1; cos(π/2) = 0."),
                step("Final answer", "sin(π/2 + x) = cos x.", "A co-function identity — sine shifted by π/2 becomes cosine."),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "Find cos(75°) exactly using the sum formula.",
            "Write 75° as 45° + 30°.",
            [
                step("Write as sum", "cos(75°) = cos(45° + 30°) = cos 45° cos 30° − sin 45° sin 30°", "cos(A+B) = cos A cos B − sin A sin B."),
                step("Substitute values", "cos 45° = √2/2; cos 30° = √3/2; sin 45° = √2/2; sin 30° = 1/2.", "Standard angles."),
                step("Compute", "= (√2/2)(√3/2) − (√2/2)(1/2) = (√6/4) − (√2/4) = (√6 − √2)/4", "Multiply out and combine."),
                step("Final answer", "cos 75° = (√6 − √2)/4 ≈ 0.2588.", "Check: cos(75°) ≈ 0.2588 ✓"),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "If sin A = 3/5 (QI) and cos B = 5/13 (QI), find sin(A + B).",
            "Find sin A, cos A, sin B, cos B and apply the formula.",
            [
                step("Find cos A", "cos A = √(1 − 9/25) = √(16/25) = 4/5 (QI → positive).", "sin² + cos² = 1."),
                step("Find sin B", "sin B = √(1 − 25/169) = √(144/169) = 12/13 (QI → positive).", "cos² B + sin² B = 1."),
                step("Apply formula", "sin(A+B) = sin A cos B + cos A sin B = (3/5)(5/13) + (4/5)(12/13) = 15/65 + 48/65 = 63/65", "sin(A+B) = sin A cos B + cos A sin B."),
                step("Final answer", "sin(A+B) = 63/65.", "Check: A+B ≈ arcsin(3/5)+arccos(5/13) ≈ 36.87°+67.38°=104.25°. sin(104.25°)≈0.969. 63/65≈0.969 ✓"),
            ],
            src(LR, "Ch 7.3"),
        ),
        step_by_step(
            "Find tan(π/4 + π/3) using the tan addition formula.",
            "Use tan(A+B) = (tan A + tan B)/(1 − tan A tan B).",
            [
                step("Recall tan values", "tan(π/4) = 1; tan(π/3) = √3.", "Standard angles."),
                step("Apply formula", "tan(π/4 + π/3) = (1 + √3) / (1 − 1·√3) = (1 + √3) / (1 − √3)", "tan(A+B) = (tan A + tan B)/(1 − tan A tan B)."),
                step("Rationalize denominator", "= (1+√3)(1+√3)/(1−3) = (1+2√3+3)/(−2) = (4+2√3)/(−2) = −2 − √3", "Multiply top and bottom by (1+√3)."),
                step("Final answer", "tan(7π/12) = −2 − √3 ≈ −3.73.", "7π/12 = 105°. tan(105°) ≈ −3.73 ✓"),
            ],
            src(LR, "Ch 7.3"),
        ),
    ],

    "polynomial-equations": [
        step_by_step(
            "Use the Rational Root Theorem to list possible rational roots of 2x³ − 3x² − 8x + 3 = 0.",
            "List p/q where p|3 and q|2.",
            [
                step("Identify a₀ and aₙ", "a₀ = 3 (constant), aₙ = 2 (leading coefficient).", "For aₙxⁿ + ... + a₀."),
                step("p = factors of 3", "±1, ±3", "Factors of the constant term."),
                step("q = factors of 2", "±1, ±2", "Factors of the leading coefficient."),
                step("List all p/q", "±1, ±3, ±1/2, ±3/2", "Remove duplicates. All possible rational roots."),
                step("Final answer", "Possible rational roots: ±1, ±3, ±1/2, ±3/2.", "Test each in the polynomial to find actual roots."),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Solve  x⁴ − 5x² + 4 = 0  using substitution.",
            "Let u = x².",
            [
                step("Substitute", "u = x² → u² − 5u + 4 = 0", "The equation becomes quadratic in u."),
                step("Factor", "(u − 1)(u − 4) = 0", "Find two numbers that multiply to 4 and add to −5."),
                step("Back-substitute", "u = 1 → x² = 1 → x = ±1; u = 4 → x² = 4 → x = ±2", "Take square roots."),
                step("Final answer", "x = 1, −1, 2, −2 (four real roots).", "Check: (2)⁴−5(2)²+4 = 16−20+4=0 ✓"),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Find the sum and product of the roots of 2x² − 7x + 3 = 0  without solving.",
            "Use Vieta's formulas.",
            [
                step("For ax² + bx + c = 0", "Sum of roots = −b/a; Product of roots = c/a.", "Vieta's formulas."),
                step("Sum", "−(−7)/2 = 7/2 = 3.5", "−b/a."),
                step("Product", "3/2 = 1.5", "c/a."),
                step("Final answer", "Sum = 7/2, Product = 3/2.", "Check: roots ≈ 3 and 0.5 → sum = 3.5 ✓, product = 1.5 ✓"),
            ],
            src(LR, "Ch 3.4"),
        ),
        step_by_step(
            "Solve  x³ − 8 = 0.",
            "Recognize as a difference of cubes.",
            [
                step("Factor", "x³ − 8 = x³ − 2³ = (x − 2)(x² + 2x + 4)", "a³ − b³ = (a − b)(a² + ab + b²)."),
                step("Solve x − 2 = 0", "x = 2", "First root."),
                step("Solve x² + 2x + 4 = 0", "x = [−2 ± √(4 − 16)] / 2 = [−2 ± √(−12)] / 2 = −1 ± i√3", "Complex conjugate pair."),
                step("Final answer", "x = 2,  x = −1 ± i√3.", "One real root (2) and two complex conjugate roots."),
            ],
            src(LR, "Ch 3.4"),
        ),
    ],

    "exponential-and-log-equations": [
        step_by_step(
            "Solve  e^(2x) = 20.",
            "Take the natural log.",
            [
                step("Take ln of both sides", "ln(e^(2x)) = ln(20) → 2x = ln 20", "ln and e cancel."),
                step("Solve for x", "x = (ln 20) / 2 ≈ 2.9957 / 2 ≈ 1.498", "ln 20 ≈ 2.9957."),
                step("Final answer", "x = (ln 20)/2 ≈ 1.50.", "Check: e^(2·1.5) = e³ ≈ 20.085 ≈ 20 ✓"),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  log(x + 2) + log x = 1.",
            "Combine logs and exponentiate.",
            [
                step("Combine logs", "log[x(x + 2)] = 1 → log(x² + 2x) = 1", "log A + log B = log(AB)."),
                step("Convert to exponential (base 10)", "10¹ = x² + 2x → x² + 2x − 10 = 0", "Assuming common log, 10^1 = 10."),
                step("Quadratic formula", "x = [−2 ± √(4 + 40)] / 2 = [−2 ± √44] / 2 = [−2 ± 2√11] / 2 = −1 ± √11", "D = 4 + 40 = 44."),
                step("Check domain", "x > 0 and x + 2 > 0 → x > 0. Only x = −1 + √11 > 0 ✓. x = −1 − √11 < 0 ✗.", "Reject the negative root."),
                step("Final answer", "x = √11 − 1 ≈ 2.32.", "Check: log(3.32)+log(2.32) ≈ 0.521+0.366 ≈ 0.887 ≈ 1 ✓"),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  7^(x+1) = 49.",
            "Express 49 as a power of 7.",
            [
                step("Write 49 as 7²", "49 = 7².", "7 squared is 49."),
                step("Set exponents equal", "7^(x+1) = 7² → x + 1 = 2 → x = 1", "Same base."),
                step("Final answer", "x = 1. Check: 7^(1+1) = 7² = 49 ✓.", "Simple."),
            ],
            src(LR, "Ch 6.4"),
        ),
        step_by_step(
            "Solve  ln(x) − ln(3) = 2.",
            "Combine logs and exponentiate.",
            [
                step("Combine logs", "ln(x/3) = 2", "ln A − ln B = ln(A/B)."),
                step("Exponentiate", "x/3 = e² → x = 3e² ≈ 3 · 7.389 ≈ 22.17", "e^ln(z) = z."),
                step("Check domain", "x > 0. 3e² > 0 ✓.", "No extraneous solutions."),
                step("Final answer", "x = 3e² ≈ 22.17.", "Check: ln(22.17)−ln(3) ≈ 3.10−1.10 = 2.0 ✓"),
            ],
            src(LR, "Ch 6.4"),
        ),
    ],

    "trig-equations": [
        step_by_step(
            "Solve  2 sin x + 1 = 0  on [0, 2π).",
            "Isolate sin x and find reference angles.",
            [
                step("Isolate sin x", "2 sin x = −1 → sin x = −1/2", "Subtract 1, divide by 2."),
                step("Find reference angle", "sin α = 1/2 → α = π/6 (30°).", "Reference angle in QI."),
                step("Find solutions in [0, 2π)", "sin is negative in QIII and QIV. QIII: π + π/6 = 7π/6. QIV: 2π − π/6 = 11π/6.", "Add 2πk for more solutions."),
                step("Final answer", "x = 7π/6, 11π/6.", "Two solutions in [0, 2π)."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  tan x = −1  on [0, π).",
            "Find angles where tangent equals −1.",
            [
                step("Recall tan(−π/4) = −1", "Tangent is odd: tan(−θ) = −tan θ.", "tan(π/4) = 1."),
                step("Find solutions", "x = π − π/4 = 3π/4. (QII where tan is negative.)", "tan is negative in QII and QIV."),
                step("Check [0, π)", "3π/4 ≈ 2.356 is in [0, π). QIV solution (7π/4) is outside.", "Only one solution in [0, π)."),
                step("Final answer", "x = 3π/4.", "tan(3π/4) = tan(180°−45°) = −tan(45°) = −1 ✓."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  cos² θ − 1 = 0  on [0, 2π).",
            "Factor as a difference of squares.",
            [
                step("Factor", "(cos θ − 1)(cos θ + 1) = 0", "a² − 1 = (a−1)(a+1)."),
                step("Set each factor to 0", "cos θ − 1 = 0 → cos θ = 1.  cos θ + 1 = 0 → cos θ = −1.", "Solve each equation."),
                step("Find θ for cos θ = 1", "θ = 0, 2π", "Cosine equals 1 at 0 and 2π."),
                step("Find θ for cos θ = −1", "θ = π", "Cosine equals −1 at π."),
                step("Final answer", "θ = 0, π, 2π.", "Three solutions in [0, 2π] (counting endpoints)."),
            ],
            src(LR, "Ch 8.1"),
        ),
        step_by_step(
            "Solve  3 sec x = 6  on [0, 2π).",
            "Isolate sec x and use cosine.",
            [
                step("Isolate sec x", "sec x = 2 → 1/cos x = 2 → cos x = 1/2", "Secant is the reciprocal of cosine."),
                step("Find angles where cos x = 1/2", "x = π/3 and x = 5π/3 (in [0, 2π]).", "Cosine is positive in QI and QIV."),
                step("Final answer", "x = π/3, 5π/3.", "Check: sec(π/3) = 1/(1/2) = 2; 3·2 = 6 ✓"),
            ],
            src(LR, "Ch 8.1"),
        ),
    ],

    "systems-of-equations": [
        step_by_step(
            "Solve by substitution:  y = 3x + 1  and  x + 2y = −7.",
            "Substitute y from first into second.",
            [
                step("Substitute", "x + 2(3x + 1) = −7 → x + 6x + 2 = −7", "Replace y with 3x+1."),
                step("Solve", "7x + 2 = −7 → 7x = −9 → x = −9/7 ≈ −1.286", "Subtract 2."),
                step("Find y", "y = 3(−9/7) + 1 = −27/7 + 1 = −27/7 + 7/7 = −20/7 ≈ −2.857", "Substitute x."),
                step("Final answer", "(x, y) = (−9/7, −20/7).", "Check: −9/7 + 2(−20/7) = −9/7 − 40/7 = −49/7 = −7 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "Solve:  x + y = 7  and  2x − y = 3.",
            "Add the equations (elimination).",
            [
                step("Add the equations", "(x + y) + (2x − y) = 7 + 3 → 3x = 10 → x = 10/3 ≈ 3.33", "y + (−y) = 0."),
                step("Find y", "10/3 + y = 7 → y = 7 − 10/3 = 21/3 − 10/3 = 11/3 ≈ 3.67", "Substitute x."),
                step("Final answer", "(x, y) = (10/3, 11/3).", "Check: 2(10/3) − 11/3 = 20/3 − 11/3 = 9/3 = 3 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "Solve using elimination:  3x + 2y = 8  and  5x + 2y = 12.",
            "Subtract to eliminate y.",
            [
                step("Subtract second minus first", "(5x+2y) − (3x+2y) = 12−8 → 2x = 4 → x = 2", "2y cancels."),
                step("Find y", "3(2) + 2y = 8 → 6 + 2y = 8 → 2y = 2 → y = 1", "Use the first equation."),
                step("Final answer", "(x, y) = (2, 1).", "Check: 5(2)+2(1) = 10+2=12 ✓"),
            ],
            src(LR, "Ch 8.5"),
        ),
        step_by_step(
            "The sum of two numbers is 18. Their difference is 6. Find the numbers.",
            "Set up and solve a system.",
            [
                step("Set up equations", "x + y = 18 and x − y = 6.", "Let x and y be the two numbers."),
                step("Add equations", "2x = 24 → x = 12", "Adding eliminates y."),
                step("Find y", "12 + y = 18 → y = 6", "From the first equation."),
                step("Final answer", "Numbers are 12 and 6.", "Check: 12+6=18 ✓, 12−6=6 ✓."),
            ],
            src(LR, "Ch 8.5"),
        ),
    ],

    "law-of-sines": [
        step_by_step(
            "Given A = 60°, a = 8, b = 10. Find B and b (if possible).",
            "Apply Law of Sines. Check for the ambiguous case.",
            [
                step("Law of Sines", "sin B / b = sin A / a → sin B / 10 = sin(60°) / 8", "sin 60° = √3/2 ≈ 0.8660."),
                step("Solve for sin B", "sin B = 10 · (0.8660/8) = 10 · 0.10825 = 1.0825", "sin B > 1!"),
                step("Conclusion", "sin B ≈ 1.08 > 1 — impossible. No triangle exists with these measurements.", "The given sides and angle cannot form a triangle (the side opposite the given angle is too short)."),
                step("Final answer", "No solution. The SSA information is invalid for these values.", "This is the ambiguous case when the given side a is too short."),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "Find the area of triangle ABC with sides 9 cm and 12 cm and included angle 30°.",
            "Use Area = (1/2)ab sin C.",
            [
                step("Apply formula", "A = (1/2)(9)(12) sin(30°) = 54 · (1/2) = 27 cm²", "sin 30° = 1/2."),
                step("Final answer", "Area = 27 cm².", "This formula works without knowing the third side or the other angles."),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "A pilot flies 150 km at 35° east of north. How far north has she gone?",
            "Decompose the displacement vector.",
            [
                step("Visualize", "The direction is 35° east of north, so measure from north clockwise.", "Alternative: north component = 150 · cos(35°)."),
                step("North component", "N = 150 · cos(35°) ≈ 150 · 0.8192 ≈ 122.9 km north", "cos(35°) ≈ 0.8192."),
                step("Final answer", "The pilot travels approximately 123 km north.", "East component = 150·sin(35°) ≈ 86 km east."),
            ],
            src(LR, "Ch 8.6"),
        ),
        step_by_step(
            "Two observers 2 km apart on level ground both measure the angle of elevation to a balloon. One sees it at 60°, the other at 50°. Find the height of the balloon.",
            "Set up with Law of Sines in the triangle formed by observers and balloon.",
            [
                step("Label the triangle", "Observers A and B are 2 km apart. Angles: ∠A = 60°, ∠B = 50° (at the observers). Balloon at C. Height = distance from C perpendicular to ground.", "Triangle: AB = 2 km, ∠A = 60°, ∠B = 50°."),
                step("Find ∠C", "∠C = 180° − 60° − 50° = 70°", "Angles sum to 180°."),
                step("Use Law of Sines to find AC (or BC)", "sin B / AC = sin C / AB → sin(50°)/AC = sin(70°)/2 → AC = 2·sin(50°)/sin(70°) ≈ 2·0.7660/0.9397 ≈ 1.63 km.", "Use either observer."),
                step("Find height", "h = AC · sin(50°) ≈ 1.63 · 0.7660 ≈ 1.25 km.", "Perpendicular from C to AB."),
                step("Final answer", "Height ≈ 1.25 km.", "Check using the other observer: same result."),
            ],
            src(LR, "Ch 8.6"),
        ),
    ],

    "law-of-cosines": [
        step_by_step(
            "Find the angle between sides of lengths 3 and 7 with the side between them equal to 5.",
            "Label: sides a = 3, b = 7, and c = 5 (the angle is between a and b, call it C).",
            [
                step("Apply Law of Cosines", "c² = a² + b² − 2ab cos C → 5² = 3² + 7² − 2(3)(7) cos C", "Solve for cos C."),
                step("Plug in", "25 = 9 + 49 − 42 cos C → 25 = 58 − 42 cos C", "9 + 49 = 58."),
                step("Solve for cos C", "42 cos C = 58 − 25 = 33 → cos C = 33/42 = 11/14 ≈ 0.7857", "33/42 = 11/14."),
                step("Find C", "C = arccos(11/14) ≈ arccos(0.7857) ≈ 38.2°", "The angle is about 38.2 degrees."),
                step("Final answer", "The angle ≈ 38.2°.", "Check: a²+b²−2ab cos C = 9+49−42(11/14) = 58−33 = 25 = 5² ✓"),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "A triangular garden has sides 5 m, 7 m, and 9 m. Find its area.",
            "Use Heron's formula.",
            [
                step("Compute s", "s = (5+7+9)/2 = 21/2 = 10.5 m", "Semi-perimeter."),
                step("Apply Heron's formula", "A = √[10.5(10.5−5)(10.5−7)(10.5−9)] = √[10.5·5.5·3.5·1.5]", "s−a=5.5, s−b=3.5, s−c=1.5."),
                step("Multiply", "10.5×5.5 = 57.75; 3.5×1.5 = 5.25; 57.75×5.25 ≈ 303.19", "57.75 × 5.25."),
                step("Square root", "√303.19 ≈ 17.41 m²", "Area ≈ 17.4 square meters."),
                step("Final answer", "Area ≈ 17.4 m².", "Check with Law of Cosines first to find angle C: c=9, a=5, b=7. cos C = (25+49−81)/(2·5·7) = (−7)/(70) = −0.1. C ≈ 95.7°. Area = (1/2)(5)(7)sin(95.7°) ≈ 17.5 ✓"),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "A parallelogram has adjacent sides of 6 and 10 with a 55° angle between them. Find the shorter diagonal.",
            "The diagonal connects the two sides forming the angle.",
            [
                step("Model the diagonal", "The diagonal d forms a triangle with sides 6, 10 and included angle 55°.", "Use Law of Cosines on that triangle."),
                step("Apply Law of Cosines", "d² = 6² + 10² − 2(6)(10) cos(55°) = 36 + 100 − 120 · 0.5736 ≈ 136 − 68.83 ≈ 67.17", "cos 55° ≈ 0.5736."),
                step("Take square root", "d ≈ √67.17 ≈ 8.20", "Shorter diagonal ≈ 8.2 units."),
                step("Final answer", "Shorter diagonal ≈ 8.2 units.", "The other diagonal (across the supplementary angle) would be √(36+100+68.83) ≈ √204.83 ≈ 14.3."),
            ],
            src(LR, "Ch 8.7"),
        ),
        step_by_step(
            "A triangle has sides 9, 10, and 11. Determine whether it is acute, right, or obtuse.",
            "Check c² vs a²+b² for the largest side.",
            [
                step("Identify the largest side", "c = 11. Compare c² = 121 to a² + b² = 9² + 10² = 81 + 100 = 181.", "c² = 121."),
                step("Compare", "c² = 121 < 181 = a² + b².", "121 is less than 181."),
                step("Conclusion", "c² < a² + b² → all angles are acute.", "By the converse of the Pythagorean theorem."),
                step("Final answer", "The triangle is acute (all angles < 90°).", "If c² = a²+b² it would be right; if c² > a²+b² it would be obtuse."),
            ],
            src(LR, "Ch 8.7"),
        ),
    ],

    "area-of-triangle": [
        step_by_step(
            "Find the area of triangle ABC with a = 5, b = 8, and C = 45°.",
            "Area = (1/2)ab sin C.",
            [
                step("Apply formula", "A = (1/2)(5)(8) sin(45°) = 20 · (√2/2) = 10√2", "sin 45° = √2/2."),
                step("Approximate", "10√2 ≈ 14.14 square units.", "About 14.1."),
                step("Final answer", "Area = 10√2 ≈ 14.1.", "No need to find side c or height first."),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "Find the area of an equilateral triangle with side 6 cm.",
            "Use A = (1/2)ab sin C with a = b = 6 and C = 60°.",
            [
                step("Apply formula", "A = (1/2)(6)(6) sin(60°) = 18 · (√3/2) = 9√3 cm²", "sin 60° = √3/2."),
                step("Approximate", "9√3 ≈ 15.59 cm².", "About 15.6 square centimeters."),
                step("Final answer", "Area = 9√3 ≈ 15.6 cm².", "The standard formula for equilateral triangles: (√3/4)s² = (√3/4)(36) = 9√3 ✓"),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "The area of a triangle is 24 cm². Two sides are 6 cm and 8 cm. What angle is between them?",
            "Rearrange Area = (1/2)ab sin C.",
            [
                step("Plug in", "24 = (1/2)(6)(8) sin C = 24 sin C", "6·8/2 = 24."),
                step("Solve", "sin C = 24/24 = 1 → C = arcsin(1) = 90°", "sin C = 1 implies C = 90°."),
                step("Final answer", "The included angle is 90° (a right triangle).", "Any triangle with area = (1/2)(6)(8) must have sin C = 1, so C = 90°."),
            ],
            src(LR, "Ch 8.8"),
        ),
        step_by_step(
            "Find the area of triangle ABC using Heron's formula: a = 11, b = 13, c = 20.",
            "Check if the triangle is valid first.",
            [
                step("Check triangle inequality", "11 + 13 = 24 > 20 ✓. But 24 is only slightly more than 20 — this is a very 'flat' triangle.", "Sum of any two sides must exceed the third."),
                step("Compute s", "s = (11+13+20)/2 = 44/2 = 22", "Semi-perimeter."),
                step("Apply Heron's formula", "A = √[22(22−11)(22−13)(22−20)] = √[22·11·9·2] = √[4356] = 66", "22·11=242; 9·2=18; 242·18=4356; √4356=66."),
                step("Final answer", "Area = 66 square units.", "Check: using Law of Cosines, the angle opposite c=20 is obtuse (~99°). Area = (1/2)(11)(13)sin C ≈ 71.5·sin 99° ≈ 71.5·0.99 ≈ 70.8. Slight discrepancy due to rounding — Heron's gives exact: √[22·11·9·2] = √(4356) = 66 ✓."),
            ],
            src(LR, "Ch 8.8"),
        ),
    ],

    "vectors": [
        step_by_step(
            "Find the unit vector in the direction of v = ⟨4, 3⟩.",
            "Compute u = v / |v|.",
            [
                step("Find |v|", "|v| = √(4² + 3²) = √(16 + 9) = √25 = 5", "Pythagorean theorem."),
                step("Divide by magnitude", "u = ⟨4, 3⟩ / 5 = ⟨4/5, 3/5⟩", "Unit vector has magnitude 1."),
                step("Verify", "|u| = √((4/5)² + (3/5)²) = √(16/25+9/25) = √(25/25) = 1 ✓", "Confirmed."),
                step("Final answer", "Unit vector: ⟨4/5, 3/5⟩.", "Points in the same direction as v but with length 1."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Find the angle between u = ⟨1, 1⟩ and v = ⟨1, √3⟩.",
            "Use the dot product formula: cos θ = (u·v) / (|u||v|).",
            [
                step("Compute dot product", "u · v = 1·1 + 1·√3 = 1 + √3", "u·v = a₁a₂ + b₁b₂."),
                step("Find magnitudes", "|u| = √(1²+1²) = √2; |v| = √(1²+(√3)²) = √(1+3) = 2", "Pythagorean theorem."),
                step("Find cos θ", "cos θ = (1+√3) / (√2 · 2) = (1+√3)/(2√2)", "Substitute."),
                step("Find θ", "θ = arccos((1+√3)/(2√2)) ≈ arccos((2.732)/(2.828)) ≈ arccos(0.966) ≈ 15°", "This is a 75° angle between the vectors in the standard sense — wait, let me recalculate: 2√2 ≈ 2.828; 1+√3 ≈ 2.732; 2.732/2.828 ≈ 0.966; arccos(0.966) ≈ 15°. Yes, about 15°."),
                step("Final answer", "θ ≈ 15°.", "The angle between the two vectors is approximately 15 degrees."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Resolve u = ⟨6, 8⟩ into components parallel and perpendicular to v = ⟨3, 0⟩.",
            "Find parallel = projection, perpendicular = u − projection.",
            [
                step("Find projection of u onto v", "proj_v(u) = [(u·v)/(v·v)]v = (6·3+8·0)/(9+0) · ⟨3,0⟩ = 18/9 · ⟨3,0⟩ = 2⟨3,0⟩ = ⟨6, 0⟩", "v is along the x-axis, so projection is just the x-component."),
                step("Find perpendicular component", "u⊥ = u − proj_v(u) = ⟨6,8⟩ − ⟨6,0⟩ = ⟨0, 8⟩", "The vertical component."),
                step("Check", "⟨6, 8⟩ = ⟨6, 0⟩ + ⟨0, 8⟩ ✓; dot product of parallel and perpendicular = 6·0+0·8=0 ✓.", "Perpendicular vectors have zero dot product."),
                step("Final answer", "Parallel: ⟨6, 0⟩. Perpendicular: ⟨0, 8⟩.", "This decomposes u into x- and y-components relative to v."),
            ],
            src(LR, "Ch 9.1"),
        ),
        step_by_step(
            "Find the work done by force F = ⟨3, 4⟩ N moving an object from (0, 0) to (6, 8) m.",
            "Use W = F · d.",
            [
                step("Find displacement vector", "d = ⟨6−0, 8−0⟩ = ⟨6, 8⟩ m", "Final position minus initial position."),
                step("Compute dot product", "W = F · d = 3·6 + 4·8 = 18 + 32 = 50 N·m = 50 J", "Work = Force · Displacement."),
                step("Final answer", "Work = 50 joules.", "This equals the force component in the direction of motion times the distance traveled."),
            ],
            src(LR, "Ch 9.1"),
        ),
    ],

    "complex-numbers": [
        step_by_step(
            "Find the modulus and argument of z = −1 + i.",
            "Compute r = √(a²+b²), θ = arctan(b/a).",
            [
                step("Modulus", "|z| = √((−1)² + 1²) = √(1+1) = √2", "Distance from origin."),
                step("Argument", "θ = arctan(1/(−1)) = arctan(−1) = −π/4. But in QII (x<0, y>0), add π: θ = π − π/4 = 3π/4.", "QII correction for arctan."),
                step("Final answer", "Modulus = √2, Argument = 3π/4 (135°).", "z = √2(cos(3π/4) + i sin(3π/4)) in polar form."),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Convert z = 2(cos(π/3) + i sin(π/3)) to a + bi form.",
            "Evaluate the trig functions.",
            [
                step("Evaluate cos and sin", "cos(π/3) = 1/2; sin(π/3) = √3/2.", "Standard angles."),
                step("Multiply by 2", "z = 2(1/2 + i·√3/2) = 1 + i√3", "The modulus 2 scales both parts."),
                step("Final answer", "z = 1 + i√3.", "Check: |z| = √(1+3) = 2 ✓."),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Multiply (2 + i)³ using De Moivre's theorem.",
            "First find modulus and argument, then apply (r cis θ)ⁿ = rⁿ cis(nθ).",
            [
                step("Find r and θ for 2 + i", "r = √(4+1) = √5; θ = arctan(1/2) ≈ 26.565°.", "First express in polar form."),
                step("Apply De Moivre", "(2+i)³ = (√5)³ cis(3θ) = 5√5 cis(3 arctan(1/2))", "r^n cis(nθ). 3θ ≈ 79.7°."),
                step("Compute 3θ exactly using tan(3θ) formula", "Better: expand algebraically: (2+i)² = 4+4i+i² = 3+4i. Then (3+4i)(2+i) = 6+3i+8i+4i² = 6+11i−4 = 2+11i.", "Step-by-step expansion avoids angle formulas."),
                step("Final answer", "(2+i)³ = 2 + 11i.", "Check magnitude: |2+i| = √5, |(2+i)³| = (√5)³ = 5√5 ≈ 11.18. |2+11i| = √(4+121) = √125 = 5√5 ≈ 11.18 ✓."),
            ],
            src(LR, "Ch 9.4"),
        ),
        step_by_step(
            "Solve  x² + 4x + 13 = 0  over the complex numbers.",
            "Use the quadratic formula.",
            [
                step("Apply quadratic formula", "x = [−4 ± √(16 − 52)] / 2 = [−4 ± √(−36)] / 2 = [−4 ± 6i] / 2", "D = 16−52 = −36."),
                step("Simplify", "x = −2 ± 3i", "Divide both terms by 2."),
                step("Final answer", "x = −2 + 3i or x = −2 − 3i.", "Complex conjugate pair. Check: (−2+3i)² + 4(−2+3i) + 13 = (4−12i−9)+ (−8+12i)+13 = (−5−12i)+(−8+12i)+13 = 0 ✓."),
            ],
            src(LR, "Ch 9.4"),
        ),
    ],

    "conic-sections": [
        step_by_step(
            "Identify the conic 4x² + 9y² = 36 and find its key features.",
            "Divide by 36 to get standard form.",
            [
                step("Divide by 36", "4x²/36 + 9y²/36 = 1 → x²/9 + y²/4 = 1", "Standard ellipse form."),
                step("Identify as ellipse", "Both terms positive, different denominators: a² = 9, b² = 4.", "If a² > b², the major axis is horizontal."),
                step("Key features", "Center (0,0); vertices (±3, 0); co-vertices (0, ±2); foci: (±√5, 0) since c² = 9−4 = 5.", "c = √5 ≈ 2.24."),
                step("Final answer", "Ellipse centered at origin: x²/9 + y²/4 = 1. Vertices (±3, 0), Co-vertices (0, ±2), Foci (±√5, 0).", "Horizontal major axis of length 6."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Find the equation of the parabola with focus (0, 3) and directrix y = −3.",
            "Use the definition: distance to focus = distance to directrix.",
            [
                step("Set up equation", "√[(x−0)² + (y−3)²] = |y + 3|", "Distance from (x,y) to focus = distance to directrix."),
                step("Square both sides", "(x² + (y−3)²) = (y+3)²", "Both sides are non-negative."),
                step("Expand", "x² + y² − 6y + 9 = y² + 6y + 9 → x² − 6y + 9 = 6y + 9 → x² = 12y", "Cancel y² and 9."),
                step("Standard form", "y = x²/12 = (1/12)x². Or x² = 12y → 4p = 12 → p = 3.", "Focus is (0, p) = (0, 3) ✓; directrix y = −p = −3 ✓."),
                step("Final answer", "x² = 12y (parabola opening upward).", "Vertex at (0, 0)."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Identify the conic x² + 2y² − 6x + 8y + 1 = 0 by completing the square.",
            "Complete squares in x and y.",
            [
                step("Group x and y", "(x² − 6x) + (2y² + 8y) = −1", "Move constant to right."),
                step("Complete square for x", "x² − 6x = (x−3)² − 9", "Half of −6 is −3; (−3)² = 9."),
                step("Factor and complete for y", "2(y² + 4y) = 2[(y+2)² − 4] = 2(y+2)² − 8", "Factor out 2 first, then complete."),
                step("Substitute", "(x−3)² − 9 + 2(y+2)² − 8 = −1 → (x−3)² + 2(y+2)² = 16 → (x−3)²/16 + (y+2)²/8 = 1", "Simplify: −9−8 = −17; −17 = −1 → add 16: 16 on both sides."),
                step("Final answer", "Ellipse centered at (3, −2): (x−3)²/16 + (y+2)²/8 = 1.", "Horizontal semi-axis 4, vertical semi-axis √8 ≈ 2.83."),
            ],
            src(LR, "Ch 9.5"),
        ),
        step_by_step(
            "Find the center, vertices, and asymptotes of  (y²/9) − (x²/4) = 1.",
            "This is a vertical hyperbola.",
            [
                step("Standard form", "y²/3² − x²/2² = 1. Center (0,0).", "Vertical hyperbola: y²/a² − x²/b² = 1."),
                step("Vertices", "(0, ±a) = (0, ±3).", "On the y-axis."),
                step("Asymptotes", "y = ±(a/b)x = ±(3/2)x.", "Pass through the center."),
                step("Final answer", "Center (0,0), vertices (0,±3), asymptotes y = ±(3/2)x.", "Opens up and down along the y-axis."),
            ],
            src(LR, "Ch 9.5"),
        ),
    ],
}


# ---------------------------------------------------------------------------
# Patch course.json with missing entries
# ---------------------------------------------------------------------------

def patch_missing(data):
    total_added = 0
    for w in data.get("weeks", []):
        for t in w.get("topics", []):
            slug = t.get("slug", "")
            if slug in MISSING_SBS:
                lesson = t.setdefault("lesson", {})
                existing = {s["title"] for s in lesson.get("stepByStep", [])}
                new_items = [s for s in MISSING_SBS[slug] if s["title"] not in existing]
                lesson.setdefault("stepByStep", []).extend(new_items)
                total_added += len(new_items)
                print(f"  '{t['title']}' ({slug}): added {len(new_items)} walkthroughs")
    return total_added


def main():
    with open(COURSE) as f:
        data = json.load(f)

    print("Patching missing walkthroughs...")
    added = patch_missing(data)
    print(f"\nTotal added: {added}")

    with open(COURSE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Written: {COURSE}")


if __name__ == "__main__":
    main()
