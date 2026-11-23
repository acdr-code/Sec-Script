import socket
import ssl
import time

def TlsCertCheck(host, timeout):
    result = {
        "valid": False,
        "reason": "",
        "host": host,
        "days_left": -1,
        "expires": "",
        "issuer": "",
    }

    try:
        with socket.create_connection((host, 443), timeout=timeout) as conn:
            context = ssl.create_default_context()
            with context.wrap_socket(conn, server_hostname=host) as tls_conn:
                cert = tls_conn.getpeercert()
    except ssl.SSLCertVerificationError as e:

        result["reason"] = e.verify_message
        return result

    result["valid"] = True
    result["expires"] = cert["notAfter"]

    expires_ts = ssl.cert_time_to_seconds(cert["notAfter"])
    result["days_left"] = int((expires_ts - time.time()) / 86400)

    issuer = {}
    for group in cert["issuer"]:
        for key, value in group:
            issuer[key] = value
    result["issuer"] = issuer.get("organizationName", "")

    return result