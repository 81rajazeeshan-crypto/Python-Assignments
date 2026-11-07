### Task 05 | Expression Validator and Evaluator
### Concepts: Stacks, parsing, exception handling
### Problem: Create a calculator for integer expressions containing +, -, *, /, parentheses, and whitespace. Apply standard operator precedence and parentheses.
### Requirements: Do not use eval(), exec(), or third-party parsers. Handle unary minus, malformed expressions, and division by zero.#
### Sample / expected behavior: Input: "-(3 + 2) * 4 + 18 / 3" -> -14.0.


def evaluate_expression(expr: str) -> float:
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Expression cannot be empty.")
        
    s = expr.replace(" ", "")
    if not s:
        raise ValueError("Empty expression.")
        
    tokens = []
    i = 0
    n = len(s)
    
    
    while i < n:
        char = s[i]
        if char.isdigit() or char == '.':
            num_str = ""
            while i < n and (s[i].isdigit() or s[i] == '.'):
                num_str += s[i]
                i += 1
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
        elif char in "+-*/()":
           
            if char == '-' and (i == 0 or s[i-1] in "(+-*/"):
                tokens.append(0)
                tokens.append('-')
                i += 1
            else:
                tokens.append(char)
                i += 1
        else:
            raise ValueError(f"Invalid character in expression: {char}")
            
    def apply_op(op, b, a):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero error.")
            return a / b
        return 0

    def precedence(op):
        if op in ('+', '-'): return 1
        if op in ('*', '/'): return 2
        return 0

    values = []
    ops = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, (int, float)):
            values.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(apply_op(op, val2, val1))
            if not ops or ops[-1] != '(':
                raise ValueError("Mismatched parentheses.")
            ops.pop()
        elif token in "+-*/":
            while (ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token)):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(apply_op(op, val2, val1))
            ops.append(token)
        i += 1
        
    while ops:
        op = ops.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses.")
        val2 = values.pop()
        val1 = values.pop()
        values.append(apply_op(op, val2, val1))
        
    if len(values) != 1:
        raise ValueError("Malformed expression.")
        
    return float(values[0])



if __name__ == "__main__":
    test_expr = "-(3 + 2) * 4 + 18 / 3"
    try:
        result = evaluate_expression(test_expr)
        print(f"Expression: {test_expr}")
        print(f"Result: {result}")  
    except Exception as e:
        print("Error:", e)
        
    print("10 + 2 * 6 =", evaluate_expression("10 + 2 * 6"))       
    print("100 / (2 + 3) =", evaluate_expression("100 / (2 + 3)")) 