import AST
import sys
from concurrent.futures import ThreadPoolExecutor
import SecurityStuff
from scapy.all import get_if_list
import subprocess
from errorHandler import SecScriptError
import time
from datetime import datetime, timezone
from convertTypes import convert
import fileHandel
import os
from pathResolver import resolve_path
import os
from Grammar import parser
from AST import ASTBuilder

imported_files = set()
dir_stack = []

def run_file(filepath):
    abs_path = os.path.abspath(filepath)

    if abs_path in imported_files:
        return
    imported_files.add(abs_path)

    with open(abs_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(code)
    ast_statements = ASTBuilder().transform(tree)

    is_main = (len(dir_stack) == 0)
    env_stack[-1]["__name__"] = "main" if is_main else "imported"

    dir_stack.append(os.path.dirname(abs_path))
    try:
        for stmt in ast_statements:
            interpret(stmt)
    finally:
        dir_stack.pop()

#interpreter starts
env_stack = [{}]
funcEnv = {}
ssh_sessions = []

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

    if isinstance(node, AST.IntLiteral):
        return node.value

    if isinstance(node, AST.FloatLiteral):
        return node.value

    if isinstance(node, AST.BooleanLiteral):
        return node.value

    if isinstance(node, AST.Variable):
        if node.name in env_stack[-1]:
            return env_stack[-1][node.name]
        raise SecScriptError(f"Variable '{node.name}' is not defined", line=node.line)

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
        if op == "/":
            if right == 0:
                raise SecScriptError("Division by zero", line=node.line)
            return left / right
        if op == "*": return left * right
        if op == "&": return str(left) + str(right)

        raise SecScriptError(f"Unknown operator '{op}'", line=node.line)

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
        if node.container not in env_stack[-1]:
            raise SecScriptError(f"Variable '{node.container}' is not defined", line=node.line)
        actualName = env_stack[-1][node.container]
        index = evaluate(node.index)
        try:
            return actualName[index]
        except (KeyError, IndexError):
            raise SecScriptError(f"Index/key '{index}' not found in '{node.container}'", line=node.line)

    if isinstance(node, AST.FunctionCallNode):
        #user built
        if node.name in funcEnv:
            return call_function(node)

        #built-in(s)
        #hashing
        hashResult = SecurityStuff.hedIt(node)
        if hashResult is not None:
            return hashResult

        #http request - response
        httpRequestResult = SecurityStuff.httpRequest(node)
        if httpRequestResult is not None:
            return httpRequestResult

        #type change
        typechangeResult = convert(node)
        if typechangeResult is not None:
            return typechangeResult

        #in function
        if node.name == "in":
            user_input = input(evaluate(node.argument[0]))
            return user_input

        #dict, list -- length
        if node.name == "length":
            container = evaluate(node.argument[0])
            return len(container)

        #get iface
        if node.name == "getMyIfaces":
            return get_if_list()

        #get ip
        if node.name == "getMyIp":
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
            return result.stdout

        #get uersname
        if node.name == "myusrname":
            result = subprocess.run(["whoami"], capture_output=True, text=True, check=True)
            return result.stdout

        #get netinfo
        if node.name == "netInfo":
            result = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True)
            return result.stdout

        #time elements
        if node.name == "localtime":
            return datetime.now()

        if node.name == "utctime":
            return datetime.now(timezone.utc)

        if node.name == "unixtime":
            return time.time()

        raise SecScriptError(f"Cannot evaluate function: {node.name}", line=node.line)

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

    if isinstance(node, AST.ShellRunNode):
        if not ssh_sessions:
            raise SecScriptError("run statement is used outside of connecting function", line=node.line)

        client = ssh_sessions[-1]
        command = evaluate(node.command)

        return SecurityStuff.RunSsh(client=client, command=command)

    if isinstance(node, AST.FileExistsNode):
        return fileHandel.FileExists(resolve_path(node))

    if isinstance(node, AST.SimpleReadNode):
        return fileHandel.WholeFileRead(resolve_path(node))

    if isinstance(node, AST.ReadLinesNode):
        return fileHandel.LineFileRead(resolve_path(node))

    if isinstance(node, AST.DnsNode):
        return SecurityStuff.dnsRecords(node)

    if isinstance(node, AST.TslCertCheckNode):
        host = evaluate(node.ip)
        timeout = evaluate(node.timeout)
        try:
            return SecurityStuff.TlsCertCheck(host, timeout)
        except OSError as e:
            raise SecScriptError(str(e), line=node.line)

    raise SecScriptError(f"Cannot evaluate: {type(node).__name__}", line=getattr(node, "line", None))


def interpret(node):
    if isinstance(node, AST.FunctionCallNode):
        if node.name == "append":
            if len(node.argument) < 2:
                raise SecScriptError("append() should have at least 2 arguments", line=node.line)

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                if len(node.argument) != 2:
                    raise SecScriptError("For list append, you should have 2 arguments", line=node.line)
                value = evaluate(node.argument[1])
                container.append(value)

            elif isinstance(container, dict):
                if len(node.argument) != 3:
                    raise SecScriptError("For dict append, you should have 3 arguments (key and value)", line=node.line)
                key = evaluate(node.argument[1])
                value = evaluate(node.argument[2])
                container[key] = value

            else:
                raise SecScriptError(f"Can't append on '{container}', not list or dict format", line=node.line)

        elif node.name == "remove":
            if len(node.argument) != 2:
                raise SecScriptError("remove() should have only 2 arguments", line=node.line)

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                value = evaluate(node.argument[1])
                container.remove(value)

            elif isinstance(container, dict):
                keyValue = evaluate(node.argument[1])
                del container[keyValue]

            else:
                raise SecScriptError(f"Can't append on '{container}', not list or dict format", line=node.line)

        elif node.name == "clear":
            if len(node.argument) != 1:
                raise SecScriptError("clear() function only gets one argument", line=node.line)

            container = evaluate(node.argument[0])

            if isinstance(container, dict):
                container.clear()

            elif isinstance(container, list):
                del container[:]

            else:
                raise SecScriptError(f"Can't clear '{container}', not list or dict format", line=node.line)

        elif node.name == "removeLast":
            if len(node.argument) != 1:
                raise SecScriptError("removeLast() function only gets one argument", line=node.line)

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                container.pop()

            else:
                raise SecScriptError(f"Can't removeList '{container}', not list format", line=node.line)\
                
        elif node.name == "out":
            if len(node.argument) > 0:
                value = evaluate(node.argument[0])
            else:
                value = ""
            print(value)
        
        elif node.name in funcEnv:
            return call_function(node)

        elif node.name == "length":
            if len(node.argument) != 1:
                raise SecScriptError("length() only gets 1 argument", line=node.line)

            container = evaluate(node.argument[0])

            if isinstance(container, list) or isinstance(container, dict):
                return len(container)

            else:
                raise SecScriptError(f"Can't get length of '{container}', not list or dict format", line=node.line)

        elif node.name in ("hash", "encode", "decode"):
            SecurityStuff.hedIt(node)

        elif node.name in ("string", "float", "bool", "int"):
            convert(node)

        elif node.name == "httpRequest":
            SecurityStuff.httpRequest(node)
        
        else:
            raise SecScriptError(f"Unknown function: {node.name}", line=node.line)

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
        if node.list_name not in env_stack[-1]:
            raise SecScriptError(f"Variable '{node.list_name}' is not defined", line=node.line)
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
        return ("RETURN", value)

    elif isinstance(node, AST.ImportNode):
        filename = node.file
        current_dir = dir_stack[-1] if dir_stack else os.getcwd()
        target_path = os.path.join(current_dir, filename)
        run_file(target_path)

    elif isinstance(node, AST.ShellNode):
        target = evaluate(node.target)
        password = evaluate(node.password)
        port = evaluate(node.port)

        client = SecurityStuff.ConnectSsh(target=target, password=password, port=port)
        ssh_sessions.append(client)

        try:
            for stmt in node.body:
                result = interpret(stmt)
                if result is not None and result[0] == "RETURN":
                    return result
        finally:
            SecurityStuff.CloseSsh(client)
            ssh_sessions.pop()

    elif isinstance(node, AST.SimpleWriteNode):
        try:
            path = resolve_path(node)
            writeObject = evaluate(node.container)

            return fileHandel.FileWrite(path=path, writeObj=writeObject, mode="w")

        except Exception:
            raise SecScriptError(f"Error while requesting to write the file at path -> {path}", line=node.line)

    elif isinstance(node, AST.WriteEndNode):
        try:
            path = resolve_path(node)
            writeObject = evaluate(node.container)

            return fileHandel.FileWrite(path=path, mode="a", writeObj=writeObject)

        except Exception:
            raise SecScriptError(f"Error while requesting to write the file at path -> {path}", line=node.line)

    else:
        raise SecScriptError(f"Unknown node type: {type(node).__name__}", line=getattr(node, "line", None))