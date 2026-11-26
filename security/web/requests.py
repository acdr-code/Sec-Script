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

def redirectInspect(firstAddr, httpMode, timeout, output, line):
    HTTP_METHODS = ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS", "TRACE"]
    OUTPUT_MODES = ["all", "url", "status", "method", "location"]

    redirectList = []

    if httpMode.upper() not in HTTP_METHODS:
        raise SecScriptError(f"HTTP-Method: {httpMode} is Unknown or not accessed", line=line)

    if output not in OUTPUT_MODES:
        raise SecScriptError(f"Unknown output mode: {output}", line=line)
    
    try:
        response = requests.request(
            method=httpMode.upper(),
            url=firstAddr,
            allow_redirects=True,
            timeout=timeout
        )

        for redirect in response.history:
            redirectList.append({
                "url": redirect.url,
                "status": redirect.status_code,
                "method": redirect.request.method,
                "location": redirect.headers.get("Location")
            })

        if output == "all":
            return redirectList

        else:
            return [item[output] for item in redirectList]

    except requests.exceptions.MissingSchema:
        raise SecScriptError(f"Given url {firstAddr} doesn't have http:// or https:// at first", line=line)

    except requests.exceptions.InvalidSchema:
        raise SecScriptError(f"Given url {firstAddr} schema is invalid", line=line)

    except requests.exceptions.InvalidURL:
        raise SecScriptError(f"Url {firstAddr} is invalid and not usable", line=line)

    except requests.exceptions.SSLError:
        raise SecScriptError(f"Error in SSL/TLS connection with {firstAddr}", line=line)

    except requests.exceptions.ConnectTimeout:
        raise SecScriptError(f"Connection timeout while connecting to {firstAddr}", line=line)

    except requests.exceptions.ReadTimeout:
        raise SecScriptError(f"Response timeout while connecting to {firstAddr}", line=line)

    except requests.exceptions.Timeout:
        raise SecScriptError(f"Timeout while connecting to {firstAddr}: {timeout}s", line=line)

    except requests.exceptions.TooManyRedirects:
        raise SecScriptError(f"Maximum redirect limit exceeded for {firstAddr}", line=line)

    except requests.exceptions.ConnectionError:
        raise SecScriptError(f"Error while trying to connect to {firstAddr}", line=line)

    except requests.exceptions.RequestException:
        raise SecScriptError(f"Error while trying to inspect redirects of {firstAddr}", line=line)

    except AttributeError:
        raise SecScriptError(f"Error in input types, make sure to consider this structure: url: string, method: string, timeout: int or float, output: string")

    except Exception:
        raise SecScriptError("Unexpected error while running redirectInspect",line=line)
        