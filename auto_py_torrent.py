#!/usr/bin/env python3
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
import textwrap
import coloredlogs
import requests

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from tabulate import tabulate

args = None
content_page = None
found = False
hrefs = None
magnet = ""
modes = ['best_rated', 'list']
mode_search = ""
keep_search = True
key_search = ""
page = ""
selected = ""
string_search = ""
table = None
torrent = ""
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
              'key_search': 'No results found'}}]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
coloredlogs.install()


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    GREEN = '\033[42m'
    CYAN = '\033[36m'
    RED = '\033[41m'
    PURPLE = '\033[35m'
    LIGHTBLUE = '\033[0m\033[34m'
    LIGHTGREEN = '\033[0m\033[32m'
    LIGHTCYAN = '\033[0m\033[36m'
    LIGHTRED = '\033[0m\033[31m'
    LIGHTPURPLE = '\033[0m\033[35m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


def next_step():
    """Decide next step of the program."""
    # TODO: do.
    print(1)


def download_torrent():
    """Download torrent.

    Rated implies download  the unique best rated torrent found.
    Otherwise: download the selected torrent.
    """
    # TODO: do.
    try:
        if not(found):
            return

        # Also think about first magnet and then torrent.
        # should it be the SAME way to download it either it is rated or not?
        if mode_search == 'rated':
            # torrent or magnet should be ready here.
            # So, start download.
            print(1)
        else:
            print(1)
    except:
        logging.info('\nAn error has ocurred: \n')
        logging.error(traceback.format_exc())
        raise SystemExit()


def build_table():
    # TODO: In list mode, the components of the table are in elements.
    headers = ['Title', 'Seeders', 'Leechers', 'Age', 'Size']
    titles = []
    seeders = []
    leechers = []
    ages = []
    sizes = []

    if page == 'torrent_project':
        titles = [span.find('a').get_text() for span in elements[0]]
        seeders = [span.get_text() for span in elements[1]]
        leechers = [span.get_text() for span in elements[2]]
        ages = [span.get_text() for span in elements[3]]
        sizes = [span.get_text() for span in elements[4]]

        domain = 'https://torrentproject.se'
        global hrefs
        hrefs = [domain + span.find(href=re.compile('torrent.html'))['href'] for span in elements[0]]

    elif page == 'the_pirate_bay':
        for elem in elements[0]:
            title = elem.find('a', {'class': 'detLink'}).get_text()
            titles.append(title)

            font_text = elem.find('font', {'class': 'detDesc'}).get_text()
            dammit = UnicodeDammit(font_text)
            age, size = dammit.unicode_markup.split(',')[:-1]
            ages.append(age)
            sizes.append(size)

            domain = 'https://proxyspotting.in'
            href = domain + elem.find('a', title=re.compile('magnet'))['href']
            global hrefs
            hrefs.append(href)

        seeders = [elem.get_text() for elem in elements[1]]
        leechers = [elem.get_text() for elem in elements[2]]

    global table
    table = [[Colors.BOLD + titles[i] + Colors.ENDC
              if (i+1) % 2 == 0
              else titles[i],
              Colors.SEEDER + seeders[i] + Colors.ENDC
              if (i+1) % 2 == 0
              else Colors.LIGHTGREEN + seeders[i] + Colors.ENDC,
              Colors.LEECHER + leechers[i] + Colors.ENDC
              if (i+1) % 2 == 0
              else Colors.LIGHTRED + leechers[i] + Colors.ENDC,
              Colors.BLUE + ages[i] + Colors.ENDC
              if (i+1) % 2 == 0
              else Colors.LIGHTBLUE + ages[i] + Colors.ENDC,
              Colors.PURPLE + sizes[i] + Colors.ENDC
              if (i+1) % 2 == 0
              else Colors.LIGHTPURPLE + sizes[i] + Colors.ENDC]
              for i in range(len(hrefs))]

    print(tabulate(table,
                   headers=headers,
                   tablefmt='fancy_grid',
                   numalign='right',
                   stralign='left',
                   showindex=True))


def soupify():
    """Get proper torrent/magnet information.

    If search_mode is rated then get torrent/magnet.
    If not, get all the elements to build the table.
    There are different ways for each page.
    """
    # TODO: Add search reference for each page.
    soup = BeautifulSoup(content_page, 'lxml')
    if page == 'torrent_project':
        main = soup.find('div', {'id': 'similarfiles'})
        if mode_search == 'rated':
            rated_url = main.find(href=re.compile('torrent.html'))['href']
            domain = 'https://torrentproject.se'
            content_most_rated = requests.get(domain + rated_url)
            rated_soup = BeautifulSoup(content_most_rated, 'lxml')
            global magnet
            magnet = rated_soup.find('a', href=True, text=re.compile('Download'))['href']
        else:
            divs = main.find_all('div', limit=30)[1:]
            global elements
            elements = list(zip(*[d.find_all('span') for d in divs]))
    elif page == 'the_pirate_bay':
        main = soup.find('table', {'id': 'searchResult'})

        if mode_search == 'rated':
            rated_url = main.find('a', href=re.compile('torrent'))['href']
            domain = 'https://proxyspotting.in'
            content_most_rated = requests.get(domain + rated_url)
            rated_soup = BeautifulSoup(content_most_rated)
            global magnet
            magnet = rated_soup.find('a', href=True, text=re.compile('Get this torrent'))['href']
        else:
            trs = main.find('tbody').find_all('tr')
            global elements
            elements = list(zip(*[tr.find_all('td')[1:] for tr in trs]))


def select_torrent():
    """Select torrent.

    First check if specific element/info is obtained in content_page.
    Specify to the user if it wants best rated torrent or select one from list.
    If the user wants best rated:
        Directly obtain the appropiate magnet/torrent link.
    Else: build table with all data and enable the user select the torrent.
    """
    try:
        global found
        found = bool(key_search not in content_page)

        if not(found):
            logging.info('No torrents found.')
            return

        soupify()
        if mode_search != "rated":
            build_table()
            global selected
            selected = input('>> ')
            # TODO: Something else here? Something to validate the selected row?
    except:
        logging.info('\nAn error has ocurred: \n')
        logging.error(traceback.format_exc())
        raise SystemExit()


def build_url():
    """Build appropiate encoded URL.

    This implies the same way of searching a torrent as in the page itself.
    """
    url = requests.utils.requote_uri(torrent_page + string_search)
    if page == '1337x':
        return(url + '/1/')
    elif page == 'limetorrents':
        return(url + '/')
    else:
        return(url)


def get_content():
    """Get content of the page through url."""
    url = build_url()
    try:
        global content_page
        content_page = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.info('\nAn error has ocurred: \n' + str(e))
        logging.error(traceback.format_exc())
        raise SystemExit()


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
        get_content()
        select_torrent()
        download_torrent()
        next_step()


if __name__ == '__main__':
    try:
        run_it()
    except KeyboardInterrupt:
        print('\nSee you the next time.')
    except:
        print("\nAn error has ocurred: \n")
        logging.debug(traceback.format_exc())
    finally:
        logging.info("Good bye!")
