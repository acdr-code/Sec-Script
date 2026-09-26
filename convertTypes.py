from errorHandler import SecScriptError

def convert(node):
    from interpreter import evaluate

    if node.name in ("string", "float", "bool", "int"):
        if len(node.argument) != 1:
            raise SecScriptError(f"Type changing needs exactly 1 argument", line=node.line)
        
        if node.name == "string":
            try:
                value = evaluate(node.argument[0])
                return str(value)
            except Exception:
                raise SecScriptError(f"Can't string format this argument", line=node.line)

        if node.name == "int":
            try:
                value = evaluate(node.argument[0])
                return int(value)
            except Exception:
                raise SecScriptError(f"Can't int format this argument", line=node.line)

        if node.name == "float":
            try:
                value = evaluate(node.argument[0])
                return float(value)
            except Exception:
                raise SecScriptError(f"Can't float this argument", line=node.line)

        if node.name == "bool":
            try:
                value = evaluate(node.argument[0])
                if value == "" or value == 0:
                    return False
                else:
                    return True
            except Exception:
                raise SecScriptError(f"Can't bool this argument", line=node.line)
            
        return None