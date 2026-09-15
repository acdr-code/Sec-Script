from lark import Transformer


# ====================== Nodes ======================

class FunctionCallNode:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument


class LetNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class IfNode:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body


class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class StringLiteral:
    def __init__(self, value):
        self.value = value


class NumberLiteral:
    def __init__(self, value):
        self.value = value


class BooleanLiteral:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name

class ForLoopNode:
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self. start = start
        self.end = end
        self.body = body

class WhileLoopNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


# ====================== Transformer ======================

class ASTBuilder(Transformer):

    def start(self, items):
        return items

    def statement(self, items):
        return items[0]

    def expr(self, items):
        return items[0]

    def func_call(self, items):
        name = items[0].name
        argument = items[1]
        return FunctionCallNode(name, argument)
    
    def let_stmt(self, items):
        name = items[0].name
        value = items[1]
        return LetNode(name, value)

    def if_stmt(self, items):
        condition = items[0]
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else None
        return IfNode(condition, then_body, else_body)

    def for_stmt(self, items):
        var_name = items[0].name
        start = items[1]
        end = items[2]
        body = items[3:]
        return ForLoopNode(var_name, start, end, body)

    def while_stmt(self, items):
        condition = items[0]
        body = items[1:]
        return WhileLoopNode(condition, body)

    def comparison(self, items):
        left, op, right = items
        return BinaryOpNode(left, str(op), right)

    def atom(self, items):
        return items[0]

    # ---------- Literals & Variable ----------

    def ESCAPED_STRING(self, token):
        return StringLiteral(str(token)[1:-1])

    def NUMBER(self, token):
        text = str(token)
        value = float(text) if "." in text else int(text)
        return NumberLiteral(value)

    def TRUE(self, _):
        return BooleanLiteral(True)

    def FALSE(self, _):
        return BooleanLiteral(False)

    def NAME(self, token):
        return Variable(str(token))