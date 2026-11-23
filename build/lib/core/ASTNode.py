#Nodes

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