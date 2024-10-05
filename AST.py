from typing import Any, Self, Callable
import re

class Num:
    def __init__(self, num: str | int | float):
        if isinstance(num, str):
            self.snum = num
            self.num = int(num) if self.is_int else float(num)
        else:
            self.num = num
            self.snum = str(num)
    
    @property
    def is_positive(self) -> bool:
        return self.num > 0
    
    @property
    def is_float(self) -> bool:
        return self.snum.count(".") == 1

    @property
    def is_int(self) -> bool:
        return self.snum.isdigit()
    
    def __call__(self, *args, **kwargs):
        return self
    
    def __repr__(self) -> str:
        return f"int({self.num})" if self.is_int else f"float({self.num})"
    
    def __str__(self) -> str:
        return self.snum
    
    def __int__(self) -> int:
        return self.num
    
    def __float__(self) -> float:
        return self.num
    
    def __add__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num + value.num)
        return Num(self.num + value)
    
    def __sub__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num - value.num)
        return Num(self.num - value)
    
    def __mul__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num * value.num)
        return Num(self.num * value)
    
    def __truediv__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num / value.num)
        return Num(self.num / value)
    
    def __floordiv__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num // value.num)
        return Num(self.num // value)
    
    def __mod__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num % value.num)
        return Num(self.num % value)
    
    def __pow__(self, value: Self | int | float) -> Self:
        if isinstance(value, Num):
            return Num(self.num ** value.num)
        return Num(self.num ** value)
    
    def __eq__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num == value.num
        return self.num == value
    
    def __ne__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num != value.num
        return self.num != value
    
    def __lt__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num < value.num
        return self.num < value
    
    def __le__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num <= value.num
        return self.num <= value
    
    def __gt__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num > value.num
        return self.num > value
    
    def __ge__(self, value: Self | int | float) -> bool:
        if isinstance(value, Num):
            return self.num >= value.num
        return self.num >= value
    
class Operator:
    def __init__(self, op: str) -> None:
        self.op = op

    def __call__(self, left: Callable[[], int | float | Num] | Num, right: Callable[[], int | float | Num] | Num) -> Num:
        left_: Num = left if isinstance(left, Num) else left()
        right_: Num = right if isinstance(right, Num) else right()
        if self.op == "+":
            return left_ + right_
        elif self.op == "-":
            return left_ - right_
        elif self.op == "*":
            return left_ * right_
        elif self.op == "/":
            return left_ / right_
        elif self.op == "//":
            return left_ // right_
        elif self.op == "%":
            return left_ % right_
        elif self.op == "**":
            return left_ ** right_
        
    def __str__(self) -> str:
        return self.op
    
    def __repr__(self) -> str:
        return f"Op({self.op})"
    
    def __eq__(self, other: Self | str) -> bool:
        if isinstance(other, Operator):
            return self.op == other.op
        return self.op == other
    
    def __ne__(self, other: Self | str) -> bool:
        if isinstance(other, Operator):
            return self.op != other.op
        return self.op != other
    
class BinOp:
    def __init__(self, left: Num, op: Operator, right: Num) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.op(self.left, self.right)
    
def tokenize(expression: str) -> list:
    token_pattern = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(.))")
    # token_pattern = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([+\-*/%^()]))\s*")
    tokens = []
    for number, operator in token_pattern.findall(expression):
        if number:
            tokens.append(('NUM', Num(number)))
        elif operator:
            if operator == '(' or operator == ')':
                tokens.append(('OP', operator))
            else:
                tokens.append(('OP', Operator(operator)))
    return tokens

def parse_tokens(tokens: list) -> BinOp:
    def parse_primary():
        token_type, value = tokens.pop(0)
        if token_type == 'NUM':
            return value
        elif value == '(':
            expr = parse_expression()
            tokens.pop(0)
            return expr
        raise SyntaxError("Unexpected token: %s" % value)

    def parse_term():
        node = parse_primary()
        while tokens and tokens [0][1] in ('*', '/', '%', '//', '**'):
            op_token = tokens.pop(0)
            op_func = op_token[1]
            right = parse_term()
            node = BinOp(node, op_func, right)
        return node

    def parse_expression():
        node = parse_term()
        while tokens and tokens [0][1] in ('+', '-'):
            op_token = tokens.pop(0)
            op_func = op_token[1]
            right = parse_term()
            node = BinOp(node, op_func, right)
        return node
    return parse_expression()

def evaluate(expression: str):
    expression_ = expression.replace(' ', '')
    tokens = tokenize(expression_)
    return parse_tokens(tokens)()

if __name__ == "__main__":
    # some examples
    print(Num(1) + Num(2))
    print(Operator("+")(Num(1), Num(2)))
    print(Num(1) + 2)
    print(Num(1) + 2.0)
    print(evaluate("1+2"))
    print(evaluate("1+2*3"))
    print(evaluate("1+2*3+4"))
