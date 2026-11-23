import hashlib, base64, urllib.parse
from core.errorHandler import SecScriptError

# hashing
#hashing algors
HASH_FUNCS = {
    "md5": lambda s: hashlib.md5(s.encode()).hexdigest(),
    "sha1": lambda s: hashlib.sha1(s.encode()).hexdigest(),
    "sha256": lambda s: hashlib.sha256(s.encode()).hexdigest(),
    "sha512": lambda s: hashlib.sha512(s.encode()).hexdigest(),
}

ENCODE_FUNCS = {
    "base64": lambda s: base64.b64encode(s.encode()).decode(),
    "hex": lambda s: s.encode().hex(),
    "url": lambda s: urllib.parse.quote(s),
}

DECODE_FUNCS = {
    "base64": lambda s: base64.b64decode(s.encode()).decode(),
    "hex": lambda s: bytes.fromhex(s).decode(),
    "url": lambda s: urllib.parse.unquote(s),
}

#main func
def hedIt(node):
    if node.name == "hash":
        if len(node.argument) != 2:
            raise SecScriptError("hash should have only 2 arguments", line=node.line)

        from core.interpreter import evaluate
        algo = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(algo, str):
            raise SecScriptError("algorithm should be in string format", line=node.line)
        if algo not in HASH_FUNCS:
            raise SecScriptError(f"Unknows hash algorithm: {algo}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string format", line=node.line)

        return HASH_FUNCS[algo](data)

    elif node.name == "encode":
        if len(node.argument) != 2:
            raise SecScriptError("encode should have only 2 arguments", line=node.line)

        from core.interpreter import evaluate
        fmt = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(fmt, str):
            raise SecScriptError("encoding format should be in string", line=node.line)
        if fmt not in ENCODE_FUNCS:
            raise SecScriptError(f"Unknown encoding format: {fmt}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string", line=node.line)

        return ENCODE_FUNCS[fmt](data)

    elif node.name == "decode":
        if len(node.argument) != 2:
            raise SecScriptError("decode should have only 2 arguments", line=node.line)

        from core.interpreter import evaluate
        fmt = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(fmt, str):
            raise SecScriptError("decoding format should be in string", line=node.line)
        if fmt not in DECODE_FUNCS:
            raise SecScriptError(f"Unknown decoding format: {fmt}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string", line=node.line)

        try:
            return DECODE_FUNCS[fmt](data)
        except Exception:
            raise SecScriptError("Decoding failed, check if the entered data was really one of the valid formats: base64, hex, url", line=node.line)
    
    return None