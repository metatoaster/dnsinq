import re

patt_match_domain = re.compile(
    '^((-|_)*[a-z\d]((-|_)*[a-z\d])*(-|_)*)(\.(-|_)*'
    '([a-z\d]((-|_)*[a-z\d])*))*$'
)

patt_etc_hosts = re.compile(
    '^\d{1,3}(\.\d{1,3}){3}\s+(?P<host>[^\s]*)'
)


def iter_str(s):
    for s in s.splitlines():
        if s.startswith('#'):
            continue
        yield s


def iter_stream(stream):
    for line in stream:
        if line.startswith('#'):
            continue
        yield line


def etchostsline_to_host(s):
    match = patt_etc_hosts.match(s)
    if match:
        return match.group('host')


def get_domains(strs, filter_=None):
    domains = set()
    for s in strs:
        domain = filter_(s) if callable(filter_) else s
        if domain and patt_match_domain.match(domain):
            domains.add(domain)
    return sorted(domains)


def detect_filter(strs):
    matrix = (
        (patt_etc_hosts, etchostsline_to_host),
        (patt_match_domain, None)
    )

    for s in strs:
        for patt, filter_ in matrix:
            if patt.match(s):
                return filter_
