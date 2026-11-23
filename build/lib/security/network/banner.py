import socket
from core.errorHandler import SecScriptError

def grabBanner(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((ip,port))

        try:
            result = sock.recv(1024)

        except socket.timeout:
            result = b''

        if not result:
            sock.sendall(b"\r\n")

            try:
                result = sock.recv(1024)

            except socket.timeout:
                result = b''

            if not result:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")

                try:
                    result = sock.recv(1024)

                except socket.timeout:
                    result = b''

        banner = result.decode("utf-8", errors="ignore").strip()
        return banner if banner else "NoBanner"

    except (socket.timeout, OSError, ConnectionRefusedError) as e:
        raise SecScriptError(f"Error while trying to grab Banner from {ip}:{port}, Full error -> {e}")

    finally:
        sock.close()