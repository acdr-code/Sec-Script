from core.errorHandler import SecScriptError
from ipaddress import ip_address, ip_network

def ipversion(ipInput, line):
    try:
        ip = ip_address(ipInput)
        return ip.version
    except ValueError:
        raise SecScriptError(f"IP: {ipInput} is not valid", line=line)
    except Exception:
        raise SecScriptError(f"Error while checking version of ip: {ipInput}", line=line)

def ipValidity(ipInput, line):
    try:
        ip = ip_address(ipInput)
        return True
    except ValueError:
        return False
    except Exception:
        raise SecScriptError(f"Error while checking validity of ip: {ipInput}", line=line)

def firstUsableaddr(networkInput, line):
    try:
        network = ip_network(networkInput, strict=False)

        if network.version == 6 and network.prefixlen == 128:
            return str(network.network_address)

        hosts = network.hosts()
        firstUsable = next(hosts, None)
        return str(firstUsable)

    except ValueError:
        raise SecScriptError(f"Network: {networkInput} is not valid", line=line)
    except Exception:
        raise SecScriptError(f"Error while checking first usable network of {networkInput}", line=line)

def networkRange(networkInput, line):
    try:
        network = ip_network(networkInput, strict=False)
        version = network.version

        if version == 4:
            rangeStart = network.network_address
            rangeEnd = network.broadcast_address

        elif version == 6:
            rangeStart = network.network_address
            rangeEnd = network[-1]

        return {"start": str(rangeStart), "end": str(rangeEnd)}

    except ValueError:
        raise SecScriptError(f"Network: {networkInput} is not valid", line=line)
    except Exception:
        raise SecScriptError(f"Error while checking network range of {networkInput}", line=line)

def networkUsableNum(networkInput, line):
    try:
        network = ip_network(networkInput, strict=False)
        version = network.version

        if version == 4:
            if network.prefixlen <= 30:
                usableRange = network.num_addresses - 2
            else:
                usableRange = network.num_addresses

        elif version == 6:
            usableRange = network.num_addresses

        return usableRange

    except ValueError:
        raise SecScriptError(f"Network: {networkInput} is not valid", line=line)
    except Exception:
        raise SecScriptError(f"Error while counting usable network addresses of {networkInput}", line=line)