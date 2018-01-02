import unittest
import io
from dnsinq import core

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


class CoreTestCase(unittest.TestCase):

    def test_etchostline_to_host(self):
        self.assertEqual(
            'example.com',
            core.etchostsline_to_host('127.0.0.1 example.com'),
        )
        # the comment character will be returned because this is naive,
        # intended usage is to be filtered through the common regex
        self.assertEqual(
            '#',
            core.etchostsline_to_host('127.0.0.1 # example.com'),
        )

    def test_get_simple_list(self):
        domains = core.get_domains(core.iter_str(SIMPLE_LIST))
        self.assertEqual([
            'example.com',
            'localhost.local',
            'null.example',
            'test.example.com',
        ], sorted(domains))

    def test_get_domains_etchosts(self):
        domains = core.get_domains(
            core.iter_str(ETC_HOSTS), filter_=core.etchostsline_to_host)
        self.assertEqual([
            'example.com',
            'localhost.local',
            'null.example',
            'some.blocked.test',
        ], sorted(domains))

    def test_get_domains_dnsmasq_nxdomain(self):
        domains = core.get_domains(
            core.iter_str(DNSMASQ_NXDOMAIN),
            filter_=core.dnsmasqnxdomain_to_host,
        )
        self.assertEqual([
            'bad.example',
            'example.com',
            'null.example',
            'some.blocked.test',
        ], sorted(domains))

    def test_get_domains_etchosts_stream(self):
        domains = core.get_domains(
            core.iter_stream(io.StringIO(ETC_HOSTS)),
            filter_=core.etchostsline_to_host,
        )
        self.assertEqual([
            'example.com',
            'localhost.local',
            'null.example',
            'some.blocked.test',
        ], sorted(domains))

    def test_detect_filter(self):
        self.assertIsNone(core.detect_filter(core.iter_str(SIMPLE_LIST)))
        self.assertEqual(
            core.etchostsline_to_host,
            core.detect_filter(core.iter_str(ETC_HOSTS)))

    def test_generate_nxdomain_conf(self):
        domains = [
            'example.com',
            'local.test',
        ]
        generator = core.generate_nxdomain_conf(domains)
        self.assertEqual('server=/example.com/\n', next(generator))
        self.assertEqual('server=/local.test/\n', next(generator))

    def test_domains_from_stream(self):
        for lists in [SIMPLE_LIST, ETC_HOSTS, DNSMASQ_NXDOMAIN]:
            result = core.domains_from_stream(io.StringIO(lists))
            self.assertEqual(4, len(result))
            self.assertIn('example.com', result)
