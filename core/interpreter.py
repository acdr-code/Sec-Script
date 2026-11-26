from . import ASTNode
from . import ASTBuild
from concurrent.futures import ThreadPoolExecutor
from security import SecurityStuff
from scapy.all import get_if_list
import subprocess
from .errorHandler import (
    SecScriptError, SecsNameError, SecsRuntimeError,
    SecsTypeError, SecsArgumentError, SecsSyntaxError,
    SecsBuilderError
)
from lark.exceptions import (
    UnexpectedCharacters, UnexpectedEOF,
    UnexpectedToken, VisitError
)
import time
from datetime import datetime, timezone
from utills.convertTypes import convert
from fileio import fileHandel
import os
from fileio.pathResolver import resolve_path
from .Grammar import parser


imported_files = set()
loading_files = set()
dir_stack = []


def run_file(filepath):
    abs_path = os.path.abspath(filepath)

    if abs_path in imported_files or abs_path in loading_files:
        return

    loading_files.add(abs_path)

    try:
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                code = f.read()

        except (OSError, UnicodeError) as e:
            raise SecsRuntimeError(
                f"Could not read SecScript file '{abs_path}': {e}"
            ) from e

        try:
            tree = parser.parse(code)
            ast_statements = ASTBuild.ASTBuilder().transform(tree)

        except UnexpectedCharacters as e:
            raise SecsSyntaxError(
                f"Unexpected character: '{e.char}'",
                line=e.line
            ) from e

        except UnexpectedToken as e:
            raise SecsSyntaxError(
                f"Unexpected token: '{e.token}'",
                line=e.line
            ) from e

        except UnexpectedEOF as e:
            raise SecsSyntaxError(
                "Unexpected end of file",
                line=e.line
            ) from e

        except VisitError as e:
            raise SecsBuilderError(
                f"Error in Building AST: {e.orig_exc}",
                line=getattr(e.obj, "line", None)
            ) from e.orig_exc

        is_main = (len(dir_stack) == 0)
        env_stack[-1]["__name__"] = "main" if is_main else "imported"

        dir_stack.append(os.path.dirname(abs_path))

        try:
            for stmt in ast_statements:
                interpret(stmt)

            imported_files.add(abs_path)

        finally:
            dir_stack.pop()

    finally:
        loading_files.discard(abs_path)


# Interpreter starts
env_stack = [{}]
funcEnv = {}
ssh_sessions = []


def check_argument_count(node, expected):
    if len(node.argument) != expected:
        raise SecsArgumentError(
            f"{node.name}() expects exactly {expected} argument(s)",
            line=node.line
        )


def get_container_length(container, node):
    if not isinstance(container, (list, dict)):
        raise SecsTypeError(
            f"Can't get length of '{container}', not list or dict format",
            line=node.line
        )

    return len(container)


def call_function(node):
    func_def = funcEnv[node.name]

    if len(node.argument) != len(func_def.parametrs):
        raise SecsArgumentError(
            f"Function '{node.name}' expects {len(func_def.parametrs)} "
            f"argument(s), got {len(node.argument)}",
            line=node.line
        )

    new_scope = {}

    for i in range(len(func_def.parametrs)):
        param_name = func_def.parametrs[i]
        arg_value = evaluate(node.argument[i])
        new_scope[param_name] = arg_value

    env_stack.append(new_scope)

    try:
        return_value = None

        for stmt in func_def.body:
            result = interpret(stmt)

            if result is not None and result[0] == "RETURN":
                return_value = result[1]
                break

        return return_value

    finally:
        env_stack.pop()


def evaluate(node):
    if isinstance(node, ASTNode.StringLiteral):
        return node.value

    if isinstance(node, ASTNode.IntLiteral):
        return node.value

    if isinstance(node, ASTNode.FloatLiteral):
        return node.value

    if isinstance(node, ASTNode.BooleanLiteral):
        return node.value

    if isinstance(node, ASTNode.Variable):
        if node.name in env_stack[-1]:
            return env_stack[-1][node.name]

        raise SecsNameError(
            f"Variable '{node.name}' is not defined",
            line=node.line
        )

    if isinstance(node, ASTNode.BinaryOpNode):
        left = evaluate(node.left)
        right = evaluate(node.right)
        op = node.op

        try:
            if op == "==":
                return left == right

            if op == "!=":
                return left != right

            if op == "<":
                return left < right

            if op == ">":
                return left > right

            if op == "<=":
                return left <= right

            if op == ">=":
                return left >= right

            if op == "+":
                return left + right

            if op == "-":
                return left - right

            if op == "/":
                return left / right

            if op == "*":
                return left * right

            if op == "&":
                return str(left) + str(right)

        except TypeError as e:
            raise SecsTypeError(
                "Two arguments have incompatible types",
                line=node.line
            ) from e

        except ZeroDivisionError as e:
            raise SecsRuntimeError(
                "Division by zero",
                line=node.line
            ) from e

        raise SecsRuntimeError(
            f"Unknown operator '{op}'",
            line=node.line
        )

    if isinstance(node, ASTNode.ListNode):
        listEnv = []

        for element in node.elements:
            listEnv.append(evaluate(element))

        return listEnv

    if isinstance(node, ASTNode.DictNode):
        dictEnv = {}

        for key, valueNode in node.pairs:
            dictEnv[key] = evaluate(valueNode)

        return dictEnv

    if isinstance(node, ASTNode.IndexingNode):
        if node.container not in env_stack[-1]:
            raise SecsNameError(
                f"Variable '{node.container}' is not defined",
                line=node.line
            )

        actualName = env_stack[-1][node.container]
        index = evaluate(node.index)

        try:
            return actualName[index]

        except TypeError as e:
            raise SecsTypeError(
                f"Cannot use index '{index}' on this value",
                line=node.line
            ) from e

        except (KeyError, IndexError) as e:
            raise SecsRuntimeError(
                f"Index/key '{index}' not found in '{node.container}'",
                line=node.line
            ) from e

    if isinstance(node, ASTNode.FunctionCallNode):
        # User-built functions
        if node.name in funcEnv:
            return call_function(node)

        # Built-in functions
        # Hashing
        hashResult = SecurityStuff.hedIt(node)

        if hashResult is not None:
            return hashResult

        # HTTP request - response
        httpRequestResult = SecurityStuff.httpRequest(node)

        if httpRequestResult is not None:
            return httpRequestResult

        # Type change
        typechangeResult = convert(node)

        if typechangeResult is not None:
            return typechangeResult

        # Input
        if node.name == "in":
            check_argument_count(node, 1)

            try:
                return input(evaluate(node.argument[0]))

            except EOFError as e:
                raise SecsRuntimeError(
                    "Input stream ended unexpectedly",
                    line=node.line
                ) from e

        # Length
        if node.name == "length":
            check_argument_count(node, 1)

            container = evaluate(node.argument[0])
            return get_container_length(container, node)

        # Get interfaces
        if node.name == "getMyIfaces":
            check_argument_count(node, 0)
            return get_if_list()

        # Get IP
        if node.name == "getMyIp":
            check_argument_count(node, 0)

            try:
                result = subprocess.run(
                    ["hostname", "-I"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                return result.stdout

            except FileNotFoundError as e:
                raise SecsRuntimeError(
                    "hostname command is not available on this system",
                    line=node.line
                ) from e

            except subprocess.CalledProcessError as e:
                raise SecsRuntimeError(
                    "hostname command failed",
                    line=node.line
                ) from e

            except OSError as e:
                raise SecsRuntimeError(
                    f"Could not execute hostname command: {e}",
                    line=node.line
                ) from e

        # Get username
        if node.name == "myusrname":
            check_argument_count(node, 0)

            try:
                result = subprocess.run(
                    ["whoami"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                return result.stdout

            except FileNotFoundError as e:
                raise SecsRuntimeError(
                    "whoami command is not available on this system",
                    line=node.line
                ) from e

            except subprocess.CalledProcessError as e:
                raise SecsRuntimeError(
                    "whoami command failed",
                    line=node.line
                ) from e

            except OSError as e:
                raise SecsRuntimeError(
                    f"Could not execute whoami command: {e}",
                    line=node.line
                ) from e

        # Get network info
        if node.name == "netInfo":
            check_argument_count(node, 0)

            try:
                result = subprocess.run(
                    ["ip", "a"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                return result.stdout

            except FileNotFoundError as e:
                raise SecsRuntimeError(
                    "ip command is not available on this system",
                    line=node.line
                ) from e

            except subprocess.CalledProcessError as e:
                raise SecsRuntimeError(
                    "ip command failed",
                    line=node.line
                ) from e

            except OSError as e:
                raise SecsRuntimeError(
                    f"Could not execute ip command: {e}",
                    line=node.line
                ) from e

        # Time elements
        if node.name == "localtime":
            check_argument_count(node, 0)
            return datetime.now()

        if node.name == "utctime":
            check_argument_count(node, 0)
            return datetime.now(timezone.utc)

        if node.name == "unixtime":
            check_argument_count(node, 0)
            return time.time()

        # IP-network elements
        if node.name == "ipValidity":
            return SecurityStuff.ipValidity(
                evaluate(node.argument[0]),
                line=node.line
            )

        if node.name == "ipVer":
            return SecurityStuff.ipversion(
                evaluate(node.argument[0]),
                line=node.line
            )

        if node.name == "ipfirstUseAddr":
            return SecurityStuff.firstUsableaddr(
                evaluate(node.argument[0]),
                line=node.line
            )

        if node.name == "ipRange":
            return SecurityStuff.networkRange(
                evaluate(node.argument[0]),
                line=node.line
            )

        if node.name == "ipUseRangeNum":
            return SecurityStuff.networkUsableNum(
                evaluate(node.argument[0]),
                line=node.line
            )

        # HTTP elements
        if node.name == "redirectInspect":
            return SecurityStuff.redirectInspect(
                *(evaluate(arg) for arg in node.argument),
                node.line
            )

        if node.name == "cookieInspect":
            return SecurityStuff.cookie(
                *(evaluate(arg) for arg in node.argument),
                node.line
            )

        raise SecsNameError(
            f"Cannot evaluate function: {node.name}",
            line=node.line
        )

    if isinstance(node, ASTNode.PortScanNode):
        ip = evaluate(node.ip)
        start = evaluate(node.start)
        end = evaluate(node.end)
        timeout = evaluate(node.timeout)

        if type(start) is not int or type(end) is not int:
            raise SecsTypeError(
                "Port range values must be integers",
                line=node.line
            )

        open_ports = []

        def scan(port):
            SecurityStuff.portScan(ip, port, timeout, open_ports)

        with ThreadPoolExecutor(max_workers=100) as executor:
            list(executor.map(scan, range(start, end + 1)))

        return open_ports

    if isinstance(node, ASTNode.WebIndexingNode):
        target = evaluate(node.site)
        objectTofind = evaluate(node.object)
        found = []

        SecurityStuff.WebIndex(target, objectTofind, found)

        return found

    if isinstance(node, ASTNode.SniffingNode):
        iface = evaluate(node.iface)
        count = evaluate(node.count)
        delay = evaluate(node.delay)
        filter = evaluate(node.filter)

        result = []

        SecurityStuff.SniffRun(
            iface=iface,
            count=count,
            delay=delay,
            filter=filter,
            result=result
        )

        return result

    if isinstance(node, ASTNode.ShellRunNode):
        if not ssh_sessions:
            raise SecsRuntimeError(
                "run statement is used outside of connecting function",
                line=node.line
            )

        client = ssh_sessions[-1]
        command = evaluate(node.command)

        return SecurityStuff.RunSsh(
            client=client,
            command=command
        )

    if isinstance(node, ASTNode.FileExistsNode):
        return fileHandel.FileExists(resolve_path(node))

    if isinstance(node, ASTNode.SimpleReadNode):
        return fileHandel.WholeFileRead(resolve_path(node))

    if isinstance(node, ASTNode.ReadLinesNode):
        return fileHandel.LineFileRead(resolve_path(node))

    if isinstance(node, ASTNode.DnsNode):
        return SecurityStuff.dnsRecords(node)

    if isinstance(node, ASTNode.TslCertCheckNode):
        host = evaluate(node.ip)
        timeout = evaluate(node.timeout)

        try:
            return SecurityStuff.TlsCertCheck(host, timeout)

        except OSError as e:
            raise SecsRuntimeError(
                str(e),
                line=node.line
            ) from e

    if isinstance(node, ASTNode.ArpScanNode):
        ip = evaluate(node.ip)
        iface = evaluate(node.iface)
        timeout = evaluate(node.timeout)

        try:
            return SecurityStuff.arpScannerLan(
                ip=ip,
                iface=iface,
                timeout=timeout
            )

        except SecScriptError:
            raise

    if isinstance(node, ASTNode.BannerGrabbingNode):
        ip = evaluate(node.ip)

        try:
            port = int(evaluate(node.port))
            timeout = int(evaluate(node.timeout))

        except (ValueError, TypeError, OverflowError) as e:
            raise SecsTypeError(
                "Port and timeout must be convertible to integers",
                line=node.line
            ) from e

        return SecurityStuff.grabBanner(
            ip=ip,
            timeout=timeout,
            port=port
        )

    raise SecsRuntimeError(
        f"Cannot evaluate: {type(node).__name__}",
        line=getattr(node, "line", None)
    )


def interpret(node):
    if isinstance(node, ASTNode.FunctionCallNode):

        if node.name == "append":
            if len(node.argument) < 2:
                raise SecsArgumentError(
                    "append() should have at least 2 arguments",
                    line=node.line
                )

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                if len(node.argument) != 2:
                    raise SecsArgumentError(
                        "For list append, you should have 2 arguments",
                        line=node.line
                    )

                value = evaluate(node.argument[1])
                container.append(value)

            elif isinstance(container, dict):
                if len(node.argument) != 3:
                    raise SecsArgumentError(
                        "For dict append, you should have 3 arguments (key and value)",
                        line=node.line
                    )

                key = evaluate(node.argument[1])
                value = evaluate(node.argument[2])

                try:
                    container[key] = value

                except TypeError as e:
                    raise SecsTypeError(
                        "Dictionary key must be hashable",
                        line=node.line
                    ) from e

            else:
                raise SecsTypeError(
                    f"Can't append on '{container}', not list or dict format",
                    line=node.line
                )

        elif node.name == "remove":
            if len(node.argument) != 2:
                raise SecsArgumentError(
                    "remove() should have only 2 arguments",
                    line=node.line
                )

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                value = evaluate(node.argument[1])

                try:
                    container.remove(value)

                except ValueError as e:
                    raise SecsRuntimeError(
                        f"Value '{value}' not found in list",
                        line=node.line
                    ) from e

            elif isinstance(container, dict):
                keyValue = evaluate(node.argument[1])

                try:
                    del container[keyValue]

                except KeyError as e:
                    raise SecsRuntimeError(
                        f"Key '{keyValue}' not found in dictionary",
                        line=node.line
                    ) from e

                except TypeError as e:
                    raise SecsTypeError(
                        "Dictionary key must be hashable",
                        line=node.line
                    ) from e

            else:
                raise SecsTypeError(
                    f"Can't remove from '{container}', not list or dict format",
                    line=node.line
                )

        elif node.name == "clear":
            if len(node.argument) != 1:
                raise SecsArgumentError(
                    "clear() function only gets one argument",
                    line=node.line
                )

            container = evaluate(node.argument[0])

            if isinstance(container, dict):
                container.clear()

            elif isinstance(container, list):
                del container[:]

            else:
                raise SecsTypeError(
                    f"Can't clear '{container}', not list or dict format",
                    line=node.line
                )

        elif node.name == "removeLast":
            if len(node.argument) != 1:
                raise SecsArgumentError(
                    "removeLast() function only gets one argument",
                    line=node.line
                )

            container = evaluate(node.argument[0])

            if isinstance(container, list):
                try:
                    container.pop()

                except IndexError as e:
                    raise SecsRuntimeError(
                        "Cannot remove last item from an empty list",
                        line=node.line
                    ) from e

            else:
                raise SecsTypeError(
                    f"Can't removeLast '{container}', not list format",
                    line=node.line
                )

        elif node.name == "out":
            if len(node.argument) > 0:
                value = evaluate(node.argument[0])
            else:
                value = ""

            print(value)

        elif node.name in funcEnv:
            return call_function(node)

        elif node.name == "length":
            check_argument_count(node, 1)

            container = evaluate(node.argument[0])
            return get_container_length(container, node)

        elif node.name in ("hash", "encode", "decode"):
            SecurityStuff.hedIt(node)

        elif node.name in ("string", "float", "bool", "int"):
            convert(node)

        elif node.name == "httpRequest":
            SecurityStuff.httpRequest(node)

        else:
            raise SecsNameError(
                f"Unknown function: {node.name}",
                line=node.line
            )

    elif isinstance(node, ASTNode.LetNode):
        value = evaluate(node.value)
        env_stack[-1][node.name] = value

    elif isinstance(node, ASTNode.IfNode):
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

    elif isinstance(node, ASTNode.ForLoopNode):
        start_val = evaluate(node.start)
        end_val = evaluate(node.end)

        try:
            loop_range = range(start_val, end_val + 1)

        except TypeError as e:
            raise SecsTypeError(
                "Start-to-end range values must be integers",
                line=node.line
            ) from e

        for i in loop_range:
            env_stack[-1][node.var_name] = i

            for stmt in node.body:
                result = interpret(stmt)

                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, ASTNode.ForItemLoopNode):
        if node.list_name not in env_stack[-1]:
            raise SecsNameError(
                f"Variable '{node.list_name}' is not defined",
                line=node.line
            )

        list_name = env_stack[-1][node.list_name]

        try:
            iterator = iter(list_name)

        except TypeError as e:
            raise SecsTypeError(
                "Can't loop on chosen item",
                line=node.line
            ) from e

        for item in iterator:
            env_stack[-1][node.var_name] = item

            for stmt in node.body:
                result = interpret(stmt)

                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, ASTNode.WhileLoopNode):
        while evaluate(node.condition):
            for stmt in node.body:
                result = interpret(stmt)

                if result is not None and result[0] == "RETURN":
                    return result

    elif isinstance(node, ASTNode.FunctionNode):
        funcEnv[node.name] = node

    elif isinstance(node, ASTNode.ReturnNode):
        value = evaluate(node.value)
        return ("RETURN", value)

    elif isinstance(node, ASTNode.ImportNode):
        filename = node.file
        current_dir = dir_stack[-1] if dir_stack else os.getcwd()
        target_path = os.path.join(current_dir, filename)

        run_file(target_path)

    elif isinstance(node, ASTNode.ShellNode):
        target = evaluate(node.target)
        password = evaluate(node.password)
        port = evaluate(node.port)

        client = SecurityStuff.ConnectSsh(
            target=target,
            password=password,
            port=port
        )

        ssh_sessions.append(client)

        try:
            for stmt in node.body:
                result = interpret(stmt)

                if result is not None and result[0] == "RETURN":
                    return result

        finally:
            try:
                SecurityStuff.CloseSsh(client)

            finally:
                ssh_sessions.pop()

    elif isinstance(node, ASTNode.SimpleWriteNode):
        try:
            path = resolve_path(node)
            writeObject = evaluate(node.container)

            return fileHandel.FileWrite(
                path=path,
                writeObj=writeObject,
                mode="w"
            )

        except SecScriptError:
            raise

    elif isinstance(node, ASTNode.WriteEndNode):
        try:
            path = resolve_path(node)
            writeObject = evaluate(node.container)

            return fileHandel.FileWrite(
                path=path,
                mode="a",
                writeObj=writeObject
            )

        except SecScriptError:
            raise

    else:
        raise SecsRuntimeError(
            f"Unknown node type: {type(node).__name__}",
            line=getattr(node, "line", None)
        )
