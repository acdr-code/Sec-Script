import requests
from core.errorHandler import SecScriptError

#http request handeling
def httpRequest(node):
    from core.interpreter import evaluate
    if node.name == "httpRequest":

        if len(node.argument) != 3:
            raise SecScriptError("httpRequest function only gets 3 arguments (method, url, response form)")
    
        method = evaluate(node.argument[0])
        lowerMethod = method.lower()
        url = evaluate(node.argument[1])
        responseForm = evaluate(node.argument[2]).lower()

        if not isinstance(method, str):
            raise SecScriptError("Method should be only in string format", line=node.line)

        if not isinstance(url, str):
            raise SecScriptError("URL should be in string format", line=node.line)

        if not isinstance(responseForm, str):
            raise SecScriptError("Response form should be in string and one of (text, statusCode, headers)", line=node.line)

        try:
            if lowerMethod == "get":
                if responseForm == "text":
                    return requests.get(url).text

                elif responseForm == "statusCode":
                    return requests.get(url).status_code

                elif responseForm == "headers":
                    return requests.get(url).headers

                else:
                    raise SecScriptError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            elif lowerMethod == "post":
                if responseForm == "text":
                    return requests.get(url).text

                elif responseForm == "statusCode":
                    return requests.get(url).status_code

                elif responseForm == "headers":
                    return requests.get(url).headers

                else:
                    raise SecScriptError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            else:
                raise SecScriptError("Method not in range of available methods (post and get)", line=node.line)

        except:
            raise SecScriptError("Error in handling http request", line=node.line)

    return None