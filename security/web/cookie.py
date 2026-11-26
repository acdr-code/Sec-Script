from core.errorHandler import SecScriptError
import requests

def cookie(url, method, timeout, output, line):
    HTTP_METHODS = ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS", "TRACE"]
    OUTPUT_MODES = ["all", "name", "value","domain", "path", "expires", "secure"]

    cookiesGiven = []

    if method.upper() not in HTTP_METHODS:
        raise SecScriptError(f"HTTP-Method: {method} is unknown or not accessed", line=line)

    if output.lower() not in OUTPUT_MODES:
        raise SecScriptError(f"Output method: {output} is unknown", line=line)

    try:
        response = requests.request(
            method=method,
            url=url,
            timeout=timeout,
        )

        for acookie in response.cookies:
            cookiesGiven.append({
                "name": acookie.name,
                "value": acookie.value,
                "domain": acookie.domain,
                "path": acookie.path,
                "expires": acookie.expires,
                "secure": acookie.secure
            })

        if output.lower() == "all":
            return cookiesGiven

        else:
            return [item[output] for item in cookiesGiven]

    except requests.exceptions.MissingSchema:
        raise SecScriptError("URL is missing http:// or https://", line=line)

    except requests.exceptions.InvalidSchema:
        raise SecScriptError("URL schema is invalid", line=line)

    except requests.exceptions.InvalidURL:
        raise SecScriptError(f"URL is invalid: {url}", line=line)

    except requests.exceptions.SSLError:
        raise SecScriptError("SSL/TLS connection error", line=line)

    except requests.exceptions.ProxyError:
        raise SecScriptError("Proxy connection error", line=line)

    except requests.exceptions.ConnectTimeout:
        raise SecScriptError("Connection timeout", line=line)

    except requests.exceptions.ReadTimeout:
        raise SecScriptError("Response timeout", line=line)

    except requests.exceptions.Timeout:
        raise SecScriptError("Request timeout", line=line)

    except requests.exceptions.TooManyRedirects:
        raise SecScriptError("Maximum redirect limit exceeded", line=line)

    except requests.exceptions.ChunkedEncodingError:
        raise SecScriptError("Invalid or incomplete chunked response", line=line)

    except requests.exceptions.ContentDecodingError:
        raise SecScriptError("Response content decoding failed", line=line)

    except requests.exceptions.ConnectionError:
        raise SecScriptError(f"Connection error at {url}", line=line)

    except requests.exceptions.RequestException:
        raise SecScriptError("HTTP request failed", line=line)

    except (AttributeError, TypeError, ValueError):
        raise SecScriptError("Error while processing cookie data", line=line)

    except Exception:
        raise SecScriptError("Unexpected error while inspecting cookies", line=line)