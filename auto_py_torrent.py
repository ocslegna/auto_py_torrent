#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tool for automate torrent download."""

# Author: Gabriel Scotillo
# URL: https://ocslegna.herokuapp.com
# Please do not download illegal torrents or torrents that you do not have
#     permisson to own.
# This tool is for educational purposes only. Any damage you make will not
#     affect the author.

import os
import sys
import argparse
import re
import requests
import textwrap

from bs4 import BeautifulSoup


args = None
found = False
modes = ['best_rated', 'list']
keep_search = True
str_search = ""
torr_page = ""
torrents = [{'torrent_project': {'key_search': 'No results'}},
            {'kickass': {'key_search': 'Download torrent'}}]


def next_step():
    """Decide next step of the program."""
    # TODO: do.
    print(1)


def download_torrent():
    """Download torrent."""
    # TODO: do.
    if found:
        print(1)


def torrents_found(content):
    """Check if specific element/info is obtained in content_page."""
    # TODO: Modify first key with selected global input.
    if (torrents["torrent_project"]["key_search"]) not in content:
        return True
    else:
        return False


def select_torrent():
    """Select torrent."""
    global found
    found = torrents_found(content_page)

    if not(found):
        # TODO: Add global user input torrent.
        print("No torrents found.")
    else:
        # TODO: Modify this else doc, and add properly logic.
        #       If list, [for each torrent page separate functionality.]
        #       Else, [for each torrent page proceed to download best rated]
        """Specify to user if it wants best rated torrent or select one from list.
        If user wants best ratet change global bool value for download_torrent.
        Else: build table with all data and enable the user select the torrent.
        """


def search_torrent():
    """Search the torrent."""
    # TODO: modify torrents sub index with user input preference
    url = torrents[0] + str_search + "/"
    try:
        global content_page
        content_page = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit('\n' + str(e))


def insert():
    """Insert args values into global variables."""
    # TODO: Fill variables with args elements.
    #       Add mode.
    #       Erase print, verify.
    print("Insert torrent page name and string search in different lines: ")
    global torr_page
    torr_page = input()
    global str_search
    str_search = input()


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
          use "python %(prog)s 0 0 "String search" for example. # best rated.
          use "python %(prog)s 1 0 "String search" for example. # list rated.
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
    parser.add_argument('torrent_page', action='store',
                        choices=range(len(torrents)),
                        type=int,
                        help='Select torrent page to download from.\n'
                             'e.g: 0 or 1 or .. N')
    parser.add_argument('string_search', action='store',
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
        print("\nSee you the next time.")
