import sys
import argparse
import logging
from os.path import basename
from os.path import exists
from datetime import datetime

from dnsinq.manage import fetch_domains_from
from dnsinq.manage import append_new_dnsmasq_nxdomains_set
from dnsinq.manage import DNSMASQ_NXDOMAIN_CONF


def loadall(path):
    with open(path) as fd:
        return fetch_domains_from(fd.read().strip().splitlines())


def run(argv):
    parser = argparse.ArgumentParser(
        basename(argv[0]),
        description='utility for adding domains to dnsmasq so that an '
                    'nxdomain response be generated when queried',
    )
    parser.add_argument(
        '-l', '--load-list', action='store', dest='list_path',
        help='path to the file that contains the list of import locations; '
             'these locations can be either local paths or http(s) urls',
    )
    parser.add_argument(
        '-v', '--verbose', action='count', dest='verbose', default=0,
        help='increase logging verbosity',
    )
    parser.add_argument(
        '--conf', action='store', dest='dnsmasq_conf',
        default=DNSMASQ_NXDOMAIN_CONF,
        help='dnsmasq configuration file for the nxdomain list (default: %s)' %
            DNSMASQ_NXDOMAIN_CONF
    )

    args = parser.parse_args(argv[1:])
    if not (args.list_path and exists(args.list_path)):
        parser.print_help()
        return

    level = {1: logging.INFO, 2: logging.DEBUG}.get(
        min(args.verbose, 2), logging.WARNING)
    logger = logging.getLogger('dnsinq')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        u'%(asctime)s %(levelname)s %(name)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(level)

    try:
        domains = loadall(args.list_path)
        comment = 'added %s' % str(datetime.now())
        append_new_dnsmasq_nxdomains_set(
            domains, path=args.dnsmasq_conf, comment=comment)
    finally:
        logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)


def main():
    run(sys.argv)


if __name__ == '__main__':
    main()
