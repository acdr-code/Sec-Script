import socket

from core.errorHandler import SecsRuntimeError, SecsTypeError, SecsArgumentError


# Port Scan
def portScan(ip, port, timeout, list):
    if not isinstance(ip, str):
        raise SecsTypeError("IP address must be a string")

    if not isinstance(port, int) or isinstance(port, bool):
        raise SecsTypeError("Port must be an integer")

    if not 1 <= port <= 65535:
        raise SecsArgumentError("Port must be between 1 and 65535")

    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        raise SecsTypeError("Timeout must be a number")

    if timeout <= 0:
        raise SecsArgumentError("Timeout must be greater than zero")

    if not isinstance(list, list):
        raise SecsTypeError("Result must be a list")

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))

        if result == 0:
            list.append(port)

    except (socket.gaierror, socket.timeout, OSError) as e:
        raise SecsRuntimeError(f"Port scan failed: {e}") from e

    finally:
        if sock is not None:
            sock.close()