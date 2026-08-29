import SwiftUI

struct ToolsView: View {
    @State private var selected: Tool = .plotter
    @State private var initialExpression: String? = nil

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                Picker("Tool", selection: $selected) {
                    ForEach(Tool.allCases) { tool in
                        Text(tool.label).tag(tool)
                    }
                }
                .pickerStyle(.segmented)
                .padding(.horizontal)
                .padding(.top, 8)

                Divider().padding(.top, 8)

                Group {
                    switch selected {
                    case .plotter:
                        GraphingPlaygroundView(initialExpression: initialExpression)
                            .onChange(of: selected) { _, _ in
                                initialExpression = nil
                            }
                    case .unitCircle:
                        UnitCircleView()
                    case .formulas:
                        FormulaReferenceView()
                    }
                }
            }
            .navigationTitle("Tools")
        }
        .onReceive(NotificationCenter.default.publisher(for: .switchToPlotterWithExpression)) { notification in
            if let expr = notification.object as? String {
                selected = .plotter
                initialExpression = expr
            }
        }
    }

    enum Tool: String, CaseIterable, Identifiable {
        case plotter, unitCircle, formulas
        var id: String { rawValue }
        var label: String {
            switch self {
            case .plotter: return "Plotter"
            case .unitCircle: return "Unit Circle"
            case .formulas: return "Formulas"
            }
        }
    }
}

struct GraphingPlaygroundView: View {
    @State private var expression: String = "sin(x) * x / 4"
    @State private var xMin: Double = -10
    @State private var xMax: Double = 10
    @State private var yMin: Double = -5
    @State private var yMax: Double = 5
    @State private var customPoints: [(x: Double, y: Double)] = []
    @State private var newPointX: String = ""
    @State private var newPointY: String = ""

    var initialExpression: String? = nil

    private var parsed: Bool { (try? Expr.parse(expression)) != nil }

    init(initialExpression: String? = nil) {
        _initialExpression = State(initialValue: initialExpression)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Expression").font(.caption.weight(.semibold))
                    HStack(spacing: 4) {
                        Text("y =")
                            .font(.system(.body, design: .monospaced))
                            .foregroundStyle(.secondary)
                        TextField("e.g. sin(x), x^2 - 4, exp(-x)", text: $expression)
                            .textFieldStyle(.roundedBorder)
                            .autocorrectionDisabled()
                            .font(.system(.body, design: .monospaced))
                    }
                    if !parsed {
                        Text("Couldn't parse this expression.")
                            .font(.caption)
                            .foregroundStyle(Theme.danger)
                    }
                }
                if parsed {
                    GraphView(
                        title: "Custom plot",
                        expression: expression,
                        domainX: xMin...xMax,
                        domainY: yMin...yMax,
                        note: "Functions: sin, cos, tan, exp, ln, log, sqrt, abs, floor, ceil, pow(x, n)",
                        customPoints: customPoints
                    )
                }
                domainControls
                valueTableSection
                customPointsSection
            }
            .padding()
        }
        .onAppear {
            if let expr = initialExpression, !expr.isEmpty {
                expression = expr
                initialExpression = nil
            }
        }
    }

    private var valueTableSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Value Table").font(.caption.weight(.semibold))
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 0) {
                    ForEach([-3, -2, -1, 0, 1, 2, 3], id: \.self) { xVal in
                        VStack(spacing: 4) {
                            Text("x = \(xVal)")
                                .font(.caption2.weight(.semibold))
                                .foregroundStyle(Theme.accent)
                            let yVal = evaluateAt(xVal)
                            Text("y = \(formatNumber(yVal))")
                                .font(.caption.monospacedDigit())
                                .foregroundStyle(.secondary)
                        }
                        .frame(width: 70)
                        .padding(.vertical, 8)
                        .background(
                            xVal == 0 ? Color.accentColor.opacity(0.08) : Color.clear,
                            in: RoundedRectangle(cornerRadius: 8)
                        )
                        .overlay(
                            Rectangle()
                                .fill(Color.primary.opacity(0.08))
                                .frame(width: 1),
                            alignment: .trailing
                        )
                    }
                }
            }
            .padding(.horizontal, 8)
            .background(Theme.card, in: RoundedRectangle(cornerRadius: 12))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.primary.opacity(0.05), lineWidth: 1)
            )
        }
        .cardStyle()
    }

    private var customPointsSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("Custom Points").font(.caption.weight(.semibold))
                Spacer()
                Button {
                    if let x = Double(newPointX), let y = Double(newPointY) {
                        customPoints.append((x: x, y: y))
                        newPointX = ""
                        newPointY = ""
                    }
                } label: {
                    Image(systemName: "plus.circle.fill")
                        .foregroundStyle(Theme.accent)
                }
                .disabled(newPointX.isEmpty || newPointY.isEmpty)
            }
            HStack(spacing: 8) {
                TextField("x", text: $newPointX)
                    .keyboardType(.numbersAndPunctuation)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 60)
                TextField("y", text: $newPointY)
                    .keyboardType(.numbersAndPunctuation)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 60)
            }
            if !customPoints.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(Array(customPoints.enumerated()), id: \.offset) { idx, point in
                        HStack {
                            Text("(\(formatNumber(point.x)), \(formatNumber(point.y)))")
                                .font(.caption.monospacedDigit())
                            Spacer()
                            Button {
                                customPoints.remove(at: idx)
                            } label: {
                                Image(systemName: "xmark.circle.fill")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                        .padding(.vertical, 4)
                        .padding(.horizontal, 8)
                        .background(Theme.accentSoft, in: RoundedRectangle(cornerRadius: 6))
                    }
                }
            }
        }
        .cardStyle()
    }

    private func evaluateAt(_ x: Double) -> Double? {
        guard let expr = try? Expr.parse(expression) else { return nil }
        return try? expr.evaluate(at: x)
    }

    private func formatNumber(_ value: Double) -> String {
        if value == value.rounded() { return String(format: "%.0f", value) }
        return String(format: "%.2f", value)
    }

    private var domainControls: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Domain").font(.caption.weight(.semibold))
            HStack(spacing: 16) {
                stepper("x min", value: $xMin)
                stepper("x max", value: $xMax)
                Spacer()
            }
            HStack(spacing: 16) {
                stepper("y min", value: $yMin)
                stepper("y max", value: $yMax)
                Spacer()
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .cardStyle()
    }

    private func stepper(_ label: String, value: Binding<Double>) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(label).font(.caption2)
            HStack(spacing: 4) {
                TextField("", value: value, format: .number)
                    .keyboardType(.numbersAndPunctuation)
                    .frame(maxWidth: 60)
                    .textFieldStyle(.roundedBorder)
                Stepper("", value: value, in: -1000...1000, step: 1)
                    .labelsHidden()
            }
        }
    }
}

struct UnitCircleView: View {
    @State private var angleDegrees: Double = 30

    private var radians: Double { angleDegrees * .pi / 180 }
    private var x: Double { Foundation.cos(radians) }
    private var y: Double { Foundation.sin(radians) }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 12).fill(Color(.tertiarySystemBackground))
                Canvas { ctx, size in
                    let center = CGPoint(x: size.width / 2, y: size.height / 2)
                    let radius = min(size.width, size.height) / 2 - 20

                    // Circle
                    var circle = Path()
                    circle.addEllipse(in: CGRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2))
                    ctx.stroke(circle, with: .color(Color.primary.opacity(0.6)), lineWidth: 1.5)

                    // Axes
                    var xAxis = Path()
                    xAxis.move(to: CGPoint(x: 0, y: center.y))
                    xAxis.addLine(to: CGPoint(x: size.width, y: center.y))
                    var yAxis = Path()
                    yAxis.move(to: CGPoint(x: center.x, y: 0))
                    yAxis.addLine(to: CGPoint(x: center.x, y: size.height))
                    ctx.stroke(xAxis, with: .color(Color.primary.opacity(0.25)))
                    ctx.stroke(yAxis, with: .color(Color.primary.opacity(0.25)))

                    // Angle arc
                    var arc = Path()
                    arc.addArc(center: center, radius: 30, startAngle: .degrees(0), endAngle: .degrees(angleDegrees), clockwise: false)
                    ctx.stroke(arc, with: .color(Theme.accent), lineWidth: 2)

                    // Radius line
                    let endPoint = CGPoint(x: center.x + CGFloat(x) * radius, y: center.y - CGFloat(y) * radius)
                    var radiusLine = Path()
                    radiusLine.move(to: center)
                    radiusLine.addLine(to: endPoint)
                    ctx.stroke(radiusLine, with: .color(Theme.accent), lineWidth: 2)

                    // Point on circle
                    var dot = Path()
                    dot.addEllipse(in: CGRect(x: endPoint.x - 5, y: endPoint.y - 5, width: 10, height: 10))
                    ctx.fill(dot, with: .color(Theme.accent))

                    // Drop lines to x and y axes
                    var dropY = Path()
                    dropY.move(to: CGPoint(x: endPoint.x, y: center.y))
                    dropY.addLine(to: endPoint)
                    ctx.stroke(dropY, with: .color(Color.secondary), style: StrokeStyle(lineWidth: 1, dash: [3]))
                    var dropX = Path()
                    dropX.move(to: CGPoint(x: center.x, y: endPoint.y))
                    dropX.addLine(to: endPoint)
                    ctx.stroke(dropX, with: .color(Color.secondary), style: StrokeStyle(lineWidth: 1, dash: [3]))
                }
            }
            .frame(height: 260)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.primary.opacity(0.08)))

            VStack(alignment: .leading, spacing: 4) {
                Text("Angle: \(Int(angleDegrees))° = \(format(radians)) rad")
                Text("cos(θ) = x = \(format(x))")
                Text("sin(θ) = y = \(format(y))")
                if abs(y) > 1e-9 {
                    Text("tan(θ) = y/x = \(format(y / x))")
                }
            }
            .font(.subheadline.monospacedDigit())

            HStack {
                Text("0°")
                Slider(value: $angleDegrees, in: 0...360, step: 1)
                Text("360°")
            }

            HStack {
                ForEach([0, 30, 45, 60, 90, 120, 180, 270], id: \.self) { deg in
                    Button("\(deg)°") { angleDegrees = Double(deg) }
                        .font(.caption)
                        .buttonStyle(.bordered)
                }
            }
        }
        .padding()
    }

    private func format(_ v: Double) -> String {
        if v == v.rounded() { return String(format: "%.0f", v) }
        return String(format: "%.3f", v)
    }
}

struct FormulaReferenceView: View {
    @State private var selectedExpression: String = ""
    @State private var showingPlotter: Bool = false
    
    private let groups: [(String, [(String, String)])] = [
        ("Algebra", [
            ("Quadratic formula", "x = (-b ± √(b² - 4ac)) / 2a"),
            ("Difference of squares", "a² - b² = (a - b)(a + b)"),
            ("Perfect square", "(a ± b)² = a² ± 2ab + b²"),
        ]),
        ("Exponents & logs", [
            ("Product rule", "log(MN) = log M + log N"),
            ("Quotient rule", "log(M/N) = log M - log N"),
            ("Power rule", "log(M^p) = p log M"),
            ("Change of base", "log_b x = ln x / ln b"),
            ("ln e = 1", "ln 1 = 0"),
        ]),
        ("Trig identities", [
            ("Pythagorean", "sin²θ + cos²θ = 1"),
            ("1 + tan²θ = sec²θ", "1 + cot²θ = csc²θ"),
            ("Cofunction", "sin(π/2 - θ) = cos θ"),
            ("Sum", "sin(A + B) = sin A cos B + cos A sin B"),
            ("Double angle", "sin 2θ = 2 sin θ cos θ"),
        ]),
        ("Laws of sines / cosines", [
            ("Law of Sines", "a/sin A = b/sin B = c/sin C"),
            ("Law of Cosines", "c² = a² + b² - 2ab cos C"),
            ("Area (SAS)", "Area = ½ ab sin C"),
            ("Area (SSS, Heron)", "Area = √(s(s-a)(s-b)(s-c))"),
        ]),
        ("Vectors", [
            ("Magnitude", "|v| = √(a² + b²)"),
            ("Dot product", "u · v = u₁v₁ + u₂v₂ = |u||v| cos θ"),
        ]),
        ("Complex / polar", [
            ("Polar → rectangular", "x = r cos θ,  y = r sin θ"),
            ("De Moivre", "(cos θ + i sin θ)ⁿ = cos(nθ) + i sin(nθ)"),
        ]),
    ]

    var body: some View {
        List {
            ForEach(groups, id: \.0) { group in
                Section(group.0) {
                    ForEach(group.1, id: \.0) { item in
                        Button {
                            // Extract expression part after "=" for graphing
                            if let eqIndex = item.1.firstIndex(of: "=") {
                                let expr = String(item.1[item.1.index(after: eqIndex)...])
                                    .replacingOccurrences(of: " ", "")
                                    .replacingOccurrences(of: "²", "^2")
                                    .replacingOccurrences(of: "³", "^3")
                                    .replacingOccurrences(of: "√", "sqrt")
                                    .replacingOccurrences(of: "π", "pi")
                                    .replacingOccurrences(of: "θ", "x")
                                    .replacingOccurrences(of: "×", "*")
                                    .replacingOccurrences(of: "÷", "/")
                                    .replacingOccurrences(of: "·", "*")
                                selectedExpression = expr
                                showingPlotter = true
                            }
                        } label: {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(item.0).font(.subheadline.weight(.semibold))
                                HStack {
                                    MathBlock(text: item.1, compact: true)
                                    Spacer()
                                    Image(systemName: "chart.line.uptrend.xyaxis")
                                        .font(.caption)
                                        .foregroundStyle(Theme.accent)
                                }
                            }
                            .padding(.vertical, 4)
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
        }
        .listStyle(.insetGrouped)
        .onChange(of: showingPlotter) { _, newValue in
            if newValue && !selectedExpression.isEmpty {
                // Post notification to switch to plotter tab with expression
                NotificationCenter.default.post(
                    name: .switchToPlotterWithExpression,
                    object: selectedExpression
                )
            }
        }
    }
}

extension Notification.Name {
    static let switchToPlotterWithExpression = Notification.Name("switchToPlotterWithExpression")
}
