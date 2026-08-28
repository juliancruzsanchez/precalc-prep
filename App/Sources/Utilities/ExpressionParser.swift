import Foundation

/// A simple recursive-descent parser for mathematical expressions of one variable `x`.
///
/// Grammar (precedence: low → high):
///   expr   = term (('+' | '-') term)*
///   term   = factor (('*' | '/') factor)*
///   factor = unary ('^' factor)?   // right-associative
///   unary  = '-' unary | primary
///   primary= number | ident | ident '(' args ')' | '(' expr ')'
///
/// Supported functions: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
///   exp, ln, log, sqrt, abs, floor, ceil, round, pow
/// Constants: pi, e, x
struct Expr {
    enum Op { case add, sub, mul, div, pow, neg }
    indirect enum Node {
        case number(Double)
        case variable(Character)
        case binary(Op, Node, Node)
        case unary(Op, Node)
        case function(name: String, args: [Node])
    }
    let root: Node

    /// Parse `2*x + sin(x)` etc. Throws on syntax error.
    static func parse(_ source: String) throws -> Expr {
        var parser = Parser(source: source)
        let node = try parser.parseExpr()
        try parser.expectEnd()
        return Expr(root: node)
    }

    /// Evaluate at `x`. Throws on math domain errors.
    func evaluate(at x: Double) throws -> Double {
        try Self.eval(root, x: x)
    }

    private static func eval(_ node: Node, x: Double) throws -> Double {
        switch node {
        case .number(let n): return n
        case .variable(let v):
            switch v {
            case "x": return x
            case "e": return M_E
            case "p": return .pi    // accept 'p' for pi to allow `pi` token
            default: throw EvalError.unknownVariable(String(v))
            }
        case .binary(let op, let a, let b):
            let lhs = try eval(a, x: x)
            let rhs = try eval(b, x: x)
            switch op {
            case .add: return lhs + rhs
            case .sub: return lhs - rhs
            case .mul: return lhs * rhs
            case .div:
                guard rhs != 0 else { throw EvalError.divisionByZero }
                return lhs / rhs
            case .pow:
                return Foundation.pow(lhs, rhs)
            case .neg:
                throw EvalError.invalidOp
            }
        case .unary(let op, let inner):
            let v = try eval(inner, x: x)
            switch op {
            case .neg: return -v
            default: throw EvalError.invalidOp
            }
        case .function(let name, let args):
            let values = try args.map { try eval($0, x: x) }
            return try apply(name: name, args: values)
        }
    }

    private static func apply(name: String, args: [Double]) throws -> Double {
        switch name {
        case "sin": return Foundation.sin(args[0])
        case "cos": return Foundation.cos(args[0])
        case "tan": return Foundation.tan(args[0])
        case "asin": guard args[0] >= -1, args[0] <= 1 else { throw EvalError.domain }
            return Foundation.asin(args[0])
        case "acos": guard args[0] >= -1, args[0] <= 1 else { throw EvalError.domain }
            return Foundation.acos(args[0])
        case "atan": return Foundation.atan(args[0])
        case "sinh": return Foundation.sinh(args[0])
        case "cosh": return Foundation.cosh(args[0])
        case "tanh": return Foundation.tanh(args[0])
        case "exp": return Foundation.exp(args[0])
        case "ln": guard args[0] > 0 else { throw EvalError.domain }
            return Foundation.log(args[0])
        case "log": guard args[0] > 0 else { throw EvalError.domain }
            return Foundation.log10(args[0])
        case "sqrt": guard args[0] >= 0 else { throw EvalError.domain }
            return Foundation.sqrt(args[0])
        case "abs": return Foundation.fabs(args[0])
        case "floor": return Foundation.floor(args[0])
        case "ceil": return Foundation.ceil(args[0])
        case "round": return Foundation.round(args[0])
        case "pow": return Foundation.pow(args[0], args[1])
        default: throw EvalError.unknownFunction(name)
        }
    }
}

enum ParseError: LocalizedError {
    case unexpectedCharacter(Character, Int)
    case unexpectedEnd
    case expectedGot(String, Character?)
    case invalidNumber(String)

    var errorDescription: String? {
        switch self {
        case .unexpectedCharacter(let c, let i): return "Unexpected character '\(c)' at position \(i)."
        case .unexpectedEnd: return "Expression ended unexpectedly."
        case .expectedGot(let s, let c): return "Expected \(s) but got \(c.map(String.init) ?? "end of input")."
        case .invalidNumber(let s): return "Could not parse number '\(s)'."
        }
    }
}

enum EvalError: LocalizedError {
    case divisionByZero
    case domain
    case unknownVariable(String)
    case unknownFunction(String)
    case invalidOp

    var errorDescription: String? {
        switch self {
        case .divisionByZero: return "Division by zero."
        case .domain: return "Argument is outside the function's domain."
        case .unknownVariable(let v): return "Unknown variable '\(v)'."
        case .unknownFunction(let f): return "Unknown function '\(f)'."
        case .invalidOp: return "Invalid operation."
        }
    }
}

private struct Parser {
    let source: String
    var i: String.Index

    init(source: String) {
        self.source = source
        self.i = source.startIndex
    }

    private var peek: Character? { i < source.endIndex ? source[i] : nil }

    @discardableResult
    private mutating func advance() -> Character? {
        guard i < source.endIndex else { return nil }
        let c = source[i]
        i = source.index(after: i)
        return c
    }

    private mutating func skipWhitespace() {
        while let c = peek, c.isWhitespace { i = source.index(after: i) }
    }

    mutating func expectEnd() throws {
        skipWhitespace()
        if i < source.endIndex {
            throw ParseError.unexpectedCharacter(source[i], source.distance(from: source.startIndex, to: i))
        }
    }

    mutating func parseExpr() throws -> Expr.Node {
        var node = try parseTerm()
        while true {
            skipWhitespace()
            guard let c = peek else { break }
            if c == "+" {
                advance()
                let rhs = try parseTerm()
                node = .binary(.add, node, rhs)
            } else if c == "-" {
                advance()
                let rhs = try parseTerm()
                node = .binary(.sub, node, rhs)
            } else { break }
        }
        return node
    }

    mutating func parseTerm() throws -> Expr.Node {
        var node = try parseFactor()
        while true {
            skipWhitespace()
            guard let c = peek else { break }
            if c == "*" {
                advance()
                let rhs = try parseFactor()
                node = .binary(.mul, node, rhs)
            } else if c == "/" {
                advance()
                let rhs = try parseFactor()
                node = .binary(.div, node, rhs)
            } else { break }
        }
        return node
    }

    mutating func parseFactor() throws -> Expr.Node {
        let lhs = try parseUnary()
        skipWhitespace()
        if peek == "^" {
            advance()
            let rhs = try parseFactor()  // right-associative
            return .binary(.pow, lhs, rhs)
        }
        return lhs
    }

    mutating func parseUnary() throws -> Expr.Node {
        skipWhitespace()
        guard let c = peek else { throw ParseError.unexpectedEnd }
        if c == "-" {
            advance()
            let inner = try parseUnary()
            return .unary(.neg, inner)
        } else if c == "+" {
            advance()
            return try parseUnary()
        }
        return try parsePrimary()
    }

    mutating func parsePrimary() throws -> Expr.Node {
        skipWhitespace()
        guard let c = peek else { throw ParseError.unexpectedEnd }
        if c == "(" {
            advance()
            let inner = try parseExpr()
            skipWhitespace()
            guard peek == ")" else { throw ParseError.expectedGot("')'", peek) }
            advance()
            return inner
        }
        if c.isNumber || c == "." {
            return try parseNumber()
        }
        if c.isLetter {
            return try parseIdent()
        }
        throw ParseError.unexpectedCharacter(c, source.distance(from: source.startIndex, to: i))
    }

    mutating func parseNumber() throws -> Expr.Node {
        var s = ""
        var seenDot = false
        while let c = peek {
            if c.isNumber { s.append(c); advance() }
            else if c == "." && !seenDot { s.append(c); seenDot = true; advance() }
            else { break }
        }
        // scientific
        if peek == "e" || peek == "E" {
            s.append(advance()!)
            if peek == "-" || peek == "+" { s.append(advance()!) }
            while let c = peek, c.isNumber { s.append(c); advance() }
        }
        guard let v = Double(s) else { throw ParseError.invalidNumber(s) }
        return .number(v)
    }

    mutating func parseIdent() throws -> Expr.Node {
        var name = ""
        while let c = peek, c.isLetter || c.isNumber || c == "_" {
            name.append(c)
            advance()
        }
        skipWhitespace()
        if peek == "(" {
            advance()
            var args: [Expr.Node] = []
            skipWhitespace()
            if peek != ")" {
                args.append(try parseExpr())
                while true {
                    skipWhitespace()
                    if peek == "," { advance(); args.append(try parseExpr()); continue }
                    break
                }
            }
            skipWhitespace()
            guard peek == ")" else { throw ParseError.expectedGot("')'", peek) }
            advance()
            // Translate a few aliases.
            let canonical: String
            switch name {
            case "ln": canonical = "ln"
            case "log10": canonical = "log"
            default: canonical = name
            }
            if canonical == "x" { return .variable("x") }
            if canonical == "pi" { return .number(.pi) }
            if canonical == "e" { return .number(M_E) }
            return .function(name: canonical, args: args)
        }
        // Bare identifier
        switch name {
        case "x": return .variable("x")
        case "pi": return .number(.pi)
        case "e": return .number(M_E)
        default: throw ParseError.expectedGot("number or function", name.first)
        }
    }
}
