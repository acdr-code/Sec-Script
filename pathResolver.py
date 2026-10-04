def resolve_path(node):
    import os
    from interpreter import evaluate, dir_stack
    from errorHandler import SecScriptError

    path = evaluate(node.file)
    if not isinstance(path, str):
        raise SecScriptError("File path must be a string", line=node.line)
    current_dir = dir_stack[-1] if dir_stack else os.getcwd()
    return os.path.join(current_dir, path)