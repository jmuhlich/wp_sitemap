"""Construct HTML sitemap via WordPress XML-RPC API"""

import argparse
import getpass
import collections
import pywordpress

def render_page(page):
    """Recursively render a page to HTML."""
    print '<li><a href="{link}">{title}</a>'.format(**page)
    if 'children' in page:
        print '<ul>'
        for child in page['children']:
            render_page(child)
        print '</ul>'
    print '</li>'

parser = argparse.ArgumentParser(
    description=__doc__)
parser.add_argument('url', type=str, help='URL of wordpress installation')
parser.add_argument('username', type=str, help='WordPress user to log in as')
args = parser.parse_args()
password = getpass.getpass('WordPress password:')

wp = pywordpress.Wordpress(args.url, args.username, password)

# Wordpress.get_pages doesn't expose the max_pages argument so we need to hit
# the xmlrpc client ourselves. Is pywordpress even doing anything for us at this
# point?
page_list = wp.server.wp.getPages(wp.blog_id, wp.user, wp.password, -1)
# Sort in WP menu order.
page_list = sorted(page_list, key=lambda p: (p['wp_page_order'], p['title']))
# Build OrderedDict with same order, keyed on page_id.
page_map = collections.OrderedDict((p['page_id'], p) for p in page_list)
# Add each child page to its parent's "children" list. Because we have already
# ordered the pages in page_map, each "children" list will retain this ordering.
for page in page_map.values():
    parent_id = page['wp_page_parent_id']
    if parent_id != 0:
        parent = page_map[parent_id]
        child_list = parent.setdefault('children', [])
        child_list.append(page)
# Pull root pages out into a list.
pages = [p for p in page_map.values() if p['wp_page_parent_id'] == 0]

# Print HTML to stdout.
print '<ul>'
for p in pages:
    render_page(p)
print '</ul>'
