import SwiftUI

struct GraphView: View {
    let title: String
    let expression: String
    let domainX: ClosedRange<Double>
    let domainY: ClosedRange<Double>
    let note: String?

    private var parsed: (expr: Expr?, error: String?) {
        do {
            return (try Expr.parse(expression), nil)
        } catch {
            return (nil, error.localizedDescription)
        }
    }

    private var xMin: Double { domainX.lowerBound }
    private var xMax: Double { domainX.upperBound }
    private var yMin: Double { domainY.lowerBound }
    private var yMax: Double { domainY.upperBound }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .firstTextBaseline) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(title).font(.headline)
                    Text("y = \(expression)")
                        .font(.system(.subheadline, design: .monospaced))
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Text("x ∈ [\(format(xMin)), \(format(xMax))]")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            ZStack {
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color(.tertiarySystemBackground))
                Canvas { ctx, size in
                    drawGrid(ctx: ctx, size: size)
                    let p = parsed
                    if let expr = p.expr {
                        drawFunction(ctx: ctx, size: size, expr: expr)
                    } else if let err = p.error {
                        ctx.draw(Text("Parse error: \(err)")
                                    .font(.caption)
                                    .foregroundStyle(.red),
                                 at: CGPoint(x: 12, y: 24))
                    }
                    drawAxes(ctx: ctx, size: size)
                }
            }
            .frame(height: 260)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.primary.opacity(0.08)))

            if let note {
                Text(note)
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
        }
        .cardStyle()
    }

    // MARK: - Drawing

    private func drawGrid(ctx: GraphicsContext, size: CGSize) {
        let stepX = niceStep(span: xMax - xMin, target: 8)
        let stepY = niceStep(span: yMax - yMin, target: 6)
        let minorColor = Color.primary.opacity(0.06)
        let majorColor = Color.primary.opacity(0.15)
        var x = floor(xMin / stepX) * stepX
        while x <= xMax {
            let p = pointFor(x: x, y: 0, size: size)
            var path = Path()
            path.move(to: CGPoint(x: p.x, y: 0))
            path.addLine(to: CGPoint(x: p.x, y: size.height))
            let isMajor = abs(x.truncatingRemainder(dividingBy: stepX * 5)) < 1e-9
            ctx.stroke(path, with: .color(isMajor ? majorColor : minorColor), lineWidth: isMajor ? 0.8 : 0.4)
            x += stepX
        }
        var y = floor(yMin / stepY) * stepY
        while y <= yMax {
            let p = pointFor(x: 0, y: y, size: size)
            var path = Path()
            path.move(to: CGPoint(x: 0, y: p.y))
            path.addLine(to: CGPoint(x: size.width, y: p.y))
            let isMajor = abs(y.truncatingRemainder(dividingBy: stepY * 5)) < 1e-9
            ctx.stroke(path, with: .color(isMajor ? majorColor : minorColor), lineWidth: isMajor ? 0.8 : 0.4)
            y += stepY
        }
    }

    private func drawAxes(ctx: GraphicsContext, size: CGSize) {
        let origin = pointFor(x: 0, y: 0, size: size)
        var xPath = Path()
        xPath.move(to: CGPoint(x: 0, y: origin.y))
        xPath.addLine(to: CGPoint(x: size.width, y: origin.y))
        var yPath = Path()
        yPath.move(to: CGPoint(x: origin.x, y: 0))
        yPath.addLine(to: CGPoint(x: origin.x, y: size.height))
        ctx.stroke(xPath, with: .color(Color.primary.opacity(0.6)), lineWidth: 1)
        ctx.stroke(yPath, with: .color(Color.primary.opacity(0.6)), lineWidth: 1)
        // Tick labels on the x-axis
        let stepX = niceStep(span: xMax - xMin, target: 8)
        var lx = floor(xMin / stepX) * stepX
        while lx <= xMax {
            let p = pointFor(x: lx, y: 0, size: size)
            let text = Text(format(lx)).font(.system(size: 9)).foregroundStyle(.secondary)
            ctx.draw(text, at: CGPoint(x: p.x, y: min(size.height - 8, origin.y + 12)))
            lx += stepX
        }
        let stepY = niceStep(span: yMax - yMin, target: 6)
        var ly = floor(yMin / stepY) * stepY
        while ly <= yMax {
            let p = pointFor(x: 0, y: ly, size: size)
            let text = Text(format(ly)).font(.system(size: 9)).foregroundStyle(.secondary)
            ctx.draw(text, at: CGPoint(x: max(8, origin.x - 14), y: p.y))
            ly += stepY
        }
    }

    private func drawFunction(ctx: GraphicsContext, size: CGSize, expr: Expr) {
        let sampleCount = 600
        var path = Path()
        var started = false
        for i in 0...sampleCount {
            let t = Double(i) / Double(sampleCount)
            let x = xMin + t * (xMax - xMin)
            let yOpt = try? expr.evaluate(at: x)
            guard let y = yOpt, y.isFinite else {
                started = false
                continue
            }
            // Skip samples outside an extended band (avoid long spikes)
            if y < yMin - 3 * (yMax - yMin) || y > yMax + 3 * (yMax - yMin) {
                started = false
                continue
            }
            let p = pointFor(x: x, y: y, size: size)
            if !started {
                path.move(to: p)
                started = true
            } else {
                path.addLine(to: p)
            }
        }
        ctx.stroke(path, with: .color(Theme.accent), lineWidth: 2.2)
    }

    // MARK: - Mapping

    private func pointFor(x: Double, y: Double, size: CGSize) -> CGPoint {
        let px = CGFloat((x - xMin) / (xMax - xMin)) * size.width
        let py = CGFloat(1 - (y - yMin) / (yMax - yMin)) * size.height
        return CGPoint(x: px, y: py)
    }

    // MARK: - Helpers

    private func niceStep(span: Double, target: Int) -> Double {
        guard span > 0, target > 0 else { return 1 }
        let raw = span / Double(target)
        let exponent = floor(log10(raw))
        let fraction = raw / pow(10, exponent)
        let nice: Double
        if fraction < 1.5 { nice = 1 }
        else if fraction < 3 { nice = 2 }
        else if fraction < 7 { nice = 5 }
        else { nice = 10 }
        return nice * pow(10, exponent)
    }

    private func format(_ value: Double) -> String {
        if value == value.rounded() { return String(format: "%.0f", value) }
        if abs(value) < 0.01 || abs(value) > 1000 {
            return String(format: "%.1e", value)
        }
        return String(format: "%.2f", value)
    }
}
