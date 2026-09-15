import AST
import sys

varEnv = {}

def evaluate(node):
    if isinstance(node, AST.StringLiteral):
        return node.value

    if isinstance(node, AST.NumberLiteral):
        return node.value

    if isinstance(node, AST.BooleanLiteral):
        return node.value

    if isinstance(node, AST.Variable):
        if node.name in varEnv:
            return varEnv[node.name]
        raise NameError(f"Variable '{node.name}' is not defined")

    if isinstance(node, AST.BinaryOpNode):
        left = evaluate(node.left)
        right = evaluate(node.right)
        op = node.op

        if op == "==": return left == right
        if op == "!=": return left != right
        if op == "<":  return left < right
        if op == ">":  return left > right
        if op == "<=": return left <= right
        if op == ">=": return left >= right

    if isinstance(node, AST.ListNode):
        listEnv = []
        for element in node.elements:
            listEnv.append(evaluate(element))
        return listEnv

    raise TypeError(f"Cannot evaluate: {type(node)}")


def interpret(node):
    if isinstance(node, AST.FunctionCallNode):
        if node.name == "out":
            value = evaluate(node.argument)
            print(value)
        elif node.name == "in":
            if isinstance(node.argument, AST.Variable):
                user_input = input()
                varEnv[node.argument.name] = user_input
            else:
                print("Error: in() expects a variable name")
        
        else:
            print(f"Unknown function: {node.name}", file=sys.stderr)

    elif isinstance(node, AST.LetNode):
        value = evaluate(node.value)
        varEnv[node.name] = value

    elif isinstance(node, AST.IfNode):
        cond_value = evaluate(node.condition)

        if cond_value:
            interpret(node.then_body)
        elif node.else_body is not None:
            interpret(node.else_body)

    elif isinstance(node, AST.ForLoopNode):
        start_val = evaluate(node.start)
        end_val = evaluate(node.end)

        for i in range(start_val, end_val + 1):
            varEnv[node.var_name] = i
            for stmt in node.body:
                interpret(stmt)

    elif isinstance(node, AST.WhileLoopNode):
        while evaluate(node.condition):
            for stmt in node.body:
                interpret(stmt)

    else:
        print(f"Unknown node type: {type(node)}", file=sys.stderr)