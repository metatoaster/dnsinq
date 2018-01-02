import io
import logging
from os.path import exists
from os.path import isfile

import requests

from dnsinq.core import domains_from_stream
from dnsinq.core import generate_nxdomain_conf

logger = logging.getLogger(__name__)

DNSMASQ_NXDOMAIN_CONF = '/etc/dnsmasq.d/99-nxdomains.conf'


def load_local_domains_set(path):
    if not exists(path):
        return set()
    if not isfile(path):
        logger.warning("'%s' is not a file")
        return set()
    with open(path) as stream:
        return domains_from_stream(stream)


def load_remote_domains_set(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        logger.warning("GET %s status %s", url, r.status_code)
        return {}

    stream = io.StringIO(r.text)
    return domains_from_stream(stream)


def append_new_dnsmasq_nxdomains_set(domains, path=DNSMASQ_NXDOMAIN_CONF):
    existing = load_local_domains_set(path)
    logger.info("found %d existing domains in '%s'", len(existing), path)
    new_domains = sorted(domains - existing)
    logger.info(
        "%d out of %d domains are to be newly added",
        len(new_domains), len(domains),
    )
    with open(path, 'a') as stream:
        for domain in generate_nxdomain_conf(new_domains):
            stream.write(domain)


def fetch_domains_from(sources):
    domains = set()
    for source in sources:
        if source.startswith('http'):
            logger.info("loading remote list '%s'", source)
            new_domains = load_remote_domains_set(source)
        else:
            logger.info("loading local list '%s'", source)
            new_domains = load_local_domains_set(source)

        logger.info("fetched %d domains from '%s'", len(new_domains), source)
        domains.update(new_domains)

    logger.info("fetched %d unique domains", len(domains))
    return domains
