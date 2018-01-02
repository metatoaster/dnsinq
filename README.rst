dnsinq
======

Helpers for generating certain dnsmasq configuration files.


Usage
=====

Create a file with a list of paths/URLs to hosts (/etc/hosts) files or
simple listing of domain names.  Example ``source.txt``:

.. code::

    /etc/hosts
    https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
    https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt

Ensure that in ``/etc/dnsmasq.conf`` file, that the following option is
uncommented, so that a dedicated configuration file with the server
entries can be provided and used:

.. code::

    # Include all files in a directory which end in .conf
    conf-dir=/etc/dnsmasq.d/,*.conf

Run ``dnsinq`` with the ``-l`` flag pointing to the location of the
listing file.  If required, also specify the location of the specific
``dnsmasq.d`` configuration file with the ``--conf`` flag (default:
``/etc/dnsmasq.d/99-nxdomains.conf``):

.. code::

    $ dnsinq -l source.txt

The configuration file will either be created or appended with new
domains found in the referenced listings.
