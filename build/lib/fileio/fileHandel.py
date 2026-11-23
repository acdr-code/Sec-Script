import os

def FileExists(path):
    if os.path.isfile(path):
        return True
    else:
        return False

def WholeFileRead(path):
    with open(path, "r", encoding="utf-8") as f:
        result =  f.read()
    return result

def LineFileRead(path):
    with open(path, "r", encoding="utf-8") as f:
        result = f.read()
    return result.splitlines()

def FileWrite(path, writeObj, mode):
    with open(path, mode, encoding="utf-8") as f:
        result = f.write(writeObj)
    return result