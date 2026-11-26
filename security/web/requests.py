import requests
from core.errorHandler import SecsRuntimeError, SecsTypeError, SecsNameError, SecsArgumentError, SecScriptError

#http request handeling
def httpRequest(node):
    from core.interpreter import evaluate
    if node.name == "httpRequest":

        if len(node.argument) != 3:
            raise SecsArgumentError("httpRequest function only gets 3 arguments (method, url, response form)")
    
        method = evaluate(node.argument[0])
        lowerMethod = method.lower()
        url = evaluate(node.argument[1])
        responseForm = evaluate(node.argument[2]).lower()

        if not isinstance(method, str):
            raise SecsTypeError("Method should be only in string format", line=node.line)

        if not isinstance(url, str):
            raise SecsTypeError("URL should be in string format", line=node.line)

        if not isinstance(responseForm, str):
            raise SecsTypeError("Response form should be in string and one of (text, statusCode, headers)", line=node.line)

        try:
            if lowerMethod == "get":
                if responseForm == "text":
                    return requests.get(url).text

                elif responseForm == "statusCode":
                    return requests.get(url).status_code

                elif responseForm == "headers":
                    return requests.get(url).headers

                else:
                    raise SecsNameError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            elif lowerMethod == "post":
                if responseForm == "text":
                    return requests.post(url).text

                elif responseForm == "statusCode":
                    return requests.post(url).status_code

                elif responseForm == "headers":
                    return requests.post(url).headers

                else:
                    raise SecsNameError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            else:
                raise SecsNameError("Method not in range of available methods (post and get)", line=node.line)

        except SecScriptError:
            raise

    return None

def redirectInspect(firstAddr, httpMode, timeout, output, line):
    HTTP_METHODS = ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS", "TRACE"]
    OUTPUT_MODES = ["all", "url", "status", "method", "location"]

    redirectList = []

    if httpMode.upper() not in HTTP_METHODS:
        raise SecsNameError(f"HTTP-Method: {httpMode} is Unknown or not accessed", line=line)

    if output not in OUTPUT_MODES:
        raise SecsNameError(f"Unknown output mode: {output}", line=line)
    
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
        raise SecsTypeError(f"Given url {firstAddr} doesn't have http:// or https:// at first", line=line)

    except requests.exceptions.InvalidSchema:
        raise SecsTypeError(f"Given url {firstAddr} schema is invalid", line=line)

    except requests.exceptions.InvalidURL:
        raise SecsTypeError(f"Url {firstAddr} is invalid and not usable", line=line)

    except requests.exceptions.SSLError:
        raise SecsRuntimeError(f"Error in SSL/TLS connection with {firstAddr}", line=line)

    except requests.exceptions.ConnectTimeout:
        raise SecsRuntimeError(f"Connection timeout while connecting to {firstAddr}", line=line)

    except requests.exceptions.ReadTimeout:
        raise SecsRuntimeError(f"Response timeout while connecting to {firstAddr}", line=line)

    except requests.exceptions.Timeout:
        raise SecsRuntimeError(f"Timeout while connecting to {firstAddr}: {timeout}s", line=line)

    except requests.exceptions.TooManyRedirects:
        raise SecsRuntimeError(f"Maximum redirect limit exceeded for {firstAddr}", line=line)

    except requests.exceptions.ConnectionError:
        raise SecsRuntimeError(f"Error while trying to connect to {firstAddr}", line=line)

    except requests.exceptions.RequestException:
        raise SecsRuntimeError(f"Error while trying to inspect redirects of {firstAddr}", line=line)

    except AttributeError:
        raise SecsTypeError(f"Error in input types, make sure to consider this structure: url: string, method: string, timeout: int or float, output: string", line=line)

    except Exception:
        raise SecsRuntimeError("Unexpected error while running redirectInspect",line=line)
        