import dns.resolver
import dns.exception
# DNS record
def dnsRecords(node):
    from core.interpreter import evaluate
    from core.errorHandler import (
        SecsNameError,
        SecsTypeError,
        SecsArgumentError,
        SecsRuntimeError,
        SecScriptError
    )

    domain = evaluate(node.ip)
    record = evaluate(node.record)

    if not isinstance(domain, str):
        raise SecsTypeError(
            "DNS domain must be a string",
            line=node.line
        )

    if not isinstance(record, str):
        raise SecsTypeError(
            "DNS record type must be a string",
            line=node.line
        )

    if not domain.strip():
        raise SecsArgumentError(
            "DNS domain cannot be empty",
            line=node.line
        )

    record = record.upper()

    allRecordType = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV", "CAA", "PTR"]

    if record in allRecordType:
        try:
            answers = dns.resolver.resolve(domain, record)
            results = [rdata.to_text() for rdata in answers]

        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.exception.Timeout
        ):
            results = []

        except SecScriptError:
            raise

        except (dns.exception.DNSException, OSError, ValueError) as e:
            raise SecsRuntimeError(
                f"DNS lookup failed: {e}",
                line=node.line
            ) from e

    elif record == "ALL":
        results = {}

        for rtype in allRecordType:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [rdata.to_text() for rdata in answers]

            except (
                dns.resolver.NoAnswer,
                dns.resolver.NXDOMAIN,
                dns.resolver.NoNameservers,
                dns.exception.Timeout
            ):
                pass

            except SecScriptError:
                raise

            except (dns.exception.DNSException, OSError, ValueError) as e:
                raise SecsRuntimeError(
                    f"DNS lookup failed for record {rtype}: {e}",
                    line=node.line
                ) from e

    else:
        raise SecsNameError(
            f"Unknown DNS record type: {record}",
            line=node.line
        )

    return results