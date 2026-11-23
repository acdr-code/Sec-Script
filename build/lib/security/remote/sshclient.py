import paramiko

#Ssh session
def ConnectSsh(target, port, password):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    usrname, host = target.split("@")

    client.connect(
        hostname=host,
        username=usrname,
        port=port,
        password=password,
        timeout=10
    )

    return client

def RunSsh(command, client):
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

def CloseSsh(client):
    client.close()