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

class ListNode:
    def __init__(self, elements):
        self.elements = elements

class IndexingNode:
    def __init__(self, list_name, index):
        self.list_name = list_name
        self.index = index

class ForLoopNode:
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self. start = start
        self.end = end
        self.body = body

class ForItemLoopNode:
    def __init__(self, var_name, list_name, body):
        self.var_name = var_name
        self.list_name = list_name
        self.body = body

class WhileLoopNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionNode:
    def __init__(self, name, parametrs, body):
        self.name = name
        self.parametrs = parametrs
        self.body = body

class ReturnNode:
    def __init__(self, value):
        self.value = value

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
        arguments = items[1]
        return FunctionCallNode(name, arguments)

    def args(self, items):
        values = []
        for item in items:
            values.append(item)
        return values
    
    
    def let_stmt(self, items):
        name = items[0].name
        value = items[1]
        return LetNode(name, value)

    def list(self, items):
        values = items[:]
        return ListNode(values)

    def index_access(self, items):
        name = items[0].name
        value = items[1]
        return IndexingNode(name, value)

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

    def foreach_stmt(self, items):
        var_name = items[0].name
        list_name = items[1].name
        body = items[2:]
        return ForItemLoopNode(var_name, list_name, body)

    def while_stmt(self, items):
        condition = items[0]
        body = items[1:]
        return WhileLoopNode(condition, body)

    def function_stmt(self, items):
        name = items[0].name
        parametrs = items[1]
        body = items[2:]
        return FunctionNode(name, parametrs, body)

    def params(self, items):
        values = []
        for item in items:
            values.append(item.name)
        return values

    def return_stmt(self, items):
        return ReturnNode(items[0])

    def comparison(self, items):
        left, op, right = items
        return BinaryOpNode(left, str(op), right)

    def math_ing(self, items):
        left, op, right = items
        return BinaryOpNode(left, op, right)

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