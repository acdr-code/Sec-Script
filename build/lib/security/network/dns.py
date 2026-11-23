from core.errorHandler import SecScriptError

#Dns record
def dnsRecords(node):
    from core.interpreter import evaluate
    import dns.resolver

    domain = evaluate(node.ip)
    record = evaluate(node.record)

    allRecordType = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV", "CAA", "PTR"]

    if record in allRecordType:
        try:
            answers = dns.resolver.resolve(domain, record)
            results = [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                dns.resolver.NoNameservers, dns.exception.Timeout):
            results = []

    elif record == "ALL":
        results = {}
        for rtype in allRecordType:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [rdata.to_text() for rdata in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                    dns.resolver.NoNameservers, dns.exception.Timeout):
                pass

    else:
        raise SecScriptError("Unknown DNS record wanted", line=node.line)

    return results