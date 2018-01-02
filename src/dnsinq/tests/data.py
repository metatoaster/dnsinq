__all__ = [
    'SIMPLE_LIST',
    'ETC_HOSTS',
    'DNSMASQ_NXDOMAIN',
]

SIMPLE_LIST = """
# This is a comment

localhost.local
null.example
# some additional comment
example.com
test.example.com
"""

ETC_HOSTS = """
# This is a comment

127.0.0.1  localhost.local
0.0.0.0    null.example
0.0.0.0    # some invalid line
0.0.0.0    example.com # with a comment
0.0.0.0    some.blocked.test # with a comment
"""

DNSMASQ_NXDOMAIN = """
server=/example.com/
server=/null.example/
server=/bad.example/
server=/some.blocked.test/
"""
