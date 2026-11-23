from lark import Transformer
from lark import v_args
from . import ASTNode

#Build

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
        return ASTNode.FunctionCallNode(name, arguments, line=meta.line)

    def args(self, meta, items):
        values = []
        for item in items:
            values.append(item)
        return values

    def let_stmt(self, meta, items):
        name = items[0].name
        value = items[1]
        return ASTNode.LetNode(name, value, line=meta.line)

    def list(self, meta, items):
        values = items[:]
        return ASTNode.ListNode(values, line=meta.line)

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

        return ASTNode.DictNode(pairs, line=meta.line)

    def index_access(self, meta, items):
        name = items[0].name
        value = items[1]
        return ASTNode.IndexingNode(name, value, line=meta.line)

    def if_stmt(self, meta, items):
        condition = items[0]
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else None
        return ASTNode.IfNode(condition, then_body, else_body, line=meta.line)

    def for_stmt(self, meta, items):
        var_name = items[0].name
        start = items[1]
        end = items[2]
        body = items[3:]
        return ASTNode.ForLoopNode(var_name, start, end, body, line=meta.line)

    def foreach_stmt(self, meta, items):
        var_name = items[0].name
        list_name = items[1].name
        body = items[2:]
        return ASTNode.ForItemLoopNode(var_name, list_name, body, line=meta.line)

    def while_stmt(self, meta, items):
        condition = items[0]
        body = items[1:]
        return ASTNode.WhileLoopNode(condition, body, line=meta.line)

    def function_stmt(self, meta, items):
        name = items[0].name
        parametrs = items[1]
        body = items[2:]
        return ASTNode.FunctionNode(name, parametrs, body, line=meta.line)

    def params(self, meta, items):
        values = []
        for item in items:
            values.append(item.name)
        return values

    def return_stmt(self, meta, items):
        return ASTNode.ReturnNode(items[0], line=meta.line)

    def import_stmt(self, meta, items):
        path = items[0].value
        return ASTNode.ImportNode(path, line=meta.line)

    def scan_stmt(self, meta, items):
        ip = items[0]
        start = items[1]
        end = items[2]
        timeout = items[3]
        return ASTNode.PortScanNode(ip, start, end, timeout, line=meta.line)

    def webindex_stmt(self, meta, items):
        object = items[0]
        site = items[1]
        return ASTNode.WebIndexingNode(object, site, line=meta.line)

    def sniffing_stmt(self, meta, items):
        iface = items[0]
        count = items[1]
        filter = items[2]
        delay = items[3]
        return ASTNode.SniffingNode(iface=iface, count=count, filter=filter, delay=delay, line=meta.line)

    def shell_stmt(self, meta, items):
        target = items[0]
        password = items[1]
        port = items[2]
        body = items[3:]
        return ASTNode.ShellNode(target, password, port, body, line=meta.line)

    def dns(self, meta, items):
            ipObj = items[0]
            recordObj = items[1]
            return ASTNode.DnsNode(ip=ipObj, record=recordObj, line=meta.line)
    
    def check_cert(self, meta, items):
        ipObj = items[0]
        timeOut = items[1]
        return ASTNode.TslCertCheckNode(ip=ipObj, line=meta.line, timeout=timeOut)

    def run_ing(self, meta, items):
        command = items[0]
        return ASTNode.ShellRunNode(command, line=meta.line)

    def arpscan(self, meta, items):
        ip = items[0]
        iface = items[1]
        timeout = items[2]
        return ASTNode.ArpScanNode(ip=ip, iface=iface, timeout=timeout, line=meta.line)

    def banner_grab(self, meta, items):
        ip = items[0]
        port = items[1]
        timeout = items[2]
        return ASTNode.BannerGrabbingNode(ip=ip, timeout=timeout, port=port, line=meta.line)

    #file-stuff
    def write(self, meta, items):
        container = items[0]
        fileName = items[1]
        return ASTNode.SimpleWriteNode(container=container, file=fileName, line=meta.line)

    def writeend(self, meta, items):
        container = items[0]
        fileName = items[1]
        return ASTNode.WriteEndNode(container=container, file=fileName, line=meta.line)

    def read(self, meta, items):
        fileName = items[0]
        return ASTNode.SimpleReadNode(file=fileName, line=meta.line)

    def readlines(self, meta, items):
        fileName = items[0]
        return ASTNode.ReadLinesNode(file=fileName, line=meta.line)

    def exists(self, meta, items):
        fileName = items[0]
        return ASTNode.FileExistsNode(file=fileName, line=meta.line)

    #-----------------------

    def comparison(self, meta, items):
        left, op, right = items
        return ASTNode.BinaryOpNode(left, str(op), right, line=meta.line)

    def math_ing(self, meta, items):
        left, op, right = items
        return ASTNode.BinaryOpNode(left, op, right, line=meta.line)

    def connect_ing(self, meta, items):
        left, op, right = items
        return ASTNode.BinaryOpNode(left, op, right, line=meta.line)

    def atom(self, meta, items):
        return items[0]

    # ---------- Literals & Variable ----------

    def ESCAPED_STRING(self, token):
        return ASTNode.StringLiteral(str(token)[1:-1], line=token.line)

    def INT_NUMBER(self, token):
        text = str(token)
        value = int(text)
        return ASTNode.IntLiteral(value, line=token.line)

    def FLOAT_NUMBER(self, token):
        text = str(token)
        value = float(text)
        return ASTNode.FloatLiteral(value, line=token.line)

    def TRUE(self, token):
        return ASTNode.BooleanLiteral(True, line=token.line)

    def FALSE(self, token):
        return ASTNode.BooleanLiteral(False, line=token.line)

    def NAME(self, token):
        return ASTNode.Variable(str(token), line=token.line)