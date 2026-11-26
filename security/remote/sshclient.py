
import paramiko

from core.errorHandler import SecsRuntimeError, SecsTypeError, SecsArgumentError


# Ssh session
def ConnectSsh(target, port, password):
    if not isinstance(target, str) or target.count("@") != 1:
        raise SecsArgumentError("Target must be in username@host format")

    if not isinstance(port, int) or isinstance(port, bool):
        raise SecsTypeError("Port must be an integer")

    if not 1 <= port <= 65535:
        raise SecsArgumentError("Port must be between 1 and 65535")

    if not isinstance(password, str):
        raise SecsTypeError("Password must be a string")

    usrname, host = target.split("@")

    if not usrname or not host:
        raise SecsArgumentError("Username and host cannot be empty")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=usrname, port=port, password=password, timeout=10)
        return client

    except paramiko.AuthenticationException as e:
        client.close()
        raise SecsRuntimeError(f"SSH authentication failed: {e}") from e

    except (paramiko.SSHException, OSError, TimeoutError) as e:
        client.close()
        raise SecsRuntimeError(f"SSH connection failed: {e}") from e


def RunSsh(command, client):
    if not isinstance(command, str):
        raise SecsTypeError("SSH command must be a string")

    if not isinstance(client, paramiko.SSHClient):
        raise SecsTypeError("Invalid SSH client")

    try:
        stdin, stdout, stderr = client.exec_command(command)

        raw = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        exit_code = stdout.channel.recv_exit_status()

        return {
            "raw": raw,
            "lines": raw.splitlines(),
            "exit_code": exit_code,
            "error": error
        }

    except (paramiko.SSHException, OSError, UnicodeDecodeError, EOFError) as e:
        raise SecsRuntimeError(f"SSH command execution failed: {e}") from e


def CloseSsh(client):
    if not isinstance(client, paramiko.SSHClient):
        raise SecsTypeError("Invalid SSH client")

    try:
        client.close()
    except (paramiko.SSHException, OSError) as e:
        raise SecsRuntimeError(f"Failed to close SSH connection: {e}") from e
