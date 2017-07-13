#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""auto_py_torrent.

This module provides utilities to download a torrent within specific types.

"""


# Author: Gabriel Scotillo
# URL: https://ocslegna.herokuapp.com
# Please do not download illegal torrents or torrents that you do not have
#     permisson to own.
# This tool is for educational purposes only. Any damage you make will not
#     affect the author.


import os
import sys
import traceback
import logging
import argparse
import re
import requests
import textwrap

from bs4 import BeautifulSoup


args = None
found = False
modes = ['best_rated', 'list']
keep_search = True
key_search = ""
page = ""
string_search = ""
torrent_page = ""
torrents = [{'torrent_project':
             {'page': 'https://torrentproject.se/?t=',
              'key_search': 'No results'}},
            {'the_pirate_bay':
             {'page': 'https://proxyspotting.in/s/?q=',
              'key_search': 'No hits'}},
            {'torrentz2':
             {'page': 'https://torrentz2.eu/search?f=',
              'key_search': 'did not match'}},
            {'rarbg':
             {'page': 'https://rarbg.to/torrents.php?search=',
              'key_search': '<div id="pager_links"></div>'}},
            {'1337x':
             {'page': 'https://1337x.to/search/',
              'key_search': 'No results were returned'}},
            {'eztv':
             {'page': 'https://eztv.ag/search/',
              'key_search': 'It does not have any.'}},
            {'limetorrents':
             {'page': 'https://www.limetorrents.cc/search/all/',
              'key_search': 'No results found'}},
            {'isohunt':
             {'page': 'https://isohunt.to/torrents/?ihq=',
              'key_search': 'No results found'}},
            {'torrentdownloads':
             {'page': 'https://www.torrentdownloads.me/search/?search=',
              'key_search': 'No results found'}},
            {'demonoid':
             {'page': 'https://www.demonoid.pw/files/?query=',
              'key_search': 'No torrents found'}}]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def next_step():
    """Decide next step of the program."""
    # TODO: do.
    print(1)


def download_torrent():
    """Download torrent."""
    # TODO: do.
    if found:
        print(1)


def torrents_found():
    """Check if specific element/info is obtained in content_page.

    This implies the same search key in the torrent page.
    """
    if (key_search) not in content_page:
        return True
    else:
        return False


def select_torrent():
    """Select torrent."""
    # TODO: next! (:
    global found
    found = torrents_found(content_page)

    if not(found):
        # TODO: Add global user input torrent.
        print('No torrents found.')
    else:
        # TODO: Modify this else doc, and add properly logic.
        #       If list, [for each torrent page separate functionality.]
        #       Else, [for each torrent page proceed to download best rated]
        """Specify to user if it wants best rated torrent or select one from list.
        If user wants best ratet change global bool value for download_torrent.
        Else: build table with all data and enable the user select the torrent.
        """


def build_url():
    """Build appropiate encoded URL.

    This implies the same way of searching a torrent as in the page itself.
    """
    url = requests.utils.requote_uri(torrent_page + string_search)
    if page == page == '1337x':
        return(url + '/1/')
    elif page == 'limetorrents':
        return(url + '/')
    else:
        return(url)


def search_torrent():
    """Search the torrent."""
    url = build_url()
    try:
        global content_page
        content_page = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit('\nAn error has ocurred: \n' + str(e))


def insert():
    """Insert args values into global variables."""
    global page
    page = list(torrents[args.torr_page].keys())[0]
    global mode_search
    mode_search = modes[args.mode]
    global torrent_page
    torrent_page = torrents[args.torr_page]['page']
    global string_search
    string_search = args.str_search
    global key_search
    key_search = torrents[args.torr_page]['key_search']


def initialize():
    """Initialize script."""
    print("Welcome to auto_py_torrent!")


def parse():
    """Parse command line arguments. It parses argv into args variable."""
    desc = textwrap.dedent(
        '''\
        ------------------------------------
        Tool for download a desired torrent.
        ------------------------------------
        ''')
    usage_info = textwrap.dedent(
        '''\
        use "python %(prog)s --help" for more information.
        Examples:
          use "python %(prog)s 0 0 "String search" # best rated.
          use "python %(prog)s 1 0 "String search" # list rated.
        ''')
    epi = textwrap.dedent(
        '''\
        ___
        -> Thanks for using auto_py_torrent!
        ''')

    # Parent and only parser.
    parser = argparse.ArgumentParser(
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=usage_info,
        description=desc,
        epilog=epi)
    parser.add_argument('mode', action='store',
                        choices=range(len(modes)),
                        type=int,
                        help='Select mode of torrent download.\n'
                             'e.g: 0 or 1')
    parser.add_argument('torr_page', action='store',
                        choices=range(len(torrents)),
                        type=int,
                        help='Select torrent page to download from.\n'
                             'e.g: 0 or 1 or .. N')
    parser.add_argument('str_search', action='store',
                        type=str,
                        help='Input torrent string to search.\n'
                             'e.g: "String search"')

    global args
    args = parser.parse_args()


def run_it():
    """Search and download torrents until the user says it so."""
    parse()
    initialize()
    while(keep_search):
        insert()
        search_torrent()
        select_torrent()
        download_torrent()
        next_step()


if __name__ == '__main__':
    try:
        run_it()
    except KeyboardInterrupt:
        print('\nSee you the next time.')
    except Exception:
        """Get the full traceback."""
        print('\nAn error has ocurred: \n' + traceback.format_exc())
        logging.debug(traceback.format_exc())
    finally:
        print('Good bye!')
