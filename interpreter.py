import AST
import sys
from concurrent.futures import ThreadPoolExecutor
import SecurityStuff
from scapy.all import get_if_list
import subprocess

env_stack = [{}]
funcEnv = {}

#calling function
def call_function(node):
    func_def = funcEnv[node.name]

    new_scope = {}
    for i in range(len(func_def.parametrs)):
        param_name = func_def.parametrs[i]
        arg_value = evaluate(node.argument[i])
        new_scope[param_name] = arg_value

    env_stack.append(new_scope)

    return_value = None
    for stmt in func_def.body:
        result = interpret(stmt)
        if result is not None and result[0] == "RETURN":
            return_value = result[1]
            break

    env_stack.pop()
    return return_value


def evaluate(node):
    if isinstance(node, AST.StringLiteral):
        return node.value

    if isinstance(node, AST.NumberLiteral):
        return node.value

    if isinstance(node, AST.BooleanLiteral):
        return node.value

    if isinstance(node, AST.Variable):
        if node.name in env_stack[-1]:
            return env_stack[-1][node.name]
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
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "/": return left / right
        if op == "*": return left * right
        if op == "&": return str(left) + str(right)

    if isinstance(node, AST.ListNode):
        listEnv = []
        for element in node.elements:
            listEnv.append(evaluate(element))
        return listEnv

    if isinstance(node, AST.DictNode):
        dictEnv = {}
        for key, valueNode in node.pairs:
            dictEnv[key] = evaluate(valueNode)
        return dictEnv

    if isinstance(node, AST.IndexingNode):
            actualName = env_stack[-1][node.container]
            index = evaluate(node.index)
            return actualName[index]

    if isinstance(node, AST.FunctionCallNode):
        if node.name in funcEnv:
            return call_function(node)

        #built-ins
        if node.name == "getMyIfaces":
            return get_if_list()

        if node.name == "getMyIp":
            result =  subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
            return result.stdout

        if node.name == "myusrname":
            result = subprocess.run(["whoami"], capture_output=True, text=True, check=True)
            return result.stdout

        if node.name == "netInfo":
            result = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True)
            return result.stdout

        raise TypeError(f"Cannot evaluate function: {node.name}")

    if isinstance(node, AST.PortScanNode):
        ip = evaluate(node.ip)
        start = evaluate(node.start)
        end = evaluate(node.end)
        timeout = evaluate(node.timeout)
        
        open_ports = []

        def scan(port):
            SecurityStuff.portScan(ip, port, timeout, open_ports)

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scan, range(start, end + 1))

        return open_ports

    if isinstance(node, AST.WebIndexingNode):
        target = evaluate(node.site)
        objectTofind = evaluate(node.object)
        found = []

        SecurityStuff.WebIndex(target, objectTofind, found)

        return found

    if isinstance(node, AST.SniffingNode):
        iface = evaluate(node.iface)
        count = evaluate(node.count)
        delay = evaluate(node.delay)
        filter = evaluate(node.filter)

        result = []

        SecurityStuff.SniffRun(iface=iface, count=count, delay=delay, filter=filter, list=result)
        
        return result

    raise TypeError(f"Cannot evaluate: {type(node)}")

def interpret(node):
    if isinstance(node, AST.FunctionCallNode):
        if node.name == "out":
            value = evaluate(node.argument[0])
            print(value)
        elif node.name == "in":
            if isinstance(node.argument[0], AST.Variable):
                user_input = input()
                env_stack[-1][node.argument[0].name] = user_input
        elif node.name in funcEnv:
            return call_function(node)

        elif node.name == "append":
            if len(node.argument) < 2:
                print("append() should atleast have 2 arguments", file=sys.stderr)
            else:
                container = evaluate(node.argument[0])

                if isinstance(container, list):
                    if len(node.argument) != 2:
                        print("For list append, you should have 2 arguments", file=sys.stderr)
                    value = evaluate(node.argument[1])
                    container.append(value)

                elif isinstance(container, dict):
                    if len(node.argument) != 3:
                        print("For Dict append, you should have 3 arguments (key and value)", file=sys.stderr)
                    key = evaluate(node.argument[1])
                    value = evaluate(node.argument[2])
                    container[key] = value

                else:
                    print(f"Can't append on {container}, not list or dict format", file=sys.stderr)
        else:
            print(f"Unknown function: {node.name}", file=sys.stderr)

    elif isinstance(node, AST.LetNode):
        value = evaluate(node.value)
        env_stack[-1][node.name] = value

    elif isinstance(node, AST.IfNode):
        cond_value = evaluate(node.condition)

        if cond_value:
            for stmt in node.then_body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result
        elif node.else_body is not None:
            for stmt in node.else_body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, AST.ForLoopNode):
        start_val = evaluate(node.start)
        end_val = evaluate(node.end)

        for i in range(start_val, end_val + 1):
            env_stack[-1][node.var_name] = i
            for stmt in node.body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, AST.ForItemLoopNode):
        list_name = env_stack[-1][node.list_name]

        for item in list_name:
            env_stack[-1][node.var_name] = item
            for stmt in node.body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, AST.WhileLoopNode):
        while evaluate(node.condition):
            for stmt in node.body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, AST.FunctionNode):
        funcEnv[node.name] = node

    elif isinstance(node, AST.ReturnNode):
        value = evaluate(node.value)
        return("RETURN", value)
    
    else:
        print(f"Unknown node type: {type(node)}", file=sys.stderr)