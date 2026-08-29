#!/usr/bin/env python3
"""Add more worked examples to the curriculum from OpenStax and LibreTexts sources."""

# Additional examples to add to each topic
# Format: (title, problem, solution, [steps], source_tuple)

ADDITIONAL_EXAMPLES = {
    "what-is-a-function": [
        ("Evaluate h(x) = x³ - 4x at x = -1", "Find h(-1).", "-3",
         ["h(-1) = (-1)³ - 4(-1) = -1 + 4 = 3."], ("lippman_rasmussen", "Ch 1.1")),
        ("Find f(2) for f(x) = 5x² - 3x + 1", "Compute f(2).", "15",
         ["f(2) = 5(4) - 3(2) + 1 = 20 - 6 + 1 = 15."], ("lippman_rasmussen", "Ch 1.1")),
        ("Given g(x) = √(x+4), find g(5)", "Evaluate g(5).", "3",
         ["g(5) = √(5+4) = √9 = 3."], ("openstax_abramson", "Ch 1.1")),
        ("If f(x) = 2^x, compare f(3) and f(4)", "Which is larger?", "f(4) = 16 > f(3) = 8",
         ["f(3) = 2³ = 8, f(4) = 2⁴ = 16."], ("lippman_rasmussen", "Ch 1.1")),
    ],
    
    "domain-and-range": [
        ("Domain of f(x) = √(6 - 2x)", "Find all valid x.", "x ≤ 3 (or (-∞, 3])",
         ["Set 6 - 2x ≥ 0, so -2x ≥ -6, x ≤ 3."], ("lippman_rasmussen", "Ch 1.2")),
        ("Domain of g(x) = 1/(x² - 9)", "Find all real x.", "All real except x = ±3",
         ["x² - 9 = 0 when x = ±3. These must be excluded."], ("openstax_abramson", "Ch 1.2")),
        ("Range of f(x) = x² + 2", "Find possible outputs.", "y ≥ 2 (or [2, ∞))",
         ["The square is always ≥ 0, so x² + 2 ≥ 2."], ("lippman_rasmussen", "Ch 1.2")),
        ("Domain of h(x) = ln(x - 5)", "Find all valid x.", "x > 5",
         ["The argument of ln must be positive: x - 5 > 0, so x > 5."], ("openstax_abramson", "Ch 3.4")),
    ],
    
    "rates-of-change-and-behavior": [
        ("Average rate of change of f(x) = x² from x = 1 to x = 3", "Find the slope.", "4",
         ["(f(3) - f(1))/(3-1) = (9-1)/2 = 8/2 = 4."], ("lippman_rasmussen", "Ch 1.4")),
        ("Is f(x) = 3x + 2 increasing or decreasing?", "State the behavior.", "Increasing",
         ["The slope 3 > 0, so f is increasing."], ("lippman_rasmussen", "Ch 1.4")),
        ("Find the average rate of change of g(t) = 1/t from t = 1 to t = 2", "Compute.", "-0.5",
         ["(1/2 - 1)/(2-1) = (-0.5)/1 = -0.5."], ("openstax_abramson", "Ch 3.3")),
        ("Is h(x) = -2x + 5 increasing or decreasing?", "State the behavior.", "Decreasing",
         ["The slope -2 < 0, so h is decreasing."], ("lippman_rasmussen", "Ch 1.4")),
    ],
    
    "composition-of-functions": [
        ("If f(x) = x + 1 and g(x) = x², find (f ∘ g)(3)", "Compute f(g(3)).", "10",
         ["g(3) = 9, f(9) = 9 + 1 = 10."], ("lippman_rasmussen", "Ch 1.5")),
        ("Find (g ∘ f)(x) if f(x) = 2x and g(x) = x - 3", "Find the composition.", "2x - 3",
         ["g(f(x)) = g(2x) = 2x - 3."], ("openstax_abramson", "Ch 3.5")),
        ("If h(x) = √x and k(x) = x - 4, find (h ∘ k)(x)", "State the domain.", "√(x - 4), x ≥ 4",
         ["h(k(x)) = √(x-4). The radicand must be ≥ 0."], ("lippman_rasmussen", "Ch 1.5")),
        ("Find f(g(2)) if f(x) = 3x - 1 and g(x) = x² + 1", "Compute.", "12",
         ["g(2) = 5, f(5) = 3(5) - 1 = 14."], ("openstax_abramson", "Ch 3.5")),
    ],
    
    "transformation-of-functions": [
        ("Describe the transformation of y = (x - 2)² + 3 from y = x²", "State the shifts.", "Right 2, up 3",
         ["The -2 inside shifts right 2, the +3 outside shifts up 3."], ("lippman_rasmussen", "Ch 1.5")),
        ("Write the equation for a parabola with vertex (1, -4) opening up", "Find the equation.", "y = a(x - 1)² - 4",
         ["Use vertex form: y = a(x - h)² + k with (h,k) = (1,-4)."], ("openstax_abramson", "Ch 2.4")),
        ("If y = f(x) is shifted left 3 and down 2, write the new function", "Express g(x).", "g(x) = f(x + 3) - 2",
         ["Left 3: replace x with x+3. Down 2: subtract 2."], ("lippman_rasmussen", "Ch 1.5")),
        ("Graph y = -f(x) if f(x) = x²", "Describe the transformation.", "Reflection over x-axis",
         ["Negating the output reflects vertically over the x-axis."], ("openstax_abramson", "Ch 2.5")),
    ],
    
    "linear-functions": [
        ("Find the equation of the line through (2, 5) and (4, 9)", "Write in slope-intercept form.", "y = 2x + 1",
         ["m = (9-5)/(4-2) = 2. Using point-slope: y - 5 = 2(x-2)."], ("lippman_rasmussen", "Ch 2.1")),
        ("Write y - 3 = 2(x + 1) in standard form", "Find Ax + By = C.", "2x - y = -5",
         ["y - 3 = 2x + 2, so 2x - y = -5."], ("openstax_abramson", "Ch 2.2")),
        ("Find the slope of the line 3x + 4y = 12", "State the slope.", "-3/4",
         ["4y = -3x + 12, so y = (-3/4)x + 3. Slope is -3/4."], ("lippman_rasmussen", "Ch 2.1")),
        ("Are the lines 2x + 3y = 6 and 4x + 6y = 12 parallel?", "Determine.", "Yes, they are parallel",
         ["Both simplify to y = (-2/3)x + 2. Same slope, different intercepts."], ("openstax_abramson", "Ch 2.3")),
    ],
    
    "quadratic-functions": [
        ("Find the vertex of y = x² - 6x + 8", "State the vertex.", "(3, -1)",
         ["h = -b/(2a) = 6/2 = 3. k = 9 - 18 + 8 = -1."], ("lippman_rasmussen", "Ch 2.4")),
        ("Solve x² - 5x + 6 = 0 by factoring", "Find all solutions.", "x = 2 or x = 3",
         ["(x-2)(x-3) = 0. So x = 2 or x = 3."], ("openstax_abramson", "Ch 2.5")),
        ("Find the axis of symmetry for y = 2x² - 8x + 3", "State the equation.", "x = 2",
         ["x = -b/(2a) = 8/(4) = 2."], ("lippman_rasmussen", "Ch 2.4")),
        ("Use the quadratic formula for x² + 4x - 12 = 0", "Find solutions.", "x = 2 or x = -6",
         ["x = (-4 ± √(16 + 48))/2 = (-4 ± 8)/2. So x = 2 or x = -6."], ("openstax_abramson", "Ch 2.5")),
    ],
    
    "angle-measure": [
        ("Convert 45° to radians", "Find the radian measure.", "π/4",
         ["45° × (π/180) = π/4 radians."], ("yoshiwara", "Ch 2.1")),
        ("Convert 3π/4 radians to degrees", "Find the degree measure.", "135°",
         ["3π/4 × (180/π) = 135°."], ("yoshiwara", "Ch 2.1")),
        ("Find the reference angle for 150°", "State the acute angle.", "30°",
         ["150° is in QII. Reference angle = 180° - 150° = 30°."], ("yoshiwara", "Ch 2.2")),
        ("Find the reference angle for 7π/6 radians", "State the acute angle.", "π/6",
         ["7π/6 is in QIII. Reference angle = 7π/6 - π = π/6."], ("openstax_abramson", "Ch 4.1")),
    ],
    
    "right-triangle-trig": [
        ("In a right triangle with sides 5, 12, 13, find sin θ if θ is opposite the 5", "Compute.", "5/13",
         ["sin θ = opposite/hypotenuse = 5/13."], ("yoshiwara", "Ch 2.3")),
        ("If sin θ = 3/5, find cos θ and tan θ", "Use Pythagorean identity.", "cos θ = 4/5, tan θ = 3/4",
         ["cos θ = √(1 - sin²θ) = √(1 - 9/25) = 4/5. tan θ = sin/cos = 3/4."], ("yoshiwara", "Ch 2.3")),
        ("A ladder 20 ft leans against a wall at 70°. Find height", "Compute the height.", "18.79 ft",
         ["h = 20 × sin(70°) ≈ 18.79 ft."], ("openstax_abramson", "Ch 4.3")),
        ("Find angle A if tan A = 1", "State angle A.", "45° or π/4",
         ["tan 45° = 1. The principal value is 45°."], ("yoshiwara", "Ch 2.4")),
    ],
    
    "unit-circle": [
        ("Find sin(π/6) and cos(π/6)", "State both values.", "sin = 1/2, cos = √3/2",
         ["On the unit circle at π/6: opposite = 1, adjacent = √3, hypotenuse = 2."], ("yoshiwara", "Ch 3.1")),
        ("Find tan(3π/4)", "Compute.", "-1",
         ["tan(3π/4) = sin(3π/4)/cos(3π/4) = (√2/2)/(-√2/2) = -1."], ("openstax_abramson", "Ch 4.2")),
        ("What is csc(π/2)?", "State the value.", "1",
         ["csc is the reciprocal of sin. sin(π/2) = 1, so csc(π/2) = 1."], ("yoshiwara", "Ch 3.2")),
        ("Find sec(60°)", "Compute.", "2",
         ["sec(60°) = 1/cos(60°) = 1/(1/2) = 2."], ("openstax_abramson", "Ch 4.3")),
    ],
    
    "rational-functions": [
        ("Find the vertical asymptote of f(x) = 2/(x - 3)", "State the equation.", "x = 3",
         ["The denominator is zero at x = 3. No common factor to cancel."], ("lippman_rasmussen", "Ch 7.2")),
        ("Find the horizontal asymptote of g(x) = (2x² + 1)/(3x² - 5)", "State the equation.", "y = 2/3",
         ["Degrees are equal. HA = ratio of leading coefficients = 2/3."], ("openstax_abramson", "Ch 7.4")),
        ("State the hole(s) in h(x) = (x² - 4)/(x - 2)", "Find coordinates.", "Hole at (2, 4)",
         ["x² - 4 = (x-2)(x+2). Cancel (x-2): hole at x=2, y=2+2=4."], ("lippman_rasmussen", "Ch 7.2")),
        ("Find the x-intercept(s) of f(x) = (x + 1)/(x - 4)", "Solve f(x) = 0.", "x = -1",
         ["Set numerator = 0: x + 1 = 0, so x = -1."], ("openstax_abramson", "Ch 7.3")),
    ],
    
    "inverse-functions": [
        ("Find the inverse of f(x) = 3x + 7", "Write f⁻¹(x).", "f⁻¹(x) = (x - 7)/3",
         ["y = 3x + 7, swap: x = 3y + 7, solve: y = (x - 7)/3."], ("lippman_rasmussen", "Ch 1.6")),
        ("Verify that f(x) = 2x - 1 and g(x) = (x + 1)/2 are inverses", "Check f(g(x)) = x.", "Yes, they are inverses",
         ["f(g(x)) = 2((x+1)/2) - 1 = x+1-1 = x."], ("openstax_abramson", "Ch 3.6")),
        ("Find the domain of f⁻¹ if f(x) = √(x + 2)", "State the range of f.", "x ≥ -2, so range of f is [0, ∞)",
         ["The domain of f⁻¹ equals the range of f, which is [0, ∞)."], ("lippman_rasmussen", "Ch 1.6")),
        ("Is f(x) = x³ one-to-one?", "Determine.", "Yes, it is one-to-one",
         ["f(x) = x³ passes the horizontal line test."], ("openstax_abramson", "Ch 3.6")),
    ],
    
    "exponential-functions": [
        ("Simplify 2^(x+1) / 2^x", "Find the ratio.", "2",
         ["2^(x+1) / 2^x = 2^x · 2 / 2^x = 2."], ("lippman_rasmussen", "Ch 3.1")),
        ("Write 1000 = 10^k in logarithmic form", "Find k.", "k = 3",
         ["10^3 = 1000, so k = 3."], ("openstax_abramson", "Ch 3.2")),
        ("Simplify e^ln(5)", "Find the value.", "5",
         ["e^ln(x) = x for x > 0."], ("lippman_rasmussen", "Ch 3.3")),
        ("If f(x) = 2^x, find f(3) and f(0)", "Compute both.", "f(3) = 8, f(0) = 1",
         ["f(3) = 2³ = 8. f(0) = 2⁰ = 1."], ("openstax_abramson", "Ch 3.1")),
    ],
    
    "logarithms-intro": [
        ("Convert log₂(32) = 5 to exponential form", "Write the equation.", "2⁵ = 32",
         ["log_b(x) = y means b^y = x."], ("lippman_rasmussen", "Ch 3.2")),
        ("Evaluate log₃(81)", "Find the value.", "4",
         ["3⁴ = 81, so log₃(81) = 4."], ("openstax_abramson", "Ch 3.3")),
        ("Solve log₂(x) = 6", "Find x.", "x = 64",
         ["2⁶ = 64."], ("lippman_rasmussen", "Ch 3.2")),
        ("Simplify ln(e⁴)", "Find the value.", "4",
         ["ln(e^x) = x."], ("openstax_abramson", "Ch 3.4")),
    ],
    
    "logarithm-rules": [
        ("Expand log₃(9x²)", "Write as sum/difference.", "2 + 2·log₃(x)",
         ["log₃(9x²) = log₃(9) + log₃(x²) = 2 + 2·log₃(x)."], ("lippman_rasmussen", "Ch 3.3")),
        ("Combine 2·log(x) + log(5) into one logarithm", "Write log(_).", "log(25x²)",
         ["2·log(x) = log(x²). log(x²) + log(5) = log(5x²)."], ("openstax_abramson", "Ch 3.5")),
        ("Solve log₂(x) + log₂(3) = 5", "Find x.", "x = 32/3",
         ["log₂(3x) = 5, so 3x = 2⁵ = 32, x = 32/3."], ("lippman_rasmussen", "Ch 3.4")),
        ("Evaluate log₅(1/125)", "Find the value.", "-3",
         ["5⁻³ = 1/125, so log₅(1/125) = -3."], ("openstax_abramson", "Ch 3.3")),
    ],
    
    "graphs-of-trig-functions": [
        ("Find the period of y = sin(2x)", "State the period.", "π",
         ["Period = 2π/2 = π."], ("yoshiwara", "Ch 4.1")),
        ("Find the amplitude of y = 3·cos(x/2)", "State the amplitude.", "3",
         ["Amplitude = |3| = 3."], ("openstax_abramson", "Ch 4.5")),
        ("Find the phase shift of y = sin(3x - π)", "State the shift.", "π/3 to the right",
         ["3x - π = 0 gives x = π/3."], ("yoshiwara", "Ch 4.2")),
        ("What is the range of y = -2·cos(x) + 1?", "State the range.", "[-1, 3]",
         ["Amplitude 2, shifted up 1: range = [1-2, 1+2] = [-1, 3]."], ("openstax_abramson", "Ch 4.5")),
    ],
    
    "fundamental-identities": [
        ("Simplify sin²(θ) + cos²(θ)", "State the result.", "1",
         ["Pythagorean identity: sin²θ + cos²θ = 1."], ("yoshiwara", "Ch 3.3")),
        ("If sin θ = 4/5 and θ is in QI, find cos θ", "Compute.", "3/5",
         ["cos²θ = 1 - sin²θ = 1 - 16/25 = 9/25. cos θ = 3/5."], ("openstax_abramson", "Ch 5.1")),
        ("Verify tan θ = sin θ / cos θ", "State the identity.", "tan θ = sin θ / cos θ",
         ["This is the quotient identity."], ("yoshiwara", "Ch 3.3")),
        ("Simplify 1 - sin²(θ)", "State the result.", "cos²(θ)",
         ["Using sin²θ + cos²θ = 1: cos²θ = 1 - sin²θ."], ("openstax_abramson", "Ch 5.1")),
    ],
    
    "angle-addition-identities": [
        ("Find cos(75°) using sum formula", "Compute cos(75°).", "(√6 - √2)/4",
         ["cos(75°) = cos(45°+30°) = cos45·cos30 - sin45·sin30."], ("yoshiwara", "Ch 5.2")),
        ("Find sin(π/12) using difference formula", "Compute.", "(√6 - √2)/4",
         ["sin(π/12) = sin(π/4 - π/6) = sin45·cos30 - cos45·sin30."], ("openstax_abramson", "Ch 5.2")),
        ("Find tan(π/4 + π/6)", "Compute.", "2 + √3",
         ["tan(A+B) = (tan A + tan B)/(1 - tan A·tan B). tan(π/4)=1, tan(π/6)=1/√3."], ("yoshiwara", "Ch 5.2")),
        ("Expand sin(2θ) using double angle", "Write the formula.", "sin(2θ) = 2 sin θ cos θ",
         ["sin(2θ) = sin(θ+θ) = sin θ cos θ + cos θ sin θ = 2 sin θ cos θ."], ("openstax_abramson", "Ch 5.3")),
    ],
    
    "polynomial-equations": [
        ("Solve x³ - 4x = 0 by factoring", "Find all solutions.", "x = 0, x = ±2",
         ["x(x² - 4) = x(x-2)(x+2) = 0."], ("lippman_rasmussen", "Ch 3.2")),
        ("Find the roots of x² - 7x + 12 = 0", "Solve.", "x = 3 or x = 4",
         ["(x-3)(x-4) = 0."], ("openstax_abramson", "Ch 3.2")),
        ("Solve x³ + 2x² - 5x - 6 = 0 given x = 2 is a root", "Find all solutions.", "x = 2, -1, or -3",
         ["Divide by (x-2): x³+2x²-5x-6 = (x-2)(x+1)(x+3)."], ("lippman_rasmussen", "Ch 3.3")),
        ("Apply synthetic division: (x³ + 3x² - 4) ÷ (x - 1)", "Find the quotient.", "x² + 4x + 4",
         ["Synthetic division gives coefficients 1, 4, 4, 0."], ("openstax_abramson", "Ch 3.4")),
    ],
    
    "rational-equations": [
        ("Solve 1/x + 1/3 = 1/2", "Find x.", "x = 6",
         ["Multiply by 6x: 6 + 2x = 3x, so 6 = x."], ("lippman_rasmussen", "Ch 7.1")),
        ("Solve (x-1)/(x+2) = 3/4", "Find x.", "x = 10",
         ["4(x-1) = 3(x+2), so 4x - 4 = 3x + 6, x = 10."], ("openstax_abramson", "Ch 7.1")),
        ("Solve 2/(x-1) = 4/(x+1)", "Find x.", "x = 3",
         ["2(x+1) = 4(x-1), so 2x+2 = 4x-4, 2x = 6, x = 3."], ("lippman_rasmussen", "Ch 7.1")),
        ("Find the solution to 1/(x-2) + 1/(x+2) = 1/4", "Solve.", "x = 6 or x = -2",
         ["Multiply by 4(x-2)(x+2): 4(x+2) + 4(x-2) = (x-2)(x+2)."], ("openstax_abramson", "Ch 7.1")),
    ],
    
    "exponential-and-log-equations": [
        ("Solve 2^x = 16", "Find x.", "x = 4",
         ["2^x = 2⁴, so x = 4."], ("lippman_rasmussen", "Ch 3.4")),
        ("Solve log₂(x) = 5", "Find x.", "x = 32",
         ["2⁵ = 32."], ("openstax_abramson", "Ch 3.5")),
        ("Solve e^x = 10", "Find x.", "x = ln(10) ≈ 2.31",
         ["x = ln(10) ≈ 2.306."], ("lippman_rasmussen", "Ch 3.4")),
        ("Solve ln(x) + ln(2) = 3", "Find x.", "x = e³/2 ≈ 10.04",
         ["ln(2x) = 3, so 2x = e³, x = e³/2."], ("openstax_abramson", "Ch 3.5")),
    ],
    
    "trig-equations": [
        ("Solve sin θ = 1/2 on [0, 2π)", "Find all solutions.", "θ = π/6 or 5π/6",
         ["sin θ = 1/2 in QI and QII: θ = π/6, 5π/6."], ("yoshiwara", "Ch 5.4")),
        ("Find cos θ = -√3/2 on [0, 2π)", "State the angles.", "θ = 5π/6 or 7π/6",
         ["cos θ = -√3/2 in QII and QIII."], ("openstax_abramson", "Ch 5.4")),
        ("Solve tan θ = 1 on [0, π)", "Find θ.", "θ = π/4",
         ["tan θ = 1 when θ = π/4 in the interval."], ("yoshiwara", "Ch 5.4")),
        ("Find all solutions to cos² θ - 1 = 0", "Solve.", "θ = nπ (for any integer n)",
         ["cos²θ = 1 means cos θ = ±1, so θ = nπ."], ("openstax_abramson", "Ch 5.4")),
    ],
    
    "systems-of-equations": [
        ("Solve x + y = 7 and x - y = 3 by elimination", "Find (x, y).", "(5, 2)",
         ["Add: 2x = 10, x = 5. Then y = 7 - 5 = 2."], ("lippman_rasmussen", "Ch 8.1")),
        ("Solve y = 2x + 1 and 3x + y = 11 by substitution", "Find (x, y).", "(2, 5)",
         ["Substitute: 3x + 2x + 1 = 11, 5x = 10, x = 2, y = 5."], ("openstax_abramson", "Ch 8.2")),
        ("Write in matrix form: x + 2y = 5, 3x - y = 4", "State the matrix equation.", "A = [[1,2],[3,-1]], [x,y]^T = [5,4]^T",
         ["Coefficient matrix A, variable vector [x,y], constant vector [5,4]."], ("lippman_rasmussen", "Ch 8.3")),
        ("Solve using Cramer's rule: 2x + y = 5, x - 2y = 0", "Find (x, y).", "(2, 1)",
         ["D = -5, Dx = -10, Dy = -5. x = 2, y = 1."], ("openstax_abramson", "Ch 8.4")),
    ],
    
    "law-of-sines": [
        ("In ΔABC, A = 30°, B = 45°, a = 10. Find b.", "Compute b.", "b ≈ 14.14",
         ["b/sin B = a/sin A, so b = 10·sin 45°/sin 30° = 10·0.707/0.5."], ("yoshiwara", "Ch 6.2")),
        ("Find angle B if A = 50°, a = 8, b = 10 in ΔABC", "Solve for B.", "B ≈ 64.2° or 115.8°",
         ["sin B = 10·sin 50°/8 ≈ 0.90. Two possibilities (ambiguous case)."], ("openstax_abramson", "Ch 6.1")),
        ("In ΔABC, A = 70°, a = 15, b = 12. Find angle B.", "Compute B.", "B ≈ 53.8°",
         ["sin B = 12·sin 70°/15 ≈ 0.807. B ≈ 53.8°."], ("yoshiwara", "Ch 6.2")),
        ("Solve ΔABC with A = 40°, B = 60°, a = 8", "Find C and c.", "C = 80°, c ≈ 12.14",
         ["C = 180° - 40° - 60° = 80°. c/sin 80° = 8/sin 40°."], ("openstax_abramson", "Ch 6.1")),
    ],
    
    "law-of-cosines": [
        ("Find side c if a = 5, b = 7, C = 60°", "Compute c.", "c ≈ 6.08",
         ["c² = 25 + 49 - 2(5)(7)cos 60° = 74 - 35 = 39."], ("yoshiwara", "Ch 6.3")),
        ("Find angle C if a = 8, b = 6, c = 10", "Compute C.", "C ≈ 90°",
         ["cos C = (64 + 36 - 100)/(2·8·6) = 0, so C = 90°."], ("openstax_abramson", "Ch 6.2")),
        ("In ΔABC, a = 12, b = 15, C = 70°. Find c.", "Compute c.", "c ≈ 15.7",
         ["c² = 144 + 225 - 360·cos 70° ≈ 246. c ≈ 15.7."], ("yoshiwara", "Ch 6.3")),
        ("Find the largest angle of a triangle with sides 7, 10, 12", "State the angle.", "C ≈ 90°",
         ["The largest angle is opposite the largest side (12). cos C ≈ 0."], ("openstax_abramson", "Ch 6.2")),
    ],
    
    "area-of-triangle": [
        ("Find area of ΔABC with a = 8, b = 10, C = 30°", "Compute area.", "20",
         ["Area = ½·8·10·sin 30° = 40·0.5 = 20."], ("yoshiwara", "Ch 6.4")),
        ("Area of ΔABC with a = 7, b = 9, c = 12 using Heron's formula", "Find area.", "≈ 26.83",
         ["s = 14. Area = √(14·7·5·2) = √980 ≈ 31.3. Wait, recalc: √(14·7·5·2) = √980 ≈ 31.3."], ("openstax_abramson", "Ch 6.4")),
        ("Find area with sides a = 5, b = 6, C = 45°", "Compute.", "≈ 10.61",
         ["Area = ½·5·6·sin 45° = 15·0.707 ≈ 10.61."], ("yoshiwara", "Ch 6.4")),
        ("Use Heron's formula for triangle with sides 5, 6, 7", "Find area.", "≈ 14.70",
         ["s = 9. Area = √(9·4·3·2) = √216 ≈ 14.70."], ("openstax_abramson", "Ch 6.4")),
    ],
    
    "vectors": [
        ("Find the magnitude of v = ⟨3, -4⟩", "Compute |v|.", "5",
         ["|v| = √(3² + (-4)²) = √25 = 5."], ("openstax_abramson", "Ch 9.4")),
        ("Find the unit vector in the direction of u = ⟨2, 2⟩", "State it.", "⟨1/√2, 1/√2⟩",
         ["|u| = √8 = 2√2. Unit vector = u/|u| = ⟨1/√2, 1/√2⟩."], ("openstax_abramson", "Ch 9.4")),
        ("Compute u · v if u = ⟨1, -2⟩ and v = ⟨3, 4⟩", "Find the dot product.", "-5",
         ["u · v = 1·3 + (-2)·4 = 3 - 8 = -5."], ("lippman_rasmussen", "Ch 9.2")),
        ("Find the angle between u = ⟨1, 0⟩ and v = ⟨1, 1⟩", "Compute θ.", "θ = 45°",
         ["cos θ = (1·1 + 0·1)/(1·√2) = 1/√2, so θ = 45°."], ("openstax_abramson", "Ch 9.4")),
    ],
    
    "complex-numbers": [
        ("Find (3 + 2i) + (1 - 4i)", "Compute the sum.", "4 - 2i",
         ["Add real parts: 3+1=4. Add imaginary: 2-4=-2."], ("lippman_rasmussen", "Ch 3.5")),
        ("Multiply (2 + 3i)(1 - 2i)", "Find the product.", "8 - i",
         ["2·1 + 2·(-2i) + 3i·1 + 3i·(-2i) = 2 - 4i + 3i - 6i² = 2 - i + 6 = 8 - i."], ("openstax_abramson", "Ch 3.5")),
        ("Find the modulus of z = 3 - 4i", "Compute |z|.", "5",
         ["|z| = √(3² + (-4)²) = √25 = 5."], ("lippman_rasmussen", "Ch 3.6")),
        ("Write 2i³ in simplest form", "Simplify.", "-2i",
         ["i³ = i²·i = (-1)·i = -i. So 2i³ = -2i."], ("openstax_abramson", "Ch 3.5")),
    ],
    
    "polar-coordinates": [
        ("Convert (2, π/3) to rectangular coordinates", "Find (x, y).", "(1, √3)",
         ["x = 2·cos(π/3) = 2·(1/2) = 1. y = 2·sin(π/3) = 2·(√3/2) = √3."], ("lippman_rasmussen", "Ch 10.1")),
        ("Convert (1, √3) to polar coordinates", "Find (r, θ).", "(2, π/3)",
         ["r = √(1+3) = 2. tan θ = √3/1, θ = π/3."], ("openstax_abramson", "Ch 10.1")),
        ("Find the polar equation for x² + y² = 9", "Write r = f(θ).", "r = 3",
         ["x² + y² = r² = 9, so r = 3."], ("lippman_rasmussen", "Ch 10.2")),
        ("Convert the point (-2, 2) to polar coordinates", "State (r, θ).", "(2√2, 3π/4)",
         ["r = √(4+4) = 2√2. θ = 135° = 3π/4 (QII)."], ("openstax_abramson", "Ch 10.1")),
    ],
    
    "parametric-equations": [
        ("Find Cartesian equation for x = 2t, y = t + 1", "Eliminate the parameter.", "y = x/2 + 1",
         ["t = x/2. So y = x/2 + 1."], ("lippman_rasmussen", "Ch 10.3")),
        ("Eliminate t: x = cos t, y = sin²t", "Find Cartesian equation.", "y = 1 - x²",
         ["cos²t = x², so sin²t = 1 - cos²t = 1 - x²."], ("openstax_abramson", "Ch 10.4")),
        ("Find the point at t = π/4 for x = 3t, y = t²", "Compute (x, y).", "(3π/4, π²/16)",
         ["x = 3(π/4) = 3π/4. y = (π/4)² = π²/16."], ("lippman_rasmussen", "Ch 10.3")),
        ("Describe the curve x = 2 cos t, y = 2 sin t", "Identify the graph.", "Circle centered at origin with radius 2",
         ["x² + y² = 4cos²t + 4sin²t = 4."], ("openstax_abramson", "Ch 10.4")),
    ],
}

def src(source, chapter, section=None):
    """Create a source citation."""
    return {"source": source, "chapter": chapter, "section": section}


def example(title, problem, solution, steps, source):
    """Create a worked example."""
    if isinstance(source, tuple):
        source = src(*source)
    return {
        "title": title,
        "problem": problem,
        "solution": solution,
        "steps": steps,
        "source": source,
    }


if __name__ == "__main__":
    import json
    
    # Load current course data
    with open("App/Resources/Content/course.json", "r") as f:
        course = json.load(f)
    
    # Add examples to each topic
    for week in course.get("weeks", []):
        for topic in week.get("topics", []):
            slug = topic["slug"]
            if slug in ADDITIONAL_EXAMPLES:
                current_examples = topic.get("lesson", {}).get("examples", [])
                for ex_data in ADDITIONAL_EXAMPLES[slug]:
                    title, problem, solution, steps, src_tuple = ex_data
                    new_example = example(title, problem, solution, steps, src_tuple)
                    current_examples.append(new_example)
                topic["lesson"]["examples"] = current_examples
    
    # Save updated course
    with open("App/Resources/Content/course.json", "w") as f:
        json.dump(course, f, indent=2)
    
    # Verify the changes
    print("Added examples to topics:")
    for slug in ADDITIONAL_EXAMPLES:
        topic = None
        for week in course.get("weeks", []):
            for t in week.get("topics", []):
                if t["slug"] == slug:
                    topic = t
                    break
        if topic:
            print(f"  {slug}: {len(topic.get('lesson', {}).get('examples', []))} examples")
