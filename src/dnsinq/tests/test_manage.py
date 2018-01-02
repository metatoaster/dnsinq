import unittest
import tempfile
from os.path import join

from dnsinq.manage import append_new_dnsmasq_nxdomains_set
from dnsinq.manage import fetch_domains_from

from .data import *


class ManageTestCase(unittest.TestCase):

    def test_append_new(self):
        with tempfile.TemporaryDirectory() as workdir:
            target = join(workdir, 'nxdomain.conf')
            append_new_dnsmasq_nxdomains_set(
                {'example.com', 'example.test'}, target)
            with open(target) as fd:
                self.assertEqual(
                    'server=/example.com/\n'
                    'server=/example.test/\n', fd.read())

    def test_append_existing(self):
        with tempfile.TemporaryDirectory() as workdir:
            target = join(workdir, 'nxdomain.conf')
            with open(target, 'w') as fd:
                fd.write('server=/example.test/\n')
                fd.write('server=/example.com/\n')

            append_new_dnsmasq_nxdomains_set(
                {'example.test'}, target)
            with open(target) as fd:
                self.assertEqual(
                    'server=/example.test/\n'
                    'server=/example.com/\n', fd.read())

            append_new_dnsmasq_nxdomains_set(
                {'banned.test', 'banned.example'}, target)
            with open(target) as fd:
                self.assertEqual(
                    'server=/example.test/\n'
                    'server=/example.com/\n'
                    'server=/banned.example/\n'
                    'server=/banned.test/\n', fd.read())

    def test_fetch_domains_from(self):
        with tempfile.TemporaryDirectory() as workdir:
            simple_list = join(workdir, 'simple.txt')
            etc_hosts = join(workdir, 'hosts')

            with open(simple_list, 'w') as fd:
                fd.write(SIMPLE_LIST)

            with open(etc_hosts, 'w') as fd:
                fd.write(ETC_HOSTS)

            self.assertEqual([
                'example.com',
                'localhost.local',
                'null.example',
                'some.blocked.test',
                'test.example.com',
            ], sorted(fetch_domains_from([simple_list, etc_hosts])))
