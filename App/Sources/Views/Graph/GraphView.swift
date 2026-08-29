import SwiftUI

struct GraphView: View {
    let title: String
    let expression: String
    let domainX: ClosedRange<Double>
    let domainY: ClosedRange<Double>
    let note: String?
    var customPoints: [(x: Double, y: Double)] = []

    @State private var touchLocation: CGPoint? = nil
    @State private var touchValue: (x: Double, y: Double)? = nil
    @State private var curvePoint: CGPoint? = nil
    @State private var isTouching: Bool = false

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

            GeometryReader { proxy in
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
                        // Draw custom points
                        for point in customPoints {
                            drawPoint(ctx: ctx, size: size, x: point.x, y: point.y)
                        }
                        drawAxes(ctx: ctx, size: size)
                    }
                    .gesture(
                        DragGesture(minimumDistance: 0, coordinateSpace: .local)
                            .onChanged { value in
                                isTouching = true
                                touchLocation = value.location
                                let size = proxy.size
                                let yTarget = yFromPoint(value.location, size: size)
                                if let expr = parsed.expr,
                                   let (x, y) = findPointOnCurve(forY: yTarget, expr: expr) {
                                    touchValue = (x: x, y: y)
                                    curvePoint = pointFor(x: x, y: y, size: size)
                                } else {
                                    // Fallback: show the touched coordinate as-is so the
                                    // user still gets feedback when the function is undefined.
                                    let xAtTouch = xFromPoint(value.location, size: size)
                                    touchValue = (x: xAtTouch, y: yTarget)
                                    curvePoint = value.location
                                }
                            }
                            .onEnded { _ in
                                isTouching = false
                                touchLocation = nil
                                touchValue = nil
                                curvePoint = nil
                            }
                    )
                    // Touch indicator
                    if isTouching, let cp = curvePoint, let value = touchValue {
                        // Faint crosshair guides through the curve point
                        Path { path in
                            path.move(to: CGPoint(x: cp.x, y: 0))
                            path.addLine(to: CGPoint(x: cp.x, y: proxy.size.height))
                            path.move(to: CGPoint(x: 0, y: cp.y))
                            path.addLine(to: CGPoint(x: proxy.size.width, y: cp.y))
                        }
                        .stroke(Theme.accent.opacity(0.25), style: StrokeStyle(lineWidth: 0.5, dash: [3, 3]))
                        // Marker on the curve
                        Circle()
                            .fill(Theme.accent)
                            .frame(width: 12, height: 12)
                            .overlay(Circle().stroke(.white, lineWidth: 2))
                            .shadow(color: Theme.accent.opacity(0.4), radius: 3)
                            .position(cp)
                        // Coordinate label
                        CoordinateLabel(x: value.x, y: value.y)
                            .position(x: clamp(cp.x, 60, proxy.size.width - 60),
                                      y: max(cp.y - 28, 22))
                    }
                }
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.primary.opacity(0.08)))
            }
            .frame(height: 260)

            if let note {
                Text(note)
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
        }
        .cardStyle()
    }

    private func xFromPoint(_ point: CGPoint, size: CGSize) -> Double {
        guard size.width > 0 else { return xMin }
        return xMin + (Double(point.x) / Double(size.width)) * (xMax - xMin)
    }

    private func yFromPoint(_ point: CGPoint, size: CGSize) -> Double {
        guard size.height > 0 else { return yMax }
        return yMax - (Double(point.y) / Double(size.height)) * (yMax - yMin)
    }

    /// Given a target Y on the graph, find the (x, y) point on the function curve
    /// at that Y. Samples the function across the X domain and uses linear
    /// interpolation between adjacent samples that bracket the target Y, which
    /// gives an exact crossing. Falls back to the closest sample when the
    /// function does not actually reach the target Y within the visible band.
    private func findPointOnCurve(forY yTarget: Double, expr: Expr) -> (x: Double, y: Double)? {
        let sampleCount = 600
        var prev: (x: Double, y: Double)? = nil
        var bestSample: (x: Double, y: Double, distY: Double)? = nil

        for i in 0...sampleCount {
            let t = Double(i) / Double(sampleCount)
            let x = xMin + t * (xMax - xMin)
            guard let y = (try? expr.evaluate(at: x)), y.isFinite else {
                prev = nil
                continue
            }

            let distY = abs(y - yTarget)
            if bestSample == nil || distY < bestSample!.distY {
                bestSample = (x, y, distY)
            }

            // Look for a sign change between the previous and current sample so
            // we can interpolate to the exact X where f(x) = yTarget.
            if let p = prev {
                let crosses = (p.y <= yTarget && y >= yTarget) || (p.y >= yTarget && y <= yTarget)
                if crosses, abs(y - p.y) > 1e-12 {
                    let frac = (yTarget - p.y) / (y - p.y)
                    let xInterp = p.x + frac * (x - p.x)
                    return (x: xInterp, y: yTarget)
                }
            }

            prev = (x, y)
        }

        return bestSample.map { (x: $0.x, y: $0.y) }
    }

    private func clamp(_ value: CGFloat, _ minVal: CGFloat, _ maxVal: CGFloat) -> CGFloat {
        min(max(value, minVal), maxVal)
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

    private func drawPoint(ctx: GraphicsContext, size: CGSize, x: Double, y: Double) {
        let p = pointFor(x: x, y: y, size: size)
        // Only draw if point is within visible range
        guard p.x >= 0 && p.x <= size.width && p.y >= 0 && p.y <= size.height else { return }

        // Draw point marker
        var pointPath = Path()
        pointPath.addEllipse(in: CGRect(x: p.x - 5, y: p.y - 5, width: 10, height: 10))
        ctx.fill(pointPath, with: .color(Theme.warning))
        ctx.stroke(pointPath, with: .color(.white), lineWidth: 1.5)
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

struct CoordinateLabel: View {
    let x: Double
    let y: Double

    var body: some View {
        Text("(\(formatCoord(x)), \(formatCoord(y)))")
            .font(.callout.monospacedDigit().weight(.medium))
            .foregroundStyle(.white)
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .background(Theme.accent.opacity(0.95), in: RoundedRectangle(cornerRadius: 8))
            .shadow(color: .black.opacity(0.2), radius: 3, y: 1)
    }

    private func formatCoord(_ value: Double) -> String {
        // Cap at 2 decimal places, no scientific notation.
        return String(format: "%.2f", value)
    }
}
