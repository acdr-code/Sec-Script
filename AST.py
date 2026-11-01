from lark import Transformer
from lark import v_args


# ====================== Nodes ======================

#father
class ASTNODE:
    def __init__(self, line=None):
        self.line = line


class FunctionCallNode(ASTNODE):
    def __init__(self, name, argument, line=None):
        super().__init__(line)
        self.name = name
        self.argument = argument


class LetNode(ASTNODE):
    def __init__(self, name, value, line=None):
        super().__init__(line)
        self.name = name
        self.value = value


class IfNode(ASTNODE):
    def __init__(self, condition, then_body, else_body=None, line=None):
        super().__init__(line)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body


class BinaryOpNode(ASTNODE):
    def __init__(self, left, op, right, line=None):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class StringLiteral(ASTNODE):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value


class IntLiteral(ASTNODE):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value

class FloatLiteral(ASTNODE):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value

class BooleanLiteral(ASTNODE):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value


class Variable(ASTNODE):
    def __init__(self, name, line=None):
        super().__init__(line)
        self.name = name


class ListNode(ASTNODE):
    def __init__(self, elements, line=None):
        super().__init__(line)
        self.elements = elements


class DictNode(ASTNODE):
    def __init__(self, pairs, line=None):
        super().__init__(line)
        self.pairs = pairs


class IndexingNode(ASTNODE):
    def __init__(self, container, index, line=None):
        super().__init__(line)
        self.container = container
        self.index = index


class ForLoopNode(ASTNODE):
    def __init__(self, var_name, start, end, body, line=None):
        super().__init__(line)
        self.var_name = var_name
        self.start = start
        self.end = end
        self.body = body


class ForItemLoopNode(ASTNODE):
    def __init__(self, var_name, list_name, body, line=None):
        super().__init__(line)
        self.var_name = var_name
        self.list_name = list_name
        self.body = body


class WhileLoopNode(ASTNODE):
    def __init__(self, condition, body, line=None):
        super().__init__(line)
        self.condition = condition
        self.body = body


class FunctionNode(ASTNODE):
    def __init__(self, name, parametrs, body, line=None):
        super().__init__(line)
        self.name = name
        self.parametrs = parametrs
        self.body = body


class ReturnNode(ASTNODE):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value


class PortScanNode(ASTNODE):
    def __init__(self, ip, start, end, timeout, line=None):
        super().__init__(line)
        self.ip = ip
        self.start = start
        self.end = end
        self.timeout = timeout


class WebIndexingNode(ASTNODE):
    def __init__(self, object, site, line=None):
        super().__init__(line)
        self.object = object
        self.site = site


class SniffingNode(ASTNODE):
    def __init__(self, iface, count, filter, delay, line=None):
        super().__init__(line)
        self.iface = iface
        self.count = count
        self.filter = filter
        self.delay = delay


class ShellNode(ASTNODE):
    def __init__(self, target, password, port, body, line=None):
        super().__init__(line)
        self.target = target
        self.password = password
        self.port = port
        self.body = body


class ShellRunNode(ASTNODE):
    def __init__(self, command, line=None):
        super().__init__(line)
        self.command = command


class ImportNode(ASTNODE):
    def __init__(self, file, line=None):
        super().__init__(line)
        self.file = file

class DnsNode(ASTNODE):
    def __init__(self, ip, record, line=None):
        super().__init__(line)
        self.ip = ip
        self.record = record

class TslCertCheckNode(ASTNODE):
    def __init__(self, ip, timeout, line=None):
        super().__init__(line)
        self.ip = ip
        self.timeout = timeout

class ArpScanNode(ASTNODE):
    def __init__(self, ip, iface, timeout, line=None):
        super().__init__(line)
        self.ip = ip
        self.iface = iface
        self.timeout = timeout

class BannerGrabbingNode(ASTNODE):
    def __init__(self, ip, port, timeout, line=None):
        super().__init__(line)
        self.ip = ip
        self.port = port
        self.timeout = timeout

#file-stuff
class SimpleWriteNode(ASTNODE):
    def __init__(self, container, file, line=None):
        super().__init__(line)
        self.container = container
        self.file = file

class WriteEndNode(ASTNODE):
    def __init__(self, container, file, line=None):
        super().__init__(line)
        self.container = container
        self.file = file

class SimpleReadNode(ASTNODE):
    def __init__(self, file, line=None):
        super().__init__(line)
        self.file = file

class ReadLinesNode(ASTNODE):
    def __init__(self, file, line=None):
        super().__init__(line)
        self.file = file

class FileExistsNode(ASTNODE):
    def __init__(self, file, line=None):
        super().__init__(line)
        self.file = file

#-----------------------

# ====================== Transformer ======================

@v_args(meta=True)
class ASTBuilder(Transformer):

    def start(self, meta, items):
        return items

    def statement(self, meta, items):
        return items[0]

    def expr(self, meta, items):
        return items[0]

    def func_call(self, meta, items):
        name = items[0].name
        arguments = items[1]
        return FunctionCallNode(name, arguments, line=meta.line)

    def args(self, meta, items):
        values = []
        for item in items:
            values.append(item)
        return values

    def let_stmt(self, meta, items):
        name = items[0].name
        value = items[1]
        return LetNode(name, value, line=meta.line)

    def list(self, meta, items):
        values = items[:]
        return ListNode(values, line=meta.line)

    def pair(self, meta, items):
        key = str(items[0].name)
        value = items[1]
        return (key, value)

    def dict(self, meta, items):
        pairs = items[:]
        seen = set()

        for key, value in pairs:
            if key in seen:
                raise Exception(f"Key {key} is written more than 1 time")
            seen.add(key)

        return DictNode(pairs, line=meta.line)

    def index_access(self, meta, items):
        name = items[0].name
        value = items[1]
        return IndexingNode(name, value, line=meta.line)

    def if_stmt(self, meta, items):
        condition = items[0]
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else None
        return IfNode(condition, then_body, else_body, line=meta.line)

    def for_stmt(self, meta, items):
        var_name = items[0].name
        start = items[1]
        end = items[2]
        body = items[3:]
        return ForLoopNode(var_name, start, end, body, line=meta.line)

    def foreach_stmt(self, meta, items):
        var_name = items[0].name
        list_name = items[1].name
        body = items[2:]
        return ForItemLoopNode(var_name, list_name, body, line=meta.line)

    def while_stmt(self, meta, items):
        condition = items[0]
        body = items[1:]
        return WhileLoopNode(condition, body, line=meta.line)

    def function_stmt(self, meta, items):
        name = items[0].name
        parametrs = items[1]
        body = items[2:]
        return FunctionNode(name, parametrs, body, line=meta.line)

    def params(self, meta, items):
        values = []
        for item in items:
            values.append(item.name)
        return values

    def return_stmt(self, meta, items):
        return ReturnNode(items[0], line=meta.line)

    def import_stmt(self, meta, items):
        path = items[0].value
        return ImportNode(path, line=meta.line)

    def scan_stmt(self, meta, items):
        ip = items[0]
        start = items[1]
        end = items[2]
        timeout = items[3]
        return PortScanNode(ip, start, end, timeout, line=meta.line)

    def webindex_stmt(self, meta, items):
        object = items[0]
        site = items[1]
        return WebIndexingNode(object, site, line=meta.line)

    def sniffing_stmt(self, meta, items):
        iface = items[0]
        count = items[1]
        filter = items[2]
        delay = items[3]
        return SniffingNode(iface=iface, count=count, filter=filter, delay=delay, line=meta.line)

    def shell_stmt(self, meta, items):
        target = items[0]
        password = items[1]
        port = items[2]
        body = items[3:]
        return ShellNode(target, password, port, body, line=meta.line)

    def dns(self, meta, items):
            ipObj = items[0]
            recordObj = items[1]
            return DnsNode(ip=ipObj, record=recordObj, line=meta.line)
    
    def check_cert(self, meta, items):
        ipObj = items[0]
        timeOut = items[1]
        return TslCertCheckNode(ip=ipObj, line=meta.line, timeout=timeOut)

    def run_ing(self, meta, items):
        command = items[0]
        return ShellRunNode(command, line=meta.line)

    def arpscan(self, meta, items):
        ip = items[0]
        iface = items[1]
        timeout = items[2]
        return ArpScanNode(ip=ip, iface=iface, timeout=timeout, line=meta.line)

    def banner_grab(self, meta, items):
        ip = items[0]
        port = items[1]
        timeout = items[2]
        return BannerGrabbingNode(ip=ip, timeout=timeout, port=port, line=meta.line)

    #file-stuff
    def write(self, meta, items):
        container = items[0]
        fileName = items[1]
        return SimpleWriteNode(container=container, file=fileName, line=meta.line)

    def writeend(self, meta, items):
        container = items[0]
        fileName = items[1]
        return WriteEndNode(container=container, file=fileName, line=meta.line)

    def read(self, meta, items):
        fileName = items[0]
        return SimpleReadNode(file=fileName, line=meta.line)

    def readlines(self, meta, items):
        fileName = items[0]
        return ReadLinesNode(file=fileName, line=meta.line)

    def exists(self, meta, items):
        fileName = items[0]
        return FileExistsNode(file=fileName, line=meta.line)

    #-----------------------

    def comparison(self, meta, items):
        left, op, right = items
        return BinaryOpNode(left, str(op), right, line=meta.line)

    def math_ing(self, meta, items):
        left, op, right = items
        return BinaryOpNode(left, op, right, line=meta.line)

    def connect_ing(self, meta, items):
        left, op, right = items
        return BinaryOpNode(left, op, right, line=meta.line)

    def atom(self, meta, items):
        return items[0]

    # ---------- Literals & Variable ----------

    def ESCAPED_STRING(self, token):
        return StringLiteral(str(token)[1:-1], line=token.line)

    def INT_NUMBER(self, token):
        text = str(token)
        value = int(text)
        return IntLiteral(value, line=token.line)

    def FLOAT_NUMBER(self, token):
        text = str(token)
        value = float(text)
        return FloatLiteral(value, line=token.line)

    def TRUE(self, token):
        return BooleanLiteral(True, line=token.line)

    def FALSE(self, token):
        return BooleanLiteral(False, line=token.line)

    def NAME(self, token):
        return Variable(str(token), line=token.line)