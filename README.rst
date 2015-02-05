wp_sitemap
==========
Construct HTML sitemap from WordPress pages via XML-RPC API.

Requirements
============
* Python 2.7 (for argparse, at least)
* pywordpress - https://pypi.python.org/pypi/pywordpress

Usage
=====

::

    wp_sitemap.py [-h] url username

    positional arguments:
      url         URL of wordpress installation
      username    WordPress user to log in as

    optional arguments:
      -h, --help  show this help message and exit

Notes
=====
You will be prompted interactively for the WordPress user's password.

The output format is defined by the ``render_page`` function. It's very simple
and easy enough to hack to produce a different output format.
