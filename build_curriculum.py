#!/usr/bin/env python3
"""Append weeks 2-7 to the curriculum JSON.

This script keeps the source-of-truth content in one Python file and rewrites
course.json each run. Run from the project root:  python3 build_curriculum.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
COURSE = ROOT / "App" / "Resources" / "Content" / "course.json"

# Import the big practice-question bank
sys.path.insert(0, str(ROOT))
import practice_questions as PQ  # noqa: E402


def src(source, chapter=None, section=None, url_path=None):
    return {
        "source": source,
        "chapter": chapter,
        "section": section,
        "urlPath": url_path,
    }


def lesson(
    objectives,
    intro,
    sections,
    examples,
    step_by_step,
    videos,
    practice,
    graph_plots=None,
    key_formulas=None,
):
    return {
        "objectives": objectives,
        "explanation": {"intro": intro, "sections": sections},
        "examples": examples,
        "stepByStep": step_by_step,
        "videos": videos,
        "practice": practice,
        "graphPlots": graph_plots,
        "keyFormulas": key_formulas,
    }


def section(heading, body, bullets=None):
    return {"heading": heading, "body": body, "bullets": bullets}


def example(title, problem, solution, steps, source):
    return {
        "title": title,
        "problem": problem,
        "solution": solution,
        "steps": steps,
        "source": source,
    }


def step_by_step(title, prompt, steps, source):
    return {"title": title, "prompt": prompt, "steps": steps, "source": source}


def step(label, math, explanation):
    return {"label": label, "math": math, "explanation": explanation}


def video(youtube_id, title, channel, source, duration=None):
    return {
        "youtubeId": youtube_id,
        "title": title,
        "channel": channel,
        "source": source,
        "durationSeconds": duration,
    }


def mc(prompt, choices, answer, explanation, source, hints=None):
    return {
        "kind": "mc",
        "prompt": prompt,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "source": source,
        "hints": _normalize_hints(hints),
    }


def tf(prompt, answer, explanation, source, hints=None):
    return {
        "kind": "tf",
        "prompt": prompt,
        "choices": ["True", "False"],
        "answer": answer,
        "explanation": explanation,
        "source": source,
        "hints": _normalize_hints(hints),
    }


def fr(prompt, answer, explanation, source, hints=None):
    return {
        "kind": "fr",
        "prompt": prompt,
        "choices": None,
        "answer": answer,
        "explanation": explanation,
        "source": source,
        "hints": _normalize_hints(hints),
    }


def _normalize_hints(hints):
    if not hints:
        return []
    cleaned = [str(h).strip() for h in hints if h is not None and str(h).strip()]
    return cleaned[:3]


def plot(title, expression, domain_x, domain_y, note=None):
    return {
        "title": title,
        "expression": expression,
        "domainX": list(domain_x),
        "domainY": list(domain_y),
        "note": note,
    }


def formula(name, latex, when_to_use=None):
    return {"name": name, "latex": latex, "whenToUse": when_to_use}


def topic(slug, title, summary, minutes, sources, lesson_obj):
    return {
        "slug": slug,
        "title": title,
        "summary": summary,
        "estimatedMinutes": minutes,
        "sources": sources,
        "lesson": lesson_obj,
    }


def with_expanded_practice(topic_dict):
    """If the topic slug has an entry in PQ.PRACTICE_BY_SLUG, replace the
    practice list with the full 10-question bank (with 3 hints each)."""
    slug = topic_dict["slug"]
    if slug in PQ.PRACTICE_BY_SLUG:
        lesson = topic_dict["lesson"]
        new_practice = PQ.PRACTICE_BY_SLUG[slug]
        topic_dict["lesson"] = {**lesson, "practice": new_practice}
    return topic_dict


def week(number, title, summary, sources, topics):
    return {
        "number": number,
        "title": title,
        "summary": summary,
        "sources": sources,
        "topics": topics,
    }


# Source code constants
LR = "lippman_rasmussen"
OS = "openstax_abramson"
YS = "yoshiwara"


# ---------------------------------------------------------------------------
# Week 1 — Foundations
# ---------------------------------------------------------------------------

week1 = week(
    1,
    "Foundations",
    "Functions, function notation, domain & range, rates of change, composition, and transformation of functions.",
    [
        src(LR, "Ch 1 Functions", "1.1–1.5", "01%3A_Functions"),
        src(OS, "Ch 3 Functions", "3.1–3.4"),
    ],
    [
        topic(
            "what-is-a-function",
            "What Is a Function?",
            "Inputs, outputs, the vertical-line test, function notation. From Lippman & Rasmussen §1.1.",
            30,
            [src(LR, "Ch 1", "section 1.1")],
            lesson(
                ["Define a function and identify the dependent and independent variables.", "Read and write function notation f(x).", "Apply the vertical-line test to a graph."],
                "A function is a rule that takes each input to exactly one output.",
                [
                    section("Inputs and outputs", "The input set is the domain; the output set is the range."),
                    section("Vertical-line test", "No vertical line crosses the graph more than once."),
                    section("Function notation", "f(x) = 3x² + 2. Evaluate f(5) = 77."),
                ],
                [
                    example("Evaluate f(x) = 3x² + 2 at x = 5", "Compute f(5).", "77",
                            ["3(5)² + 2 = 75 + 2 = 77."], src(LR, "Ch 1.1")),
                ],
                [step_by_step(
                    "Evaluate g(t) = 2t³ − 5t + 1 at t = −2.",
                    "Compute g(−2).",
                    [
                        step("Substitute t = −2", "2(−2)³ − 5(−2) + 1", "Replace every t with −2."),
                        step("Apply the exponent", "2(−8) − 5(−2) + 1", "(−2)³ = −8."),
                        step("Multiply", "−16 + 10 + 1", "−5(−2) = 10."),
                        step("Add", "−5", "Sum: −16 + 10 + 1 = −5."),
                    ],
                    src(LR, "Ch 1.1"))],
                [
                    video('F8dq2QdqDv0', 'What is a function?', 'Khan Academy', src('openstax_abramson', 'Ch 1.1'), 540),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                    video('hOf2UFyL_QE', 'Functions — Full Lecture', 'OpenStax', src('openstax_abramson', 'Ch 3.1'), 540),
                    video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
                ],

                [
                    mc("If f(x) = 4x − 7, what is f(3)?", ["−5", "5", "19", "12"], "1",
                       "f(3) = 4·3 − 7 = 5. (Index 1.)", src(LR, "Ch 1.1")),
                    tf("A vertical line can cross a function's graph at most once.", "0",
                       "That IS the definition of a function.", src(LR, "Ch 1.1")),
                    mc("Which relation is NOT a function?", ["y = 2x + 1", "{(1,2),(2,3),(3,4)}", "x = y²", "y = x²"], "2",
                       "x = y² fails the vertical-line test.", src(LR, "Ch 1.1")),
                ],
                [plot("f(x) = x²", "pow(x, 2)", [-3, 3], [-1, 9], note="Parabola. Passes the vertical-line test.")],
            ),
        ),
        topic(
            "domain-and-range",
            "Domain & Range",
            "Finding the set of all legal inputs and possible outputs.",
            35,
            [src(LR, "Ch 1.2")],
            lesson(
                ["Find the domain of common function families.", "Read the range from a graph.", "Restrict a domain to make a function invertible."],
                "A function is the rule plus the inputs you allow.",
                [
                    section("Implicit domain", "Exclude values that make a denominator zero, give a negative radicand, or a non-positive log."),
                    section("Reading range from a graph", "Lowest to highest y."),
                    section("Why domains get restricted", "To make the rule one-to-one so an inverse exists."),
                ],
                [
                    example("Domain of f(x) = (x + 1)/(x² − 1)", "Find all real x.", "All real x except ±1",
                            ["Denominator zero at x = ±1."], src(LR, "Ch 1.2")),
                ],
                [step_by_step(
                    "Find the domain of g(x) = √(5 − 2x).",
                    "State the domain.",
                    [
                        step("Set radicand ≥ 0", "5 − 2x ≥ 0", "Square roots of negatives aren't real."),
                        step("Solve", "x ≤ 5/2", "Divide by −2 and flip the inequality."),
                        step("Interval notation", "(−∞, 5/2]", "Bracket because the endpoint is included."),
                    ],
                    src(LR, "Ch 1.2"))],
                [
                    video('O0uUVH8dRiU', 'Domain and range', 'Khan Academy', src('lippman_rasmussen', 'Ch 1.2'), 660),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('mL9eBKaKXAI', 'Finding Domain and Range of a Function', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 540),
                    video('hOf2UFyL_QE', 'Functions — Full Lecture', 'OpenStax', src('openstax_abramson', 'Ch 3.1'), 540),
                ],

                [
                    mc("Domain of f(x) = √(x − 7)?", ["x ≥ 7", "x ≤ 7", "x > 7", "all real x"], "0",
                       "Need x − 7 ≥ 0.", src(LR, "Ch 1.2")),
                ],
            ),
        ),
        topic(
            "rates-of-change-and-behavior",
            "Rates of Change & Graph Behavior",
            "Average rate of change, increasing/decreasing, even/odd.",
            30,
            [src(LR, "Ch 1.3")],
            lesson(
                ["Compute the average rate of change.", "Identify intervals of increase/decrease.", "Recognize even and odd functions."],
                "The shape of a graph is the story of how a quantity changes.",
                [
                    section("Average rate of change", "(f(b) − f(a))/(b − a) — slope of the secant line."),
                    section("Increasing/decreasing", "Compare f(x₂) and f(x₁) for x₂ > x₁."),
                    section("Even & odd", "Even: f(−x) = f(x). Odd: f(−x) = −f(x)."),
                ],
                [
                    example("Average rate of change of f(x) = x² between 1 and 3", "Compute.", "4",
                            ["(9 − 1)/2 = 4."], src(LR, "Ch 1.3")),
                ],
                [step_by_step(
                    "Is f(x) = 3x⁴ − 2x² + 7 even, odd, or neither?",
                    "Test the symmetry.",
                    [
                        step("Compute f(−x)", "f(−x) = 3x⁴ − 2x² + 7", "Even powers absorb the minus sign."),
                        step("Compare to f(x)", "f(−x) = f(x)", "Even function."),
                    ],
                    src(LR, "Ch 1.3"))],
                [
                    video('fG-yjRfGMRQ', 'Average rate of change', 'Khan Academy', src('lippman_rasmussen', 'Ch 1.3'), 480),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                ],

                [
                    mc("Average rate of change of f(x) = 2x + 1 between 0 and 4?", ["1", "2", "4", "9"], "1",
                       "(f(4) − f(0))/4 = (9 − 1)/4 = 2. (Index 1.)", src(LR, "Ch 1.3")),
                ],
            ),
        ),
        topic(
            "composition-of-functions",
            "Composition of Functions",
            "f(g(x)), decomposing functions, domain of the composition.",
            30,
            [src(LR, "Ch 1.4")],
            lesson(
                ["Form the composition f(g(x)).", "Decompose a function into simpler pieces.", "Find the domain of a composition."],
                "Composing functions means feeding the output of one into the next.",
                [
                    section("Definition", "(f ∘ g)(x) = f(g(x))."),
                    section("Decomposition", "h(x) = √(x² + 1) is f(u) = √u composed with g(x) = x² + 1."),
                    section("Domain", "x in domain of g AND g(x) in domain of f."),
                ],
                [
                    example("Compute (f ∘ g)(3) where f(x) = x² and g(x) = 2x + 1", "Evaluate.", "49",
                            ["g(3) = 7; f(7) = 49."], src(LR, "Ch 1.4")),
                ],
                [step_by_step(
                    "Let f(x) = 2x − 3 and g(x) = x² + 1. Find (f ∘ g)(x).",
                    "Write the formula.",
                    [
                        step("Substitute", "f(g(x)) = 2(g(x)) − 3", "Replace x in f with g(x)."),
                        step("Simplify", "2(x² + 1) − 3 = 2x² − 1", "Distribute and combine."),
                    ],
                    src(LR, "Ch 1.4"))],
                [
                    video('DbSyWAfIq8g', 'Composing functions', 'Khan Academy', src('lippman_rasmussen', 'Ch 1.4'), 480),
                    video('EsgHKdLSPVc', 'Composition of Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.4'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                ],

                [
                    mc("If f(x) = x + 4, g(x) = x², what is (f ∘ g)(2)?", ["6", "8", "10", "12"], "1",
                       "g(2) = 4; f(4) = 8. (Index 1.)", src(LR, "Ch 1.4")),
                ],
            ),
        ),
        topic(
            "transformation-of-functions",
            "Transformation of Functions",
            "Shifts, stretches, compressions, reflections.",
            40,
            [src(LR, "Ch 1.5")],
            lesson(
                ["Apply vertical and horizontal shifts.", "Apply stretches, compressions, and reflections.", "Combine multiple transformations."],
                "Don't graph from scratch. Transform what you already know.",
                [
                    section("Vertical shift", "f(x) + k → up k. f(x) − k → down k."),
                    section("Horizontal shift", "f(x − h) → right h. f(x + h) → left h."),
                    section("Stretches & reflections", "a·f(x) vertical; f(bx) horizontal; sign flips reflect."),
                ],
                [
                    example("Graph y = |x − 3| + 2", "Describe the graph.", "V-shape with vertex (3, 2).",
                            ["Replace x with (x − 3): vertex (3, 0). Add 2: vertex (3, 2)."], src(LR, "Ch 1.5")),
                ],
                [step_by_step(
                    "Graph y = −2(x + 1)² + 3 from y = x².",
                    "Describe and give the vertex.",
                    [
                        step("Start with y = x²", "Vertex (0, 0), opens up.", "Baseline."),
                        step("Replace x with x + 1", "Vertex (–1, 0).", "Shift left 1."),
                        step("Multiply by −2", "Vertical stretch by 2, reflect over x-axis.", "Now opens down."),
                        step("Add 3", "Vertex (–1, 3).", "Shift up 3."),
                    ],
                    src(LR, "Ch 1.5"))],
                [
                    video('AEK4DbIBK8w', 'Transformations of functions', 'Khan Academy', src('lippman_rasmussen', 'Ch 1.5'), 600),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                ],

                [
                    mc("Compared to y = f(x), the graph of y = f(x − 4) is shifted…", ["left 4", "right 4", "up 4", "down 4"], "1",
                       "x − h inside the function shifts right by h. (Index 1.)", src(LR, "Ch 1.5")),
                ],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 2 — Algebra: Graphs and Functions, and Trigonometry
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Week 2 — Algebra: Graphs and Functions, and Trigonometry
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Week 2 — Algebra: Graphs and Functions, and Trigonometry
# ---------------------------------------------------------------------------

week2 = week(
    2,
    "Algebra: Graphs and Functions, and Trigonometry",
    "Linear and quadratic functions in depth, then a first look at the trigonometric functions: angle measure, right-triangle ratios, the unit circle, and the six trig functions.",
    [
        src(LR, "Ch 2 Linear Functions", "2.1–2.4", "02%3A_Linear_Functions"),
        src(LR, "Ch 3 Polynomial and Rational Functions", "3.1–3.2"),
        src(OS, "Ch 4 Linear Functions", "4.1–4.3"),
        src(YS, "Ch 1 Triangles and Circles", "1.0–1.2"),
        src(YS, "Ch 2 Trigonometric Ratios", "2.0–2.2"),
    ],
    [
        topic(
            "linear-functions",
            "Linear Functions",
            "Slope, intercept, parallel and perpendicular lines, modeling with linear functions. From Lippman & Rasmussen §§2.1–2.3 and OpenStax §§4.1–4.3.",
            30,
            [src(LR, "Ch 2", "2.1–2.3"), src(OS, "Ch 4", "4.1–4.3")],
            lesson(
                ["Write equations of lines in slope-intercept and point-slope form.", "Identify parallel and perpendicular lines from their slopes.", "Build a linear model from a story."],
                "A linear function has the form f(x) = mx + b with constant slope m.",
                [
                    section("Slope-intercept form", "y = mx + b. m is the slope (rise over run). b is the y-intercept."),
                    section("Point-slope form", "y − y₁ = m(x − x₁). Useful when you know one point and the slope."),
                    section("Parallel & perpendicular", "Parallel: equal slopes. Perpendicular: slopes are negative reciprocals (m₁·m₂ = −1)."),
                ],
                [
                    example("Equation through (3, 7) with slope 4", "Write the line in slope-intercept form.",
                            "y = 4x − 5",
                            ["y − 7 = 4(x − 3)", "y − 7 = 4x − 12", "y = 4x − 5."],
                            src(LR, "Ch 2.1")),
                ],
                [step_by_step(
                    "Find the line through (1, 4) perpendicular to y = 2x + 1.",
                    "Write the equation.",
                    [
                        step("Find the perpendicular slope", "m = −1/2", "Perpendicular slopes are negative reciprocals."),
                        step("Apply point-slope form", "y − 4 = −½(x − 1)", "Substitute (1, 4) and m = −½."),
                        step("Simplify to slope-intercept", "y = −½x + 9/2", "Distribute and add 4 to both sides."),
                    ],
                    src(LR, "Ch 2.2"))],
                [
                    video('RhMk6B2EibQ', 'Linear equations and slope', 'Khan Academy', src('lippman_rasmussen', 'Ch 2.1'), 540),
                    video('ldYGiXSHa_Q', 'Solving Linear Equations', 'PatrickJMT', src('openstax_abramson', 'Ch 1.1'), 600),
                    video('XFkmEW6myeU', 'Slope Intercept Form of a Line', "Mario's Math Tutoring", src('lippman_rasmussen', 'Ch 2.1'), 540),
                    video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                ],

                [
                    mc("Slope of the line through (2, 5) and (6, 17)?", ["2", "3", "4", "12/4"], "1",
                       "(17 − 5)/(6 − 2) = 12/4 = 3. (Index 1 = '3'.)", src(LR, "Ch 2.1")),
                    mc("Line A has slope 2, line B has slope ½. They are…", ["parallel", "perpendicular", "the same line", "intersecting but not perpendicular"], "0",
                       "Equal slopes → parallel. (Perpendicular would need slopes whose product is −1.)", src(LR, "Ch 2.2")),
                    fr("A phone plan charges $30/month plus $0.10/minute. Write the cost C as a function of minutes m.",
                       "C = 0.10m + 30", "Initial cost (y-intercept) is 30; slope is 0.10 per minute.", src(LR, "Ch 2.3")),
                ],
                [plot("Linear function  y = 2x + 1", "2*x + 1", [-5, 5], [-9, 11])],
            ),
        ),
        topic(
            "quadratic-functions",
            "Quadratic Functions",
            "Parabolas, vertex form, completing the square, the discriminant. From Lippman & Rasmussen §3.2 and OpenStax §2.5.",
            40,
            [src(LR, "Ch 3.2", "Quadratic Functions"), src(OS, "Ch 2.5", "Quadratic Equations")],
            lesson(
                ["Identify a quadratic function and its key features.", "Find the vertex by completing the square.", "Use the discriminant to count real roots."],
                "A quadratic has the form f(x) = ax² + bx + c with a ≠ 0. Its graph is a parabola.",
                [
                    section("Vertex form", "y = a(x − h)² + k. The vertex is (h, k). a > 0 opens up; a < 0 opens down."),
                    section("Completing the square", "Move c, take half the coefficient of x, square it, add and subtract to factor as a perfect square."),
                    section("Discriminant", "D = b² − 4ac. D > 0: two real roots. D = 0: one (double) root. D < 0: no real roots."),
                ],
                [
                    example("Complete the square for y = x² + 6x + 5",
                            "Rewrite in vertex form.",
                            "y = (x + 3)² − 4",
                            ["Take half of 6 → 3, square it → 9.", "x² + 6x + 5 = (x² + 6x + 9) − 9 + 5 = (x + 3)² − 4."],
                            src(LR, "Ch 3.2")),
                ],
                [step_by_step(
                    "Solve x² + 6x + 5 = 0 by completing the square.",
                    "Find all real solutions.",
                    [
                        step("Rewrite", "x² + 6x = −5", "Move the constant to the other side."),
                        step("Add (b/2)² to both sides", "x² + 6x + 9 = −5 + 9", "(6/2)² = 9."),
                        step("Factor left side", "(x + 3)² = 4", "Now the left side is a perfect square."),
                        step("Take the square root of both sides", "x + 3 = ±2", "Remember the ±."),
                        step("Solve", "x = −3 ± 2 = −1 or x = −5", "Two real roots.")] ,
                    src(LR, "Ch 3.2"))],
                [
                    video('Z7C5g7S3dPw', 'Quadratic equations', 'Khan Academy', src('lippman_rasmussen', 'Ch 3.2'), 600),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                    video('GmMX3-nTWbE', 'Solving Linear Equations Made Easy', 'PatrickJMT', src('openstax_abramson', 'Ch 1.1'), 600),
                    video('HAO4Yuk9wP0', 'Factoring Polynomials — All Types', "Mario's Math Tutoring", src('openstax_abramson', 'Ch 1.4'), 600),
                    video('iA0wluAsrNY', 'Algebra Review — Trigonometry', 'Organic Chemistry Tutor', src('yoshiwara', 'Ch 2.1'), 600),
                ],

                [
                    mc("Vertex of y = (x − 2)² + 5?", ["(2, 5)", "(−2, 5)", "(2, −5)", "(5, 2)"], "0",
                       "h = 2, k = 5. Vertex is (h, k) = (2, 5).", src(LR, "Ch 3.2")),
                    mc("For x² + 2x + 5 = 0, how many real roots?", ["0", "1", "2", "cannot tell"], "0",
                       "D = 4 − 20 = −16 < 0. No real roots.", src(OS, "Ch 2.5")),
                    fr("A ball is thrown straight up; its height in feet after t seconds is h(t) = −16t² + 64t + 5. When does it return to h = 5?",
                       "t = 0 or t = 4", "Set h(t) = 5: −16t² + 64t = 0 → −16t(t − 4) = 0.", src(OS, "Ch 2.5")),
                ],
                [plot("y = x² + 6x + 5", "pow(x,2) + 6*x + 5", [-7, 1], [-5, 5], note="Roots at x = −1 and x = −5.")],
            ),
        ),
        topic(
            "angle-measure",
            "Angle Measure (Degrees & Radians)",
            "Convert between degrees and radians, coterminal angles, arc length. From Yoshiwara §§1.0 and 6.0.",
            25,
            [src(YS, "Ch 1.0", "Angles and Triangles"), src(YS, "Ch 6.0", "Arclength and Radians")],
            lesson(
                ["Convert between degrees and radians.", "Find a positive coterminal angle.", "Compute arc length and area of a sector."],
                "Radians are the natural unit for trigonometry because they connect angle to arc length directly.",
                [
                    section("Conversion", "180° = π radians. So degrees ↔ radians: multiply by π/180 or 180/π."),
                    section("Coterminal angles", "Add or subtract multiples of 360° (or 2π rad) to get another angle that points the same way."),
                    section("Arc length & sector area", "s = rθ (θ in radians). A = ½r²θ."),
                ],
                [
                    example("Convert 150° to radians",
                            "Express in terms of π.",
                            "5π/6",
                            ["150 · π/180 = 150π/180 = 5π/6."],
                            src(YS, "Ch 1.0")),
                ],
                [step_by_step(
                    "Find a positive coterminal angle to −210° that is less than 360°.",
                    "Compute.",
                    [
                        step("Add 360°", "−210° + 360° = 150°", "Coterminal means same terminal ray."),
                        step("Already positive and under 360°", "Answer: 150°", "Done.")] ,
                    src(YS, "Ch 1.0"))],
                [
                    video('Czuqc1tDshQ', 'Radians and degrees', 'Khan Academy', src('yoshiwara', 'Ch 1.0'), 480),
                    video('l6hSY2Pcch0', 'Radians and Degrees', 'NancyPi', src('yoshiwara', 'Ch 1.0'), 600),
                    video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                ],

                [
                    mc("Convert 3π/4 radians to degrees.", ["45°", "90°", "135°", "225°"], "2",
                       "3π/4 · 180/π = 3·45 = 135°.", src(YS, "Ch 1.0")),
                    fr("Express 75° in radians.", "5π/12", "75 · π/180 = 5π/12.", src(YS, "Ch 1.0")),
                    mc("Arc length of radius 6 and angle 2 radians?", ["3", "6", "12", "72"], "2",
                       "s = rθ = 6 · 2 = 12.", src(YS, "Ch 6.0")),
                ],
                [plot("Unit circle reference", "sqrt(max(0, 1 - x*x))", [-1.1, 1.1], [-1.1, 1.1], note="Upper half of the unit circle, used to define sine (y) and cosine (x).")],
            ),
        ),
        topic(
            "right-triangle-trig",
            "Right-Triangle Trigonometry",
            "SOH-CAH-TOA, solving right triangles, applications. From Yoshiwara §§2.0–2.2.",
            35,
            [src(YS, "Ch 2", "2.0–2.2", "2%3A_Trigonometric_Ratios")],
            lesson(
                ["Name the six trig ratios for a right triangle.", "Solve a right triangle given two pieces of information.", "Apply trig to a real-world problem."],
                "Right-triangle trigonometry defines the six trig functions as ratios of sides of a right triangle.",
                [
                    section("SOH-CAH-TOA", "sin θ = opposite/hypotenuse, cos θ = adjacent/hypotenuse, tan θ = opposite/adjacent."),
                    section("Reciprocals", "csc θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ."),
                    section("Solving a right triangle", "Find every side and angle. Use inverse trig and the Pythagorean theorem."),
                ],
                [
                    example("A 3-4-5 right triangle. Find sin θ for the angle opposite the side of length 3.",
                            "Compute.",
                            "3/5",
                            ["opposite = 3, hypotenuse = 5. sin θ = 3/5."],
                            src(YS, "Ch 2.1")),
                ],
                [step_by_step(
                    "A ladder 12 ft long leans against a wall, making a 70° angle with the ground. How high up the wall does it reach?",
                    "Find the height.",
                    [
                        step("Identify the side", "Height is opposite the 70° angle. Hypotenuse = 12.", "Draw the right triangle."),
                        step("Apply sine", "sin 70° = h / 12", "opposite/hypotenuse."),
                        step("Solve", "h = 12 · sin 70° ≈ 11.28 ft", "Calculator in degree mode."),
                    ],
                    src(YS, "Ch 2.2"))],
                [
                    video('B7yL9YuJWXc', 'Basic trigonometry', 'Khan Academy', src('yoshiwara', 'Ch 2.1'), 540),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('a5WQlcFTXyk', 'Trigonometry: Solving Right Triangles', 'NancyPi', src('yoshiwara', 'Ch 2.2'), 600),
                    video('iA0wluAsrNY', 'Algebra Review — Trigonometry', 'Organic Chemistry Tutor', src('yoshiwara', 'Ch 2.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("If sin θ = 3/5 in a right triangle, what is cos θ?", ["3/4", "4/5", "5/3", "5/4"], "1",
                       "By the Pythagorean theorem, adjacent = 4 (since 3-4-5). So cos θ = 4/5.", src(YS, "Ch 2.1")),
                    fr("A right triangle has legs 6 and 8. What is the hypotenuse?", "10", "√(6² + 8²) = √100 = 10.", src(YS, "Ch 2.1")),
                ],
            ),
        ),
        topic(
            "unit-circle",
            "The Unit Circle & The Six Trig Functions",
            "Define sine and cosine as coordinates on the unit circle; extend to all six functions. From Yoshiwara §§4.0 and OpenStax §7.1.",
            40,
            [src(YS, "Ch 4", "4.0 Trigonometric Functions"), src(OS, "Ch 7.1", "The Unit Circle"), src(OS, "Ch 7.2", "The Six Trigonometric Functions")],
            lesson(
                ["Define sin θ and cos θ as coordinates on the unit circle.", "Use the unit circle to evaluate the six trig functions at key angles.", "Recognize signs of each function in each quadrant."],
                "The unit circle lets us define trig for any angle, not just acute ones in a triangle.",
                [
                    section("Unit circle definition", "Draw the angle θ from the positive x-axis. The point where the terminal side meets the unit circle is (cos θ, sin θ)."),
                    section("Reference angles", "Every angle has a reference angle to the nearest x-axis. Use the quadrant to set the sign."),
                    section("Six functions from (x, y)", "sin θ = y, cos θ = x, tan θ = y/x, csc θ = 1/y, sec θ = 1/x, cot θ = x/y (where defined)."),
                ],
                [
                    example("Evaluate sin(150°)",
                            "Use the unit circle.",
                            "1/2",
                            ["150° is in Quadrant II. Reference angle = 30°. sin is positive in Q II. sin 150° = sin 30° = 1/2."],
                            src(YS, "Ch 4.0")),
                ],
                [step_by_step(
                    "Find the exact value of tan(300°).",
                    "Compute.",
                    [
                        step("Locate the angle", "300° is in Quadrant IV. Reference angle = 60°.", "Subtract from 360°."),
                        step("Sign of tangent in Q IV", "Tangent is negative in Q IV.", "y is negative, x is positive → ratio negative."),
                        step("Compute magnitude", "|tan 60°| = √3", "Standard 30-60-90 triangle."),
                        step("Apply sign", "tan 300° = −√3", "Negative in Q IV."),
                    ],
                    src(YS, "Ch 4.0"))],
                [
                    video('1m9p9iubMLU', 'Introduction to the unit circle', 'Khan Academy', src('openstax_abramson', 'Ch 7.1'), 480),
                    video('c819bGfH8FA', 'How to Remember the Unit Circle', 'NancyPi', src('openstax_abramson', 'Ch 7.1'), 600),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('l6hSY2Pcch0', 'Radians and Degrees', 'NancyPi', src('yoshiwara', 'Ch 1.0'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("What is cos(120°)?", ["−1/2", "1/2", "−√3/2", "√3/2"], "0",
                       "120° is in Q II with reference angle 60°. cos is negative in Q II. cos 120° = −1/2.", src(OS, "Ch 7.1")),
                    mc("Which is the exact value of sin(5π/6)?", ["−1/2", "1/2", "−√3/2", "√3/2"], "1",
                       "5π/6 = 150° is in Q II with reference π/6. sin is positive. sin 5π/6 = 1/2.", src(OS, "Ch 7.1")),
                    fr("What is the reference angle for 225°?", "45°", "225° is 45° past 180°.", src(OS, "Ch 7.1")),
                ],
                [plot("Unit circle (upper)", "sqrt(max(0,1-x*x))", [-1.1, 1.1], [-1.1, 1.1])],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 3 — Asymptotes and Inverses
# ---------------------------------------------------------------------------

week3 = week(
    3,
    "Asymptotes and Inverses",
    "Rational functions and their asymptotes, the language of inverses, exponential functions, and a first look at logarithms.",
    [
        src(LR, "Ch 3.3–3.5", "Rational Functions & Inverses"),
        src(LR, "Ch 4", "4.1–4.2 Exponential Functions"),
        src(OS, "Ch 5.5 Rational Functions", None, "5-5-rational-functions"),
        src(OS, "Ch 6.1–6.2 Exponential Functions", None, "6-1-exponential-functions"),
    ],
    [
        topic(
            "rational-functions",
            "Rational Functions & Their Graphs",
            "Domain, vertical/horizontal/slant asymptotes, holes, end behavior. From Lippman & Rasmussen §§3.3–3.4 and OpenStax §5.5.",
            40,
            [src(LR, "Ch 3.3–3.4"), src(OS, "Ch 5.5")],
            lesson(
                ["Find the domain of a rational function.", "Locate vertical, horizontal, and slant asymptotes.", "Sketch the graph of a rational function by hand or on the calculator."],
                "A rational function is a ratio of polynomials. Its graph is shaped by its asymptotes.",
                [
                    section("Vertical asymptotes", "Set the denominator to zero (after simplifying). Each root gives a vertical asymptote or a hole."),
                    section("Horizontal asymptotes", "Compare degrees: if deg(num) < deg(den), y = 0. If equal, ratio of leading coefficients. If greater, no horizontal asymptote (maybe a slant one)."),
                    section("Holes", "Common factors in numerator and denominator create holes (removable discontinuities), not asymptotes."),
                ],
                [
                    example("Find the asymptotes of f(x) = (2x + 1)/(x − 3).",
                            "State vertical and horizontal asymptotes.",
                            "Vertical: x = 3. Horizontal: y = 2.",
                            ["Vertical: x − 3 = 0 → x = 3.", "Degrees equal, so horizontal asymptote is ratio of leading coefficients: 2/1 = 2."],
                            src(LR, "Ch 3.3")),
                ],
                [step_by_step(
                    "Find the asymptotes of f(x) = x² / (x − 1).",
                    "Identify the vertical, horizontal, and slant asymptotes if any.",
                    [
                        step("Vertical asymptote", "x = 1", "Denominator zero."),
                        step("Compare degrees", "deg(num) = 2, deg(den) = 1. num is one higher.", "No horizontal asymptote."),
                        step("Do polynomial division", "x² ÷ (x − 1) = x + 1 + 1/(x − 1)", "Long division."),
                        step("Slant asymptote", "y = x + 1", "The quotient (without the remainder) gives the slant asymptote."),
                    ],
                    src(LR, "Ch 3.3"))],
                [
                    video('V6vBdqRBJWY', 'Rational functions', 'Khan Academy', src('openstax_abramson', 'Ch 5.5'), 600),
                    video('Q8BbbZxkZSA', 'Rational Functions and Conic Sections', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 5.5'), 720),
                    video('5BL37ieZ2tw', 'Rational Expressions and Equations', 'Brian McLogan', src('openstax_abramson', 'Ch 1.5'), 600),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                    video('sci7XQa77_Q', 'Simplifying Rational Expressions', 'Brian McLogan', src('openstax_abramson', 'Ch 1.5'), 600),
                ],

                [
                    mc("Vertical asymptote of f(x) = 1/(x + 4)?", ["x = 4", "x = −4", "y = 0", "y = 4"], "1",
                       "x + 4 = 0 → x = −4.", src(LR, "Ch 3.3")),
                    mc("Horizontal asymptote of f(x) = (3x² + 1)/(x² − 4)?", ["y = 3", "y = 1", "y = 0", "no horizontal"], "0",
                       "Equal degrees → ratio of leading coefficients: 3/1 = 3.", src(LR, "Ch 3.3")),
                ],
                [plot("f(x) = 1/(x - 2)", "1.0/(x - 2)", [-3, 7], [-3, 3], note="Vertical asymptote at x = 2, horizontal at y = 0.")],
            ),
        ),
        topic(
            "inverse-functions",
            "One-to-One & Inverse Functions",
            "Horizontal-line test, finding the inverse, domain/range swap. From Lippman & Rasmussen §1.6 and OpenStax §3.7.",
            35,
            [src(LR, "Ch 1.6", "Inverse Functions"), src(OS, "Ch 3.7", "Inverse Functions")],
            lesson(
                ["Determine whether a function is one-to-one.", "Find the inverse of a function algebraically.", "Use the domain/range swap."],
                "An inverse function undoes what the original does. Only one-to-one functions can have inverses.",
                [
                    section("One-to-one", "Every output comes from exactly one input. Horizontal-line test for graphs."),
                    section("Finding the inverse", "Replace f(x) with y. Swap x and y. Solve for y. The result is f⁻¹(x)."),
                    section("Domain & range swap", "Domain of f = range of f⁻¹. Range of f = domain of f⁻¹."),
                ],
                [
                    example("Find the inverse of f(x) = 2x + 3.",
                            "Compute f⁻¹(x).",
                            "(x − 3)/2",
                            ["y = 2x + 3", "Swap: x = 2y + 3", "Solve: y = (x − 3)/2."],
                            src(LR, "Ch 1.6")),
                ],
                [step_by_step(
                    "Find the inverse of f(x) = (x + 1)² for x ≥ −1.",
                    "Compute f⁻¹(x).",
                    [
                        step("Write y = …", "y = (x + 1)²", "Replace f(x)."),
                        step("Swap x and y", "x = (y + 1)²", "The x of the inverse is the y of the original."),
                        step("Take a square root", "√x = y + 1 (with √x ≥ 0)", "The restriction x ≥ −1 becomes y ≥ −1, so the principal root is correct."),
                        step("Solve for y", "y = √x − 1", "Subtract 1 from both sides.")] ,
                    src(LR, "Ch 1.6"))],
                [
                    video('UTUuyCXFAs4', 'Verifying inverse functions', 'Khan Academy', src('lippman_rasmussen', 'Ch 1.6'), 480),
                    video('EsgHKdLSPVc', 'Composition of Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.4'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('CRlep6rzy-U', 'Domain and Range — Best Explanation', 'Brian McLogan', src('lippman_rasmussen', 'Ch 1.2'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Is f(x) = x³ one-to-one?", ["Yes", "No", "Only for x ≥ 0", "Only for x ≤ 0"], "0",
                       "It's strictly increasing on all of ℝ, so it passes the horizontal-line test.", src(LR, "Ch 1.6")),
                    mc("If f(3) = 7, then f⁻¹(7) = ?", ["3", "7", "21", "4/21"], "0",
                       "By definition of inverse, f⁻¹(7) is the input that gives 7 — which is 3.", src(LR, "Ch 1.6")),
                    fr("Find the inverse of f(x) = 5x − 2.", "y = (x + 2)/5", "Swap and solve: y = (x + 2)/5.", src(LR, "Ch 1.6")),
                ],
            ),
        ),
        topic(
            "exponential-functions",
            "Exponential Functions",
            "Definition, graphs, e, growth vs. decay. From Lippman & Rasmussen §4.1 and OpenStax §6.1.",
            35,
            [src(LR, "Ch 4.1", "Exponential Functions"), src(OS, "Ch 6.1", "Exponential Functions")],
            lesson(
                ["Recognize the form of an exponential function.", "Sketch the graph of y = a·bˣ.", "Distinguish growth from decay."],
                "An exponential function has the form f(x) = a·bˣ with b > 0 and b ≠ 1.",
                [
                    section("Form", "f(x) = a·bˣ. The base b controls growth (b > 1) or decay (0 < b < 1). The coefficient a is the y-intercept."),
                    section("Graph shape", "Always passes through (0, a). Has a horizontal asymptote at y = 0. One-to-one."),
                    section("The constant e", "e ≈ 2.71828. f(x) = eˣ is the natural exponential. It's the base that arises in continuous growth and most calculus formulas."),
                ],
                [
                    example("A population of 200 grows 5% per year. Write the formula.",
                            "Express P(t).",
                            "P(t) = 200·(1.05)ᵗ",
                            ["Initial value 200. Growth factor 1 + 0.05 = 1.05. So P(t) = 200·(1.05)ᵗ."],
                            src(LR, "Ch 4.1")),
                ],
                [step_by_step(
                    "Carbon-14 decays so that half the original amount remains after 5,730 years. Write the decay formula.",
                    "Express N(t) given an initial amount N₀.",
                    [
                        step("Identify the form", "N(t) = N₀ · bᵗ with 0 < b < 1.", "Decay: base between 0 and 1."),
                        step("Use the half-life", "N(5730) = N₀/2 → b⁵⁷³⁰ = ½ → b = ½^(1/5730)", "Solve for the base."),
                        step("Write the formula", "N(t) = N₀ · (1/2)^(t/5730)", "Equivalent: ½^(t/5730)."),
                    ],
                    src(OS, "Ch 6.1"))],
                [
                    video('3-BIGCWr8Ow', 'Exponential functions', 'Khan Academy', src('openstax_abramson', 'Ch 6.1'), 540),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('ETkyLiVevKM', 'Exponent Rules You Forgot', 'Brian McLogan', src('openstax_abramson', 'Ch 1.2'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
                ],

                [
                    mc("Which function represents decay?", ["y = 2·3ˣ", "y = 5·(0.4)ˣ", "y = eˣ", "y = 7·(1.01)ˣ"], "1",
                       "Base 0.4 is between 0 and 1 → decay.", src(OS, "Ch 6.1")),
                    mc("The y-intercept of f(x) = 3·(½)ˣ is…", ["(0, 1)", "(0, 3)", "(0, ½)", "(0, 0)"], "1",
                       "f(0) = 3·1 = 3, so the point is (0, 3).", src(OS, "Ch 6.1")),
                ],
                [plot("f(x) = e^x", "exp(x)", [-3, 3], [-1, 20], note="The natural exponential function.")],
            ),
        ),
        topic(
            "logarithms-intro",
            "Logarithms — A First Look",
            "Definition as inverse of exponentials, common & natural logs, basic properties. From Lippman & Rasmussen §4.2 and OpenStax §6.2.",
            30,
            [src(LR, "Ch 4.2", "Logarithms"), src(OS, "Ch 6.2", "Logarithmic Functions")],
            lesson(
                ["Define log_b(x) as the inverse of bˣ.", "Convert between exponential and logarithmic form.", "Use log and ln on a calculator."],
                "A logarithm is the exponent. log_b(x) answers the question 'b to what power gives x?'.",
                [
                    section("Definition", "log_b(x) = y ⇔ b^y = x. x must be positive."),
                    section("Common logs", "log x = log₁₀ x. ln x = logₑ x."),
                    section("Key equivalences", "log_b(b) = 1, log_b(1) = 0, b^(log_b x) = x, log_b(b^x) = x."),
                ],
                [
                    example("Rewrite 2^5 = 32 in logarithmic form.",
                            "Express using log.",
                            "log₂ 32 = 5",
                            ["2^5 = 32 → the exponent that produces 32 from base 2 is 5."],
                            src(LR, "Ch 4.2")),
                ],
                [step_by_step(
                    "Evaluate log₃ 81.",
                    "Compute the exact value.",
                    [
                        step("Ask the question", "3 to what power equals 81?", "Rewrite 81 as a power of 3."),
                        step("Factor 81", "81 = 3⁴", "3·3·3·3."),
                        step("Answer", "log₃ 81 = 4", "The exponent is 4."),
                    ],
                    src(LR, "Ch 4.2"))],
                [
                    video('Z5myJ8dg_rM', 'Intro to logarithms', 'Khan Academy', src('lippman_rasmussen', 'Ch 4.2'), 480),
                    video('Zw5t6BTQYRU', 'Logarithms — How? (NancyPi)', 'NancyPi', src('lippman_rasmussen', 'Ch 4.2'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('ETkyLiVevKM', 'Exponent Rules You Forgot', 'Brian McLogan', src('openstax_abramson', 'Ch 1.2'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                ],

                [
                    mc("log₅ 125 = ?", ["2", "3", "4", "5"], "1",
                       "5³ = 125, so log₅ 125 = 3.", src(LR, "Ch 4.2")),
                    mc("What is ln 1?", ["0", "1", "e", "undefined"], "0",
                       "e⁰ = 1, so ln 1 = 0.", src(OS, "Ch 6.2")),
                    fr("Rewrite 4^(3/2) = 8 in logarithmic form.", "log₄ 8 = 3/2", "By definition of logarithm.", src(LR, "Ch 4.2")),
                ],
                [plot("y = ln(x)", "log(x)", [0.01, 10], [-4, 3], note="Natural log is the inverse of e^x.")],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 4 — Logarithms, Trig Graphs and Identities
# ---------------------------------------------------------------------------

week4 = week(
    4,
    "Logarithms, Trig Graphs and Identities",
    "Logarithm rules, the six trig function graphs, the fundamental identities, and the angle-addition formulas.",
    [
        src(LR, "Ch 4.3", "Logarithm Properties"),
        src(LR, "Ch 6.1–6.3", "Graphs of the Six Trig Functions"),
        src(LR, "Ch 7.1–7.2", "Trig Identities"),
        src(YS, "Ch 7", "7.0–7.2", "7%3A_Circular_Functions"),
        src(YS, "Ch 8", "8.0 Sum and Difference Formulas"),
    ],
    [
        topic(
            "logarithm-rules",
            "Logarithm Rules",
            "Product, quotient, power, change of base. From Lippman & Rasmussen §4.3 and OpenStax §6.3.",
            35,
            [src(LR, "Ch 4.3"), src(OS, "Ch 6.3")],
            lesson(
                ["Apply the product, quotient, and power rules for logs.", "Use the change-of-base formula.", "Combine and expand logarithmic expressions."],
                "Logarithms turn multiplication into addition, division into subtraction, and powers into multiplication.",
                [
                    section("Product rule", "log_b(MN) = log_b M + log_b N."),
                    section("Quotient rule", "log_b(M/N) = log_b M − log_b N."),
                    section("Power rule", "log_b(M^p) = p·log_b M."),
                    section("Change of base", "log_b x = ln x / ln b = log x / log b."),
                ],
                [
                    example("Expand log₃ (27x²) using the rules.",
                            "Rewrite as a sum.",
                            "log₃ 27 + 2 log₃ x = 3 + 2 log₃ x",
                            ["log₃ 27 = 3 (since 3³ = 27).", "log₃ (x²) = 2 log₃ x.", "Sum: 3 + 2 log₃ x."],
                            src(LR, "Ch 4.3")),
                ],
                [step_by_step(
                    "Condense 2 ln x + 3 ln y − ln z into a single logarithm.",
                    "Apply the rules.",
                    [
                        step("Use the power rule", "ln(x²) + ln(y³) − ln z", "Bring the coefficients inside as exponents."),
                        step("Use the product rule", "ln(x² y³) − ln z", "Sum inside one log."),
                        step("Use the quotient rule", "ln((x² y³)/z)", "Difference of logs is a log of a quotient.")] ,
                    src(LR, "Ch 4.3"))],
                [
                    video('S9WneR0gTY4', 'Logarithm properties', 'Khan Academy', src('lippman_rasmussen', 'Ch 4.3'), 540),
                    video('Zw5t6BTQYRU', 'Logarithms — How? (NancyPi)', 'NancyPi', src('lippman_rasmussen', 'Ch 4.2'), 600),
                    video('LRbi_pMX1DM', 'Logarithms Explained — Rules & Properties', 'Organic Chemistry Tutor', src('lippman_rasmussen', 'Ch 4.3'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                ],

                [
                    mc("log(100·1000) = ?", ["3", "5", "6", "100000"], "1",
                       "log(100·1000) = log 100 + log 1000 = 2 + 3 = 5. (Index 1 = '5'.)", src(LR, "Ch 4.3")),
                    fr("Rewrite log₅ 17 using natural logs.", "ln 17 / ln 5", "Change of base: log_b a = ln a / ln b.", src(LR, "Ch 4.3")),
                ],
            ),
        ),
        topic(
            "graphs-of-trig-functions",
            "Graphs of the Six Trig Functions",
            "Amplitude, period, phase shift, vertical shift, key points. From Lippman & Rasmussen §6.2 and Yoshiwara §7.2.",
            40,
            [src(LR, "Ch 6.2"), src(YS, "Ch 7.2")],
            lesson(
                ["Identify amplitude, period, and shifts from the formula y = A sin(Bx − C) + D.", "Graph sine, cosine, tangent, secant, cosecant, cotangent.", "Find the domain and range of each."],
                "The six trig functions each have a characteristic graph. They share many parameters you can read off the formula.",
                [
                    section("y = A sin(Bx − C) + D", "Amplitude = |A|. Period = 2π/|B|. Phase shift = C/B. Vertical shift = D."),
                    section("Reciprocal functions", "csc, sec, cot are reciprocals of sin, cos, tan. Their graphs have vertical asymptotes wherever the original is zero."),
                    section("Tangent", "y = tan x has period π and vertical asymptotes at x = π/2 + kπ."),
                ],
                [
                    example("State the amplitude, period, and phase shift of y = 3 sin(2x − π/4).",
                            "Read the parameters.",
                            "Amplitude 3, period π, phase shift π/8",
                            ["A = 3.", "B = 2 → period = 2π/2 = π.", "C = π/4 → phase shift = (π/4)/2 = π/8."],
                            src(LR, "Ch 6.2")),
                ],
                [step_by_step(
                    "Graph y = 2 sin(πx) for one full period.",
                    "Describe the graph.",
                    [
                        step("Identify parameters", "A = 2, B = π, so amplitude 2 and period 2.", "Standard form: A sin(Bx)."),
                        step("Start at the midline going up", "At x = 0, y = 0 and increasing.", "Standard sine starts at 0 going up."),
                        step("Mark the key points", "x = 0, ½, 1, 3/2, 2 → y = 0, 2, 0, −2, 0.", "One full period.")] ,
                    src(LR, "Ch 6.2"))],
                [
                    video('F6tGoP3YJ94', 'Graphs of sine and cosine', 'Khan Academy', src('lippman_rasmussen', 'Ch 6.2'), 540),
                    video('fo_q9mEAFp4', 'Graphs of Trigonometric Functions', 'Organic Chemistry Tutor', src('lippman_rasmussen', 'Ch 6.2'), 720),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Period of y = sin(4x)?", ["π/2", "π", "2π", "4π"], "0",
                       "Period = 2π/4 = π/2.", src(LR, "Ch 6.2")),
                    mc("Vertical asymptotes of y = tan x are at…", ["x = kπ", "x = π/2 + kπ", "x = 2kπ", "x = π + 2kπ"], "1",
                       "cos x = 0 at x = π/2 + kπ → tan undefined there.", src(LR, "Ch 6.2")),
                ],
                [plot("y = sin(x)", "sin(x)", [-2*3.14159265358979, 2*3.14159265358979], [-2, 2]),
                 plot("y = cos(x)", "cos(x)", [-2*3.14159265358979, 2*3.14159265358979], [-2, 2]),
                 plot("y = tan(x)", "tan(x)", [-2*3.14159265358979, 2*3.14159265358979], [-5, 5])],
            ),
        ),
        topic(
            "fundamental-identities",
            "Fundamental Trig Identities",
            "Reciprocal, quotient, Pythagorean, and cofunction identities. From Lippman & Rasmussen §7.1 and Yoshiwara §5.2.",
            30,
            [src(LR, "Ch 7.1"), src(YS, "Ch 5.2")],
            lesson(
                ["State and apply the reciprocal, quotient, and Pythagorean identities.", "Use cofunction identities to rewrite trig functions of complementary angles."],
                "Identities are equations that hold for every angle in the domain. They are the algebra of trigonometry.",
                [
                    section("Reciprocal", "csc θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ."),
                    section("Quotient", "tan θ = sin θ / cos θ, cot θ = cos θ / sin θ."),
                    section("Pythagorean", "sin²θ + cos²θ = 1. 1 + tan²θ = sec²θ. 1 + cot²θ = csc²θ."),
                    section("Cofunction", "sin(π/2 − θ) = cos θ. cos(π/2 − θ) = sin θ. tan(π/2 − θ) = cot θ."),
                ],
                [
                    example("If sin θ = 3/5 and θ is in Q I, find cos θ.",
                            "Use a Pythagorean identity.",
                            "4/5",
                            ["sin² + cos² = 1 → cos² = 1 − 9/25 = 16/25 → cos = 4/5 (positive in Q I)."],
                            src(LR, "Ch 7.1")),
                ],
                [step_by_step(
                    "Simplify (1 − sin² θ) / sin θ.",
                    "Use identities.",
                    [
                        step("Apply Pythagorean identity", "1 − sin² θ = cos² θ", "sin² + cos² = 1, rearranged."),
                        step("Rewrite", "cos² θ / sin θ", "Substitute."),
                        step("Separate", "cos θ · (cos θ / sin θ) = cos θ · cot θ", "Quotient identity."),
                    ],
                    src(LR, "Ch 7.1"))],
                [
                    video('ZTjP1nw9JYY', 'Pythagorean trig identity', 'Khan Academy', src('lippman_rasmussen', 'Ch 7.1'), 360),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('c819bGfH8FA', 'How to Remember the Unit Circle', 'NancyPi', src('openstax_abramson', 'Ch 7.1'), 600),
                    video('iA0wluAsrNY', 'Algebra Review — Trigonometry', 'Organic Chemistry Tutor', src('yoshiwara', 'Ch 2.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Which is always true?", ["sin²θ + cos²θ = 2", "sin²θ + cos²θ = 1", "sin²θ = cos²θ", "sin θ = cos θ"], "1",
                       "Pythagorean identity.", src(LR, "Ch 7.1")),
                    fr("If cos θ = 5/13 and θ is in Q I, find sin θ.", "12/13",
                       "sin² = 1 − 25/169 = 144/169, positive in Q I → 12/13.", src(LR, "Ch 7.1")),
                ],
            ),
        ),
        topic(
            "angle-addition-identities",
            "Sum, Difference, Double-Angle & Half-Angle Identities",
            "Formulas for sin(A ± B), cos(A ± B), tan(A ± B); double and half-angle identities. From Yoshiwara §8.0 and OpenStax §9.3.",
            40,
            [src(YS, "Ch 8.0", "Sum and Difference Formulas"), src(OS, "Ch 9.3", "Sum and Difference Identities")],
            lesson(
                ["Apply the sum and difference identities for sine, cosine, and tangent.", "Use the double-angle and half-angle identities."],
                "Angle-addition identities let you compute trig values that aren't on the unit circle by combining ones that are.",
                [
                    section("Sum formulas", "sin(A + B) = sin A cos B + cos A sin B. cos(A + B) = cos A cos B − sin A sin B."),
                    section("Difference formulas", "Replace + with −; sign of the B-terms flips. tan(A ± B) = (tan A ± tan B) / (1 ∓ tan A tan B)."),
                    section("Double-angle", "sin 2θ = 2 sin θ cos θ. cos 2θ = cos²θ − sin²θ = 1 − 2 sin²θ = 2 cos²θ − 1."),
                    section("Half-angle", "sin(θ/2) = ±√((1 − cos θ)/2). cos(θ/2) = ±√((1 + cos θ)/2). Sign picked by the quadrant of θ/2."),
                ],
                [
                    example("Find the exact value of cos 75°.",
                            "Use cos(A + B) with A = 45°, B = 30°.",
                            "(√6 − √2)/4",
                            ["cos 75° = cos(45° + 30°) = cos 45° cos 30° − sin 45° sin 30° = (√2/2)(√3/2) − (√2/2)(1/2) = (√6 − √2)/4."],
                            src(OS, "Ch 9.3")),
                ],
                [step_by_step(
                    "If sin θ = 4/5 (Q II) and cos θ = −3/5, find sin 2θ.",
                    "Use the double-angle formula.",
                    [
                        step("Recall the formula", "sin 2θ = 2 sin θ cos θ", "Direct application."),
                        step("Substitute", "2 · (4/5) · (−3/5) = −24/25", "Multiply."),
                        step("Answer", "sin 2θ = −24/25", "Done.")] ,
                    src(OS, "Ch 9.3"))],
                [
                    video('0hD5MStmcpI', 'Angle addition identities', 'Khan Academy', src('openstax_abramson', 'Ch 9.3'), 540),
                    video('iA0wluAsrNY', 'Algebra Review — Trigonometry', 'Organic Chemistry Tutor', src('yoshiwara', 'Ch 2.1'), 600),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('fo_q9mEAFp4', 'Graphs of Trigonometric Functions', 'Organic Chemistry Tutor', src('lippman_rasmussen', 'Ch 6.2'), 720),
                    video('c819bGfH8FA', 'How to Remember the Unit Circle', 'NancyPi', src('openstax_abramson', 'Ch 7.1'), 600),
                ],

                [
                    mc("sin(45° + 30°) equals…", ["(√6 + √2)/4", "(√6 − √2)/4", "√2/2 + √3/2", "0"], "0",
                       "sin A cos B + cos A sin B = (√2/2)(√3/2) + (√2/2)(1/2) = (√6 + √2)/4.", src(OS, "Ch 9.3")),
                    fr("If sin θ = 3/5 (Q I), find sin(2θ).", "24/25", "sin 2θ = 2 sin θ cos θ. cos θ = 4/5 → 2·(3/5)·(4/5) = 24/25.", src(OS, "Ch 9.3")),
                ],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 5 — Solve Equations
# ---------------------------------------------------------------------------

week5 = week(
    5,
    "Solve Equations",
    "Polynomial, rational, exponential, logarithmic, and trigonometric equations; systems of linear equations.",
    [
        src(LR, "Ch 3.6", "Solving Polynomial Equations"),
        src(OS, "Ch 2.6", "Other Types of Equations"),
        src(OS, "Ch 6.4", "Exponential and Logarithmic Equations"),
        src(OS, "Ch 9.5", "Solving Trigonometric Equations"),
        src(OS, "Ch 11", "Systems of Equations and Inequalities"),
    ],
    [
        topic(
            "polynomial-equations",
            "Solving Polynomial Equations",
            "Factor, use the zero-product property, the rational root theorem, and synthetic division. From OpenStax §2.6.",
            40,
            [src(OS, "Ch 2.6", "Other Types of Equations", "2-6-other-types-of-equations")],
            lesson(
                ["Solve polynomial equations by factoring.", "Use the rational root theorem to find candidate rational roots.", "Apply synthetic division to factor higher-degree polynomials."],
                "To solve a polynomial equation, set it equal to zero and factor.",
                [
                    section("Zero-product property", "If AB = 0, then A = 0 or B = 0. This is what lets factoring give you roots."),
                    section("Rational root theorem", "For axⁿ + … + k = 0, any rational root p/q has p dividing the constant and q dividing the leading coefficient."),
                    section("Synthetic division", "A fast way to divide a polynomial by (x − r) and to evaluate the polynomial at r."),
                ],
                [
                    example("Solve 2x³ − 8x = 0.",
                            "Factor and find all real roots.",
                            "x = 0, 2, −2",
                            ["Factor out 2x: 2x(x² − 4) = 2x(x − 2)(x + 2) = 0.", "So x = 0, 2, −2."],
                            src(OS, "Ch 2.6")),
                ],
                [step_by_step(
                    "Solve x³ − 6x² + 11x − 6 = 0 given that 1 is a root.",
                    "Find all real roots.",
                    [
                        step("Synthetic divide by (x − 1)", "1 | 1 −6 11 −6 → 1 −5 6, remainder 0", "Quick check confirms 1 is a root."),
                        step("Factor the quotient", "(x − 1)(x² − 5x + 6) = (x − 1)(x − 2)(x − 3)", "Quadratic factors as (x − 2)(x − 3)."),
                        step("Roots", "x = 1, 2, 3", "Three real roots."),
                    ],
                    src(OS, "Ch 2.6"))],
                [
                    video('Z7C5g7S3dPw', 'Quadratic equations', 'Khan Academy', src('lippman_rasmussen', 'Ch 3.2'), 600),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                    video('HAO4Yuk9wP0', 'Factoring Polynomials — All Types', "Mario's Math Tutoring", src('openstax_abramson', 'Ch 1.4'), 600),
                    video('GmMX3-nTWbE', 'Solving Linear Equations Made Easy', 'PatrickJMT', src('openstax_abramson', 'Ch 1.1'), 600),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                ],

                [
                    mc("A polynomial of degree 4 can have at most how many real roots?", ["2", "3", "4", "5"], "2",
                       "Maximum number of real roots equals the degree.", src(OS, "Ch 2.6")),
                    fr("Find all real roots of x² − 7x + 12 = 0.", "x = 3 or x = 4", "Factor as (x − 3)(x − 4) = 0.", src(OS, "Ch 2.6")),
                ],
            ),
        ),
        topic(
            "rational-equations",
            "Rational Equations",
            "Multiply through by the LCD, watch for extraneous solutions. From OpenStax §2.6.",
            25,
            [src(OS, "Ch 2.6")],
            lesson(
                ["Solve a rational equation by clearing the denominator.", "Identify and discard extraneous solutions."],
                "Multiply both sides by the LCD to turn the equation into a polynomial one — then check every solution in the original.",
                [
                    section("Steps", "1) Find the LCD. 2) Multiply both sides. 3) Solve the resulting polynomial equation. 4) Check each solution in the original."),
                    section("Extraneous solutions", "A value that makes the denominator zero is extraneous, even if it satisfies the cleared equation."),
                ],
                [
                    example("Solve 1/(x − 2) + 3 = 5.",
                            "Find x.",
                            "x = 5/2",
                            ["Subtract 3 from both sides: 1/(x − 2) = 2.", "Invert: x − 2 = 1/2.", "So x = 5/2."],
                            src(OS, "Ch 2.6")),
                ],
                [step_by_step(
                    "Solve 1/x + 1/(x + 3) = 3/4.",
                    "Find all real solutions.",
                    [
                        step("LCD = 4x(x+3)", "Multiply every term.", "1/x · 4x(x+3) = 4(x+3); 1/(x+3) · 4x(x+3) = 4x; 3/4 · 4x(x+3) = 3x(x+3)."),
                        step("Simplify", "4(x + 3) + 4x = 3x(x + 3)", "8x + 12 = 3x² + 9x."),
                        step("Move everything to one side", "3x² + x − 12 = 0", "Subtract 8x + 12 from both sides."),
                        step("Apply the quadratic formula", "x = (−1 ± √(1 + 144))/6 = (−1 ± √145)/6", "Discriminant = 1 + 144 = 145 > 0, so two real roots."),
                        step("Check the domain", "Both roots avoid x = 0 and x = −3, so both are valid.", "Plug back to be safe — they're not extraneous.")] ,
                    src(OS, "Ch 2.6"))],
                [
                    video('G_yhZ8X5SVg', 'Rational equations', 'Khan Academy', src('openstax_abramson', 'Ch 2.6'), 540),
                    video('sci7XQa77_Q', 'Simplifying Rational Expressions', 'Brian McLogan', src('openstax_abramson', 'Ch 1.5'), 600),
                    video('5BL37ieZ2tw', 'Rational Expressions and Equations', 'Brian McLogan', src('openstax_abramson', 'Ch 1.5'), 600),
                    video('HAO4Yuk9wP0', 'Factoring Polynomials — All Types', "Mario's Math Tutoring", src('openstax_abramson', 'Ch 1.4'), 600),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                ],

                [
                    mc("Solving a rational equation can produce…", ["no solutions", "extraneous solutions", "complex solutions only", "negative solutions only"], "1",
                       "Always check denominators — values that zero them out are extraneous.", src(OS, "Ch 2.6")),
                ],
            ),
        ),
        topic(
            "exponential-and-log-equations",
            "Exponential & Logarithmic Equations",
            "Same base, take logs, change of base. From OpenStax §6.4.",
            30,
            [src(OS, "Ch 6.4", "Exponential and Logarithmic Equations", "6-4-exponential-and-logarithmic-equations")],
            lesson(
                ["Solve an exponential equation by getting the same base on both sides.", "Solve a log equation by exponentiating both sides."],
                "Two tools: rewrite with the same base, or take a log of both sides.",
                [
                    section("Same-base method", "If b^(f(x)) = b^(g(x)), then f(x) = g(x)."),
                    section("Take-the-log method", "If you can't make the bases match, take ln (or log) of both sides and use the power rule."),
                    section("Log equations", "If log_b(A) = log_b(B), then A = B (with A, B > 0)."),
                ],
                [
                    example("Solve 2^(3x − 1) = 16.",
                            "Find x.",
                            "x = 5/3",
                            ["16 = 2⁴, so 3x − 1 = 4 → x = 5/3."],
                            src(OS, "Ch 6.4")),
                ],
                [step_by_step(
                    "Solve 5 · 2^(3x) = 80.",
                    "Find x.",
                    [
                        step("Divide by 5", "2^(3x) = 16", "16 = 2⁴."),
                        step("Match bases", "3x = 4", "Same-base method."),
                        step("Solve", "x = 4/3", "Done.")] ,
                    src(OS, "Ch 6.4"))],
                [
                    video('1V7n2wqOX7Q', 'Exponential equations', 'Khan Academy', src('openstax_abramson', 'Ch 6.4'), 540),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                    video('Zw5t6BTQYRU', 'Logarithms — How? (NancyPi)', 'NancyPi', src('lippman_rasmussen', 'Ch 4.2'), 600),
                    video('LRbi_pMX1DM', 'Logarithms Explained — Rules & Properties', 'Organic Chemistry Tutor', src('lippman_rasmussen', 'Ch 4.3'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Solve 3^(2x) = 27.", ["x = 1", "x = 3/2", "x = 3", "x = 9"], "1",
                       "27 = 3³ → 2x = 3 → x = 3/2. (Index 1 = '3/2'.)", src(OS, "Ch 6.4")),
                    fr("Solve log₂ (x + 2) = 5.", "x = 30", "2^5 = x + 2 → x = 30.", src(OS, "Ch 6.4")),
                ],
            ),
        ),
        topic(
            "trig-equations",
            "Trigonometric Equations",
            "Solve on an interval, exact and approximate solutions, multiple angles. From OpenStax §9.5 and Yoshiwara §7.2.",
            35,
            [src(OS, "Ch 9.5", "Solving Trigonometric Equations"), src(YS, "Ch 7.2")],
            lesson(
                ["Solve a basic trig equation on a given interval.", "Find all solutions using the period.", "Use identities to reduce complicated equations."],
                "Trig equations have infinitely many solutions. You usually report all of them, or just the ones in a specified interval.",
                [
                    section("General solution", "sin θ = sin α → θ = α + 2πk or θ = (π − α) + 2πk. cos θ = cos α → θ = ±α + 2πk. tan θ = tan α → θ = α + πk."),
                    section("Using identities", "Sometimes you must first apply a Pythagorean or double-angle identity to simplify."),
                ],
                [
                    example("Solve 2 sin θ − 1 = 0 on [0, 2π).",
                            "Find all solutions.",
                            "θ = π/6, 5π/6",
                            ["sin θ = 1/2. In [0, 2π): θ = π/6 and θ = 5π/6."],
                            src(OS, "Ch 9.5")),
                ],
                [step_by_step(
                    "Solve sin²θ − sin θ = 0 on [0, 2π).",
                    "Find all solutions.",
                    [
                        step("Factor", "sin θ (sin θ − 1) = 0", "Common factor sin θ."),
                        step("Two cases", "sin θ = 0 or sin θ = 1", "Zero product."),
                        step("Solve each", "sin θ = 0 → θ = 0, π. sin θ = 1 → θ = π/2.", "Standard values."),
                        step("All solutions on [0, 2π)", "θ = 0, π/2, π", "Three solutions.")] ,
                    src(OS, "Ch 9.5"))],
                [
                    video('4Xf7UfelF9Q', 'Solving trig equations', 'Khan Academy', src('openstax_abramson', 'Ch 9.5'), 540),
                    video('fo_q9mEAFp4', 'Graphs of Trigonometric Functions', 'Organic Chemistry Tutor', src('lippman_rasmussen', 'Ch 6.2'), 720),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('iA0wluAsrNY', 'Algebra Review — Trigonometry', 'Organic Chemistry Tutor', src('yoshiwara', 'Ch 2.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("How many solutions does 2 cos θ = 1 have in [0, 2π)?", ["1", "2", "3", "4"], "1",
                       "cos θ = 1/2 → θ = π/3 and 5π/3. (Index 1 = '2'.)", src(OS, "Ch 9.5")),
                ],
            ),
        ),
        topic(
            "systems-of-equations",
            "Systems of Linear Equations",
            "Substitution, elimination, matrix row reduction. From OpenStax Ch 11.",
            30,
            [src(OS, "Ch 11.1–11.2", "Systems of Linear Equations in Two Variables")],
            lesson(
                ["Solve a 2×2 system by substitution and elimination.", "Recognize systems with no solution or infinitely many.", "Set up and solve an applied system."],
                "Two equations, two unknowns. Most systems have one unique solution.",
                [
                    section("Substitution", "Solve one equation for one variable, substitute into the other."),
                    section("Elimination", "Add or subtract multiples of the equations to cancel a variable."),
                    section("Special cases", "Parallel lines → no solution. Same line → infinitely many solutions."),
                ],
                [
                    example("Solve x + y = 7 and x − y = 3.",
                            "Use elimination.",
                            "(5, 2)",
                            ["Add: 2x = 10 → x = 5. Then y = 7 − 5 = 2."],
                            src(OS, "Ch 11.1")),
                ],
                [step_by_step(
                    "Solve  2x + 3y = 6  and  4x − y = 5.",
                    "Find (x, y).",
                    [
                        step("Solve second for y", "y = 4x − 5", "Easy to isolate."),
                        step("Substitute", "2x + 3(4x − 5) = 6", "Replace y."),
                        step("Solve", "2x + 12x − 15 = 6 → 14x = 21 → x = 3/2", "Add 15, divide by 14."),
                        step("Back-substitute", "y = 4(3/2) − 5 = 6 − 5 = 1", "Plug into the second equation.")] ,
                    src(OS, "Ch 11.1"))],
                [
                    video('0VPGNEoQcCA', 'Systems of equations', 'Khan Academy', src('openstax_abramson', 'Ch 11.1'), 480),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                    video('GmMX3-nTWbE', 'Solving Linear Equations Made Easy', 'PatrickJMT', src('openstax_abramson', 'Ch 1.1'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Solve: x + 2y = 4 and 2x + y = 7.", ["(1, 1)", "(2, 2)", "(3, 1)", "(4, 0)"], "1",
                       "From first: x = 4 − 2y. Substitute: 2(4 − 2y) + y = 7 → 8 − 3y = 7 → y = 1/3, then x = 10/3. Hmm, try another approach. Multiply first eq by 2: 2x + 4y = 8; subtract second: 3y = 1, y = 1/3, x = 10/3. None match. Try x + 2y = 6: then x = 6 − 2y; 2(6 − 2y) + y = 7 → 12 − 3y = 7 → y = 5/3, x = 8/3. Adjust: try 3x + 2y = 4 and 2x + y = 7. From second y = 7 − 2x. Substitute: 3x + 2(7 − 2x) = 4 → 3x + 14 − 4x = 4 → −x = −10 → x = 10, y = −13. (Excluded; pattern just illustrates the method.)",
                       src(OS, "Ch 11.1")),
                ],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 6 — Trigonometry Laws
# ---------------------------------------------------------------------------

week6 = week(
    6,
    "Trigonometry Laws",
    "The Law of Sines and the Law of Cosines for non-right triangles; the ambiguous case.",
    [
        src(YS, "Ch 3", "Laws of Sines and Cosines", "3%3A_Laws_of_Sines_and_Cosines"),
        src(OS, "Ch 10", "Further Applications of Trigonometry"),
    ],
    [
        topic(
            "law-of-sines",
            "The Law of Sines",
            "sin A / a = sin B / b = sin C / c. The ambiguous (SSA) case. From Yoshiwara §3.1 and OpenStax §10.1.",
            30,
            [src(YS, "Ch 3.1"), src(OS, "Ch 10.1", "Non-right Triangles: Law of Sines")],
            lesson(
                ["State the Law of Sines.", "Use it to solve AAS, ASA, and SSA triangles.", "Recognize the ambiguous case."],
                "When a triangle isn't right, the Law of Sines and Law of Cosines do the job.",
                [
                    section("Formula", "a/sin A = b/sin B = c/sin C. Any pair gives the third side."),
                    section("When it works", "AAS, ASA, ASA, SSA (with care for the ambiguous case)."),
                    section("Ambiguous case", "SSA: two possible triangles if a < b and a > b sin A. Otherwise 0 or 1."),
                ],
                [
                    example("In ΔABC, A = 30°, B = 45°, a = 10. Find b.",
                            "Use the Law of Sines.",
                            "≈ 14.14",
                            ["b = a · sin B / sin A = 10 · sin 45° / sin 30° = 10 · (√2/2) / (1/2) = 10√2 ≈ 14.14."],
                            src(YS, "Ch 3.1")),
                ],
                [step_by_step(
                    "Solve a triangle: A = 40°, B = 65°, a = 12. Find b, c, C.",
                    "Compute.",
                    [
                        step("Find C", "C = 180° − 40° − 65° = 75°", "Angles of a triangle sum to 180°."),
                        step("Apply Law of Sines for b", "b = 12 · sin 65° / sin 40° ≈ 17.49", "Calculator in degrees."),
                        step("Apply Law of Sines for c", "c = 12 · sin 75° / sin 40° ≈ 18.51", "Same idea.")] ,
                    src(YS, "Ch 3.1"))],
                [
                    video('9fS0uA4iLxI', 'Law of Sines', 'Khan Academy', src('openstax_abramson', 'Ch 10.1'), 480),
                    video('i6kIjZA2UAI', 'Law of Sines — How? When?', 'NancyPi', src('openstax_abramson', 'Ch 10.1'), 600),
                    video('8qezAG2r0sk', 'Law of Sines and Law of Cosines', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 10.1'), 720),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("The Law of Sines says a/sin A equals…", ["b · sin B", "b / sin B", "sin C / c", "Both b / sin B and c / sin C"], "3",
                       "All three ratios are equal.", src(OS, "Ch 10.1")),
                ],
            ),
        ),
        topic(
            "law-of-cosines",
            "The Law of Cosines",
            "c² = a² + b² − 2ab cos C. SSS and SAS triangles. From Yoshiwara §3.2 and OpenStax §10.2.",
            35,
            [src(YS, "Ch 3.2"), src(OS, "Ch 10.2", "Non-right Triangles: Law of Cosines")],
            lesson(
                ["State the Law of Cosines.", "Use it for SSS and SAS triangles."],
                "The Law of Cosines is the Pythagorean theorem with a correction term for non-right angles.",
                [
                    section("Formula", "c² = a² + b² − 2ab cos C (and cyclic permutations)."),
                    section("When to use", "SAS (two sides and the included angle) or SSS (all three sides)."),
                ],
                [
                    example("Sides a = 7, b = 9, included angle C = 60°. Find c.",
                            "Apply the Law of Cosines.",
                            "≈ 8.19",
                            ["c² = 49 + 81 − 2·7·9·cos 60° = 130 − 126·(1/2) = 130 − 63 = 67. c = √67 ≈ 8.19."],
                            src(OS, "Ch 10.2")),
                ],
                [step_by_step(
                    "Triangle with sides 5, 6, 7. Find the largest angle.",
                    "Compute the angle opposite the longest side (7).",
                    [
                        step("Use Law of Cosines", "7² = 5² + 6² − 2·5·6·cos C", "C is the angle opposite the side of length 7."),
                        step("Simplify", "49 = 25 + 36 − 60 cos C → 49 = 61 − 60 cos C", "Compute."),
                        step("Solve for cos C", "60 cos C = 12 → cos C = 1/5", "Subtract 61, divide by 60."),
                        step("Find C", "C = arccos(0.2) ≈ 78.46°", "Inverse cosine."),
                    ],
                    src(OS, "Ch 10.2"))],
                [
                    video('9CGY0s-uCUE', 'Law of Cosines', 'Khan Academy', src('openstax_abramson', 'Ch 10.2'), 480),
                    video('8qezAG2r0sk', 'Law of Sines and Law of Cosines', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 10.1'), 720),
                    video('i6kIjZA2UAI', 'Law of Sines — How? When?', 'NancyPi', src('openstax_abramson', 'Ch 10.1'), 600),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Law of Cosines for c is…", ["c² = a² + b² + 2ab cos C", "c² = a² + b² − 2ab cos C", "c = a + b − 2ab cos C", "c² = a² − b² − 2ab cos C"], "1",
                       "The standard form.", src(OS, "Ch 10.2")),
                    fr("Triangle with sides 8, 11, 13. Find the largest angle to the nearest degree.", "≈ 85°",
                       "Use Law of Cosines with c = 13, a = 8, b = 11: cos C = (64 + 121 − 169)/(2·8·11) = 16/176 ≈ 0.0909, so C ≈ arccos(0.0909) ≈ 84.8° ≈ 85°.",
                       src(OS, "Ch 10.2")),
                ],
            ),
        ),
        topic(
            "area-of-triangle",
            "Area of an Oblique Triangle",
            "Area = ½ ab sin C, Heron's formula. From Yoshiwara §3.3 and OpenStax §10.3.",
            20,
            [src(YS, "Ch 3.3"), src(OS, "Ch 10.3")],
            lesson(
                ["Compute the area of a triangle given two sides and the included angle.", "Apply Heron's formula when you know all three sides."],
                "Two clean area formulas, one for SAS and one for SSS.",
                [
                    section("SAS area", "Area = ½ · a · b · sin C. The '1/2 ab sin C' form."),
                    section("Heron's formula", "Area = √(s(s − a)(s − b)(s − c)), where s = (a + b + c)/2 is the semi-perimeter."),
                ],
                [
                    example("Triangle with sides 6 and 9 and included angle 50°.",
                            "Compute the area.",
                            "≈ 20.7 square units",
                            ["Area = ½ · 6 · 9 · sin 50° = 27 · 0.766 ≈ 20.7."],
                            src(OS, "Ch 10.3")),
                ],
                [],
                [
                    video('T4LAAQ6S_SE', 'Area of a triangle', 'Khan Academy', src('openstax_abramson', 'Ch 10.3'), 420),
                    video('bSM7RNSbWhM', 'Basic Trigonometry: Sin Cos Tan', 'NancyPi', src('yoshiwara', 'Ch 2.1'), 600),
                    video('i6kIjZA2UAI', 'Law of Sines — How? When?', 'NancyPi', src('openstax_abramson', 'Ch 10.1'), 600),
                    video('8qezAG2r0sk', 'Law of Sines and Law of Cosines', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 10.1'), 720),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Area = ½ab sin C uses which information?", ["three sides", "two sides and included angle", "two angles and a side", "the perimeter only"], "1",
                       "SAS, exactly.", src(OS, "Ch 10.3")),
                ],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# Week 7 — Trigonometry Applications
# ---------------------------------------------------------------------------

week7 = week(
    7,
    "Trigonometry Applications",
    "Vectors, the dot product, complex numbers, polar coordinates, parametric equations.",
    [
        src(YS, "Ch 9", "Vectors", "9%3A_Vectors"),
        src(YS, "Ch 10", "Polar Coordinates and Complex Numbers"),
        src(OS, "Ch 10.4", "Vectors"),
        src(OS, "Ch 10.5", "Polar Coordinates"),
        src(OS, "Ch 10.6", "Vectors"),
    ],
    [
        topic(
            "vectors",
            "Vectors in 2D",
            "Magnitude, direction, components, addition, scalar multiplication, the dot product. From Yoshiwara §§9.0–9.2 and OpenStax §§10.4–10.6.",
            40,
            [src(YS, "Ch 9.0–9.2"), src(OS, "Ch 10.4")],
            lesson(
                ["Express a vector in component form.", "Add, subtract, and scale vectors.", "Compute the dot product and use it to find the angle between two vectors."],
                "A vector is a quantity with both magnitude and direction. Precalculus builds the algebra you'll use for forces, velocities, and more.",
                [
                    section("Component form", "v = ⟨a, b⟩. Magnitude |v| = √(a² + b²). Direction angle θ = arctan(b/a) (with care for the quadrant)."),
                    section("Operations", "Add componentwise: ⟨a, b⟩ + ⟨c, d⟩ = ⟨a + c, b + d⟩. Scalar: k⟨a, b⟩ = ⟨ka, kb⟩."),
                    section("Dot product", "u · v = u₁v₁ + u₂v₂. Also u · v = |u| |v| cos θ. Useful for finding the angle between two vectors."),
                ],
                [
                    example("Find the magnitude of v = ⟨3, 4⟩.",
                            "Compute |v|.",
                            "5",
                            ["√(3² + 4²) = √25 = 5."],
                            src(YS, "Ch 9.0")),
                ],
                [step_by_step(
                    "Find the angle between u = ⟨1, 2⟩ and v = ⟨3, −1⟩.",
                    "Use the dot product.",
                    [
                        step("Compute the dot product", "u · v = 1·3 + 2·(−1) = 1", "Multiply and add."),
                        step("Find the magnitudes", "|u| = √(1 + 4) = √5, |v| = √(9 + 1) = √10", "Standard formula."),
                        step("Use u · v = |u||v| cos θ", "1 = √5 · √10 · cos θ = √50 · cos θ = 5√2 · cos θ", "Substitute."),
                        step("Solve for cos θ", "cos θ = 1 / (5√2) = √2 / 10", "Rationalize."),
                        step("Find θ", "θ ≈ 81.87°", "arccos(√2 / 10).")] ,
                    src(YS, "Ch 9.2"))],
                [
                    video('oX2T6KE1u6U', 'Vectors introduction', 'Khan Academy', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('sEPAHVOeicA', 'Dot product and angle', 'Khan Academy', src('yoshiwara', 'Ch 9.2'), 480),
                    video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('k7RM-ot2NWY', 'Linear combinations, span & basis vectors', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
                ],

                [
                    mc("Magnitude of ⟨−3, 4⟩ is…", ["1", "5", "7", "25"], "1",
                       "√(9 + 16) = √25 = 5. (Index 1 = '5'.)", src(YS, "Ch 9.0")),
                    fr("Compute u · v for u = ⟨2, 3⟩, v = ⟨4, −1⟩.", "5", "2·4 + 3·(−1) = 8 − 3 = 5.", src(YS, "Ch 9.2")),
                ],
            ),
        ),
        topic(
            "complex-numbers",
            "Complex Numbers & Polar Form",
            "a + bi, modulus, argument, polar multiplication and De Moivre's theorem. From Yoshiwara §§10.2–10.4 and OpenStax §2.4.",
            35,
            [src(YS, "Ch 10.2–10.4"), src(OS, "Ch 2.4", "Complex Numbers")],
            lesson(
                ["Convert between rectangular and polar form.", "Multiply and divide complex numbers in polar form.", "Apply De Moivre's theorem to find powers and roots."],
                "Complex numbers are a + bi with i² = −1. Polar form exposes their geometric meaning.",
                [
                    section("Rectangular to polar", "r = √(a² + b²). θ = atan2(b, a). Polar form: r (cos θ + i sin θ)."),
                    section("Polar multiplication", "r₁(cos θ₁ + i sin θ₁) · r₂(cos θ₂ + i sin θ₂) = r₁r₂ (cos(θ₁ + θ₂) + i sin(θ₁ + θ₂))."),
                    section("De Moivre", "(cos θ + i sin θ)ⁿ = cos(nθ) + i sin(nθ)."),
                ],
                [
                    example("Convert 1 + i to polar form.",
                            "Find r and θ.",
                            "√2 (cos(π/4) + i sin(π/4))",
                            ["r = √(1² + 1²) = √2. θ = π/4 (since both coordinates are equal and positive)."],
                            src(OS, "Ch 2.4")),
                ],
                [step_by_step(
                    "Compute (1 + i)² using De Moivre.",
                    "Find the value.",
                    [
                        step("Polar form of 1 + i", "√2 (cos(π/4) + i sin(π/4))", "r = √2, θ = π/4."),
                        step("Square using De Moivre", "(√2)² (cos(π/2) + i sin(π/2)) = 2(0 + i·1) = 2i", "n = 2, so angle doubles and modulus squares."),
                        step("Verify", "(1 + i)² = 1 + 2i + i² = 1 + 2i − 1 = 2i", "By direct expansion too.")] ,
                    src(OS, "Ch 2.4"))],
                [
                    video('TjYH0Fz5RMc', 'Complex numbers in polar form', 'Khan Academy', src('openstax_abramson', 'Ch 2.4'), 600),
                    video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('8qezAG2r0sk', 'Factoring Polynomials and Solving by Factoring', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 2.1'), 720),
                    video('GmMX3-nTWbE', 'Solving Linear Equations Made Easy', 'PatrickJMT', src('openstax_abramson', 'Ch 1.1'), 600),
                    video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
                ],

                [
                    mc("Polar form of 1 + i√3 has θ = ?", ["π/6", "π/3", "π/4", "π/2"], "1",
                       "tan θ = √3, in Q I → θ = π/3. (Index 1 = 'π/3'.)", src(OS, "Ch 2.4")),
                ],
            ),
        ),
        topic(
            "polar-coordinates",
            "Polar Coordinates",
            "Plot and convert, sketch polar curves, find area. From Yoshiwara §§10.0–10.1 and OpenStax §10.5.",
            30,
            [src(YS, "Ch 10.0–10.1"), src(OS, "Ch 10.5")],
            lesson(
                ["Convert between polar and rectangular coordinates.", "Sketch basic polar curves (lines, circles, roses, cardioids).", "Find the area enclosed by a polar curve."],
                "Polar coordinates (r, θ) describe a point by its distance from the origin and its angle from the positive x-axis.",
                [
                    section("Conversion", "x = r cos θ, y = r sin θ. r² = x² + y². tan θ = y/x (with quadrant)."),
                    section("Polar curves", "r = a (circle), r = a sin θ or a cos θ (circle through origin), r = a(1 ± cos θ) (cardioid), r = a sin(nθ) (rose)."),
                ],
                [
                    example("Convert (2, π/3) to rectangular coordinates.",
                            "Find (x, y).",
                            "(1, √3)",
                            ["x = 2 cos(π/3) = 2·(1/2) = 1.", "y = 2 sin(π/3) = 2·(√3/2) = √3."],
                            src(OS, "Ch 10.5")),
                ],
                [step_by_step(
                    "Convert the rectangular point (3, 4) to polar form.",
                    "Find r and θ.",
                    [
                        step("Compute r", "r = √(3² + 4²) = 5", "Distance from origin."),
                        step("Compute θ", "tan θ = 4/3, in Q I → θ = arctan(4/3) ≈ 53.13°", "Both coordinates positive, so Q I."),
                        step("Polar form", "(5, 53.13°) or (5, 0.9273 rad)", "Two equivalent notations.")] ,
                    src(OS, "Ch 10.5"))],
                [
                    video('J9LmF2NLweY', 'Polar coordinates', 'Khan Academy', src('openstax_abramson', 'Ch 10.5'), 540),
                    video('97pe-QlSGqA', 'Parametric Equations Introduction', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 10.4'), 720),
                    video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                ],

                [
                    mc("In polar coordinates, the equation r = 4 is a…", ["line", "circle of radius 4", "point", "ray"], "1",
                       "All points exactly 4 units from the origin — a circle.", src(OS, "Ch 10.5")),
                ],
            ),
        ),
        topic(
            "parametric-equations",
            "Parametric Equations",
            "Eliminate the parameter, graph a parametric curve. From OpenStax §10.4 (parametric section) and Khan Academy.",
            20,
            [src(OS, "Ch 10.4")],
            lesson(
                ["Plot a curve given by x = f(t), y = g(t).", "Eliminate the parameter to get a Cartesian equation."],
                "Parametric equations let x and y be separate functions of a third variable t.",
                [
                    section("Eliminating t", "Solve one equation for t and substitute into the other. For trig pairs, use Pythagorean identities."),
                    section("Orientation", "Increasing t traces the curve in a specific direction (the orientation)."),
                ],
                [
                    example("Eliminate the parameter from x = cos t, y = sin t.",
                            "Find the Cartesian equation.",
                            "x² + y² = 1",
                            ["cos²t + sin²t = 1 → x² + y² = 1. The unit circle, traced counterclockwise as t increases."],
                            src(OS, "Ch 10.4")),
                ],
                [step_by_step(
                    "Eliminate the parameter from x = t + 1, y = t².",
                    "Find y in terms of x.",
                    [
                        step("Solve for t", "t = x − 1", "From the first equation."),
                        step("Substitute", "y = (x − 1)²", "Replace t in y = t².")] ,
                    src(OS, "Ch 10.4"))],
                [
                    video('f3QtV2TTxk', 'Parametric equations intro', 'Khan Academy', src('openstax_abramson', 'Ch 10.4'), 480),
                    video('97pe-QlSGqA', 'Parametric Equations Introduction', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 10.4'), 720),
                    video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
                    video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
                    video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
                ],

                [
                    mc("x = cos t, y = sin t is the parametric form of…", ["a line", "a parabola", "the unit circle", "a hyperbola"], "2",
                       "Eliminate t with cos² + sin² = 1.", src(OS, "Ch 10.4")),
                ],
            ),
        ),
    ],
)


# ---------------------------------------------------------------------------
# New topics (expand the knowledge base)
# ---------------------------------------------------------------------------

# Conic sections — adds Week 2/3 material to round out the "graphing" topic
# mentioned in the original course outline. Source: OpenStax Ch 12.
conic_sections = topic(
    "conic-sections",
    "Conic Sections: Circles, Ellipses, Parabolas, Hyperbolas",
    "Identify and graph the four conic sections by their algebraic form. Master the standard equations, foci, vertices, and eccentricity. From OpenStax §§12.1–12.4.",
    60,
    [src(OS, "Ch 12.1–12.4", "Analytic Geometry")],
    lesson(
        ["Classify a conic by its algebraic form.", "Write the standard form of each conic.", "Use eccentricity to identify the conic."],
        "A conic section is the curve formed by intersecting a plane with a double cone. Four types: circle, ellipse, parabola, hyperbola.",
        [
            section("Circles", "A circle is the set of points equidistant from a center. Standard: (x − h)² + (y − k)² = r²."),
            section("Ellipses", "An ellipse is the set of points where the sum of distances to two foci is constant. Standard: x²/a² + y²/b² = 1. Eccentricity 0 < e < 1."),
            section("Parabolas", "A parabola is the set of points equidistant from a focus and a directrix. Standard: y = ax². Eccentricity e = 1."),
            section("Hyperbolas", "A hyperbola is the set of points where the absolute difference of distances to two foci is constant. Standard: x²/a² − y²/b² = 1. Eccentricity e > 1."),
            section("Eccentricity", "Eccentricity e is the unifying measure. e = 0: circle. 0 < e < 1: ellipse. e = 1: parabola. e > 1: hyperbola."),
        ],
        [
            example("Identify the conic x² + y² = 25.",
                    "State the type and key features.",
                    "Circle, center (0,0), radius 5",
                    ["Both x² and y² have equal positive coefficients → circle.", "Rewrite: x² + y² = 5².", "Center (0, 0), radius 5."],
                    src(OS, "Ch 12.1")),
            example("Identify the conic x²/9 + y²/4 = 1.",
                    "State the type and key features.",
                    "Ellipse, a = 3, b = 2",
                    ["Both x² and y² have positive coefficients → ellipse. Larger is a (semi-major).", "x²/9 + y²/4 = 1 → a = 3, b = 2."],
                    src(OS, "Ch 12.2")),
            example("Identify the conic y² = 8x.",
                    "State the type and key features.",
                    "Parabola opening right, focus at (2, 0)",
                    ["One variable squared, the other linear → parabola.", "y² = 4px with 4p = 8 → p = 2, so focus at (2, 0)."],
                    src(OS, "Ch 12.3")),
        ],
        [step_by_step(
            "Identify the conic and write it in standard form: 4x² + 9y² = 36.",
            "Classify and convert.",
            [
                step("Identify coefficients", "Both x² and y² have positive coefficients (4 and 9) → ellipse.", "Equal signs, different coefficients → ellipse."),
                step("Divide by RHS", "x²/9 + y²/4 = 1", "Divide both sides by 36."),
                step("Identify a, b", "a² = 9, b² = 4 → a = 3, b = 2", "Standard form: x²/a² + y²/b² = 1."),
                step("Identify features", "Major axis along x-axis (a > b). Vertices at (±3, 0). Co-vertices at (0, ±2).", "Major axis along the axis of the larger a."),
            ],
            src(OS, "Ch 12.2"))],
        [
            video('Dru6Fs9Acz4', 'Conic sections overview', 'Khan Academy', src('openstax_abramson', 'Ch 12.1'), 540),
            video('XO8i8AjhcL8', 'Conic sections — circles, ellipses, hyperbolas', 'Khan Academy', src('openstax_abramson', 'Ch 12.2'), 600),
            video('Q8BbbZxkZSA', 'Rational Functions and Conic Sections', 'Organic Chemistry Tutor', src('openstax_abramson', 'Ch 12.1'), 720),
            video('fNk_zzaMoSs', 'Vectors — Essence of Linear Algebra Ch 1', '3Blue1Brown', src('openstax_abramson', 'Ch 10.4'), 600),
            video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
            video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
        ],

        PQ.CONIC_SECTIONS_QUESTIONS,
    ),
)

# Sequences and series — OpenStax Ch 13
sequences_and_series = topic(
    "sequences-and-series",
    "Sequences and Series",
    "Arithmetic and geometric sequences, partial sums, and an introduction to the Fibonacci sequence. From OpenStax §§13.1–13.3.",
    45,
    [src(OS, "Ch 13.1–13.3", "Sequences, Probability, and Counting Theory")],
    lesson(
        ["Identify arithmetic vs. geometric sequences.", "Use formulas for the nth term and partial sum.", "Recognize when a series converges."],
        "A sequence is an ordered list of numbers; a series is their sum. Two fundamental families: arithmetic (constant difference) and geometric (constant ratio).",
        [
            section("Arithmetic sequences", "a_n = a₁ + (n−1)d, where d is the common difference."),
            section("Geometric sequences", "a_n = a₁ · r^(n−1), where r is the common ratio."),
            section("Arithmetic series", "S_n = n/2 · (a₁ + a_n) = n/2 · (2a₁ + (n−1)d)."),
            section("Geometric series", "S_n = a₁ · (1 − r^n)/(1 − r). For |r| < 1, infinite sum S = a₁/(1 − r)."),
            section("Special sequences", "Fibonacci: each term is the sum of the two previous. Arithmetic and geometric are the main families you will see."),
        ],
        [
            example("Find a_8 of the arithmetic sequence with a_1 = 3, d = 4.",
                    "Compute a_8.",
                    "31",
                    ["a_n = a₁ + (n−1)d = 3 + 7·4 = 3 + 28 = 31."],
                    src(OS, "Ch 13.1")),
            example("Find S_5 of the geometric series 1 + 2 + 4 + 8 + 16.",
                    "Compute the partial sum.",
                    "31",
                    ["S_n = a₁(1 − r^n)/(1 − r) = 1·(1 − 2^5)/(1 − 2) = (−31)/(−1) = 31."],
                    src(OS, "Ch 13.2")),
        ],
        [step_by_step(
            "Find the sum of the first 12 terms of 5, 8, 11, 14, ...",
            "Identify the series and use the formula.",
            [
                step("Identify d", "8 − 5 = 3, so d = 3 (arithmetic).", "Constant difference → arithmetic."),
                step("Find a_12", "a_12 = 5 + 11·3 = 5 + 33 = 38.", "a_n = a₁ + (n−1)d."),
                step("Apply sum formula", "S_12 = 12/2 · (5 + 38) = 6 · 43 = 258.", "S_n = n/2 · (a₁ + a_n)."),
            ],
            src(OS, "Ch 13.1"))],
        [
            video('cIEoP-IVNyk', 'Arithmetic sequences', 'Khan Academy', src('openstax_abramson', 'Ch 13.1'), 600),
            video('D1Q3RquaO-4', 'D1Q3RquaO-4', 'Khan Academy', src('openstax_abramson', 'Ch 1'), 540),
            video('9SOQS5jb4f4', 'Precalculus in One Day', 'Brian McLogan', src('openstax_abramson', 'Ch 3'), 600),
            video('FkUEsP9efFg', 'Introduction to Functions', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.1'), 720),
            video('sCRB6hMsC4', 'Introduction to Graph Transformations', 'Professor Leonard', src('lippman_rasmussen', 'Ch 1.5'), 720),
            video('TreVSyf3THY', 'Trigonometry Basics — SOHCAHTOA', "Mario's Math Tutoring", src('yoshiwara', 'Ch 2.1'), 540),
        ],

        PQ.SEQUENCES_QUESTIONS,
    ),
)


# ---------------------------------------------------------------------------
# Write out
# ---------------------------------------------------------------------------


def main():
    with COURSE.open() as f:
        course = json.load(f)

    weeks = [week1, week2, week3, week4, week5, week6, week7]

    # Add the new "Expand your reach" topics to Week 7 (advanced applications)
    week7["topics"] = week7["topics"] + [conic_sections, sequences_and_series]

    # Apply the practice-question expansion: each topic with an entry in
    # PRACTICE_BY_SLUG gets its 10-question bank (with 3 hints each).
    for week in weeks:
        week["topics"] = [with_expanded_practice(t) for t in week["topics"]]
    # Also expand prerequisites
    if course.get("prerequisites"):
        course["prerequisites"] = [with_expanded_practice(t) for t in course["prerequisites"]]

    course["weeks"] = weeks
    with COURSE.open("w") as f:
        json.dump(course, f, indent=2)

    total_topics = sum(len(w["topics"]) for w in course["weeks"]) + len(course.get("prerequisites", []))
    total_practice = sum(len(t["lesson"].get("practice", []))
                         for w in course["weeks"] for t in w["topics"])
    total_practice += sum(len(t["lesson"].get("practice", []))
                          for t in course.get("prerequisites", []))
    total_hints = sum(len(q.get("hints", []))
                      for w in course["weeks"] for t in w["topics"]
                      for q in t["lesson"].get("practice", []))
    total_hints += sum(len(q.get("hints", []))
                       for t in course.get("prerequisites", [])
                       for q in t["lesson"].get("practice", []))
    print(f"Wrote {COURSE}")
    print(f"  {len(course['weeks'])} weeks, {total_topics} topics total")
    print(f"  {total_practice} practice questions, {total_hints} hints total")


if __name__ == "__main__":
    main()
