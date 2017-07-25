#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""auto_py_torrent.

This module provides utilities to download a torrent within specific types.

"""


# Author: Gabriel Scotillo
# URL: https://github.com/ocslegna/auto_py_torrent
# Please do not download illegal torrents or torrents that you do not have
#     permisson to own.
# This tool is for educational purposes only. Any damage you make will not
#     affect the author.


import os
import subprocess
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


MODES = ['best_rated', 'list']

# NOTE: isohunt is down.
TORRENTS = [{'torrent_project':
             {'page': 'https://torrentproject.se/?t=',
              'key_search': 'No results',
              'domain': 'https://torrentproject.se'}},
            {'the_pirate_bay':
             {'page': 'https://proxyspotting.in/s/?q=',
              'key_search': 'No hits',
              'domain': 'https://proxyspotting.in'}},
            {'torrentz2':
             {'page': 'https://torrentz2.eu/search?f=',
              'key_search': 'did not match'}},
            {'rarbg':
             {'page': 'https://rarbg.to/torrents.php?search=',
              'key_search': '<div id="pager_links"></div>'}},
            {'1337x':
             {'page': 'https://1337x.to/search/',
              'key_search': 'No results were returned',
              'domain': 'https://1337.to'}},
            {'eztv':
             {'page': 'https://eztv.ag/search/',
              'key_search': 'It does not have any.',
              'domain': 'https://eztv.ag'}},
            {'limetorrents':
             {'page': 'https://www.limetorrents.cc/search/all/',
              'key_search': 'No results found',
              'domain': 'https://www.limetorrents.cc'}},
            {'isohunt':
             {'page': 'https://isohunt.to/torrents/?ihq=',
              'key_search': 'No results found',
              'domain': 'https://isohunt.to'}}]
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
coloredlogs.install()


class Colors:
    """Color class container."""

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


class AutoPy:
    """AutoPy class for instance variables."""

    def __init__(self, args=None, content_page=None, found=False, hrefs=None,
                 magnet="", mode_search="", keep_search=True, key_search="",
                 page="", selected="", string_search="", elements=None,
                 table=None, torrent="", torrent_page="", domain=""):
        """Args not entered will be defaulted."""
        self.args = args
        self.content_page = content_page
        self.found = found
        self.hrefs = hrefs
        self.magnet = magnet
        self.mode_search = mode_search
        self.keep_search = keep_search
        self.key_search = key_search
        self.page = page
        self.selected = selected
        self.string_search = string_search
        self.elements = elements
        self.table = table
        self.torrent = torrent
        self.torrent_page = torrent_page
        self.domain = domain

    def next_step(self):
        """Decide what will be continued."""
        pass

    def open_magnet(self):
        """Open magnet according to os."""
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', self.magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif sys.platform.startswith('win32'):
            os.startfile(self.magnet)
        elif sys.platform.startswith('cygwin'):
            os.startfile(self.magnet)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', self.magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.Popen(['xdg-open', self.magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_magnet(self, url):
        """Get magnet from torrent page. Url already got domain."""
        content_most_rated = requests.get(url)
        rated_soup = BeautifulSoup(content_most_rated.content, 'lxml')

        if self.page == 'torrent_project':
            self.magnet = rated_soup.find(
                'a', href=True, text=re.compile('Download'))['href']

        elif self.page == 'the_pirate_bay':
            self.magnet = rated_soup.find(
                'a', href=True, text=re.compile('Get this torrent'))['href']

        elif self.page == '1337x':
            div1337 = rated_soup.find(
                'div', {'class': 'torrent-category-detail'})
            self.magnet = div1337.find('a', href=re.compile('magnet'))['href']

        elif self.page == 'isohunt':
            self.magnet = rated_soup.find(
                'a', href=re.compile('magnet'))['href']

        else:
            logging.info('Wrong page to get magnet!')
            raise SystemExit()

    def download_torrent(self):
        """Download torrent.

        Rated implies download  the unique best rated torrent found.
        Otherwise: download the selected torrent.
        """
        try:
            if not(self.found):
                logging.info('Nothing found.')
                return

            if self.mode_search == 'rated':
                self.open_magnet()
            elif self.mode_search == 'list':
                if self.selected is not None:
                    if self.page in ['eztv', 'limetorrents']:
                        self.magnet = self.hrefs[int(self.selected)]
                        self.open_magnet()
                    elif self.page in ['the_pirate_bay', 'torrent_project',
                                       '1337x', 'isohunt']:
                        # torr_proj, pirate and 1337x got  magnet inside.
                        url = self.hrefs[int(self.selected)]
                        self.get_magnet(url)
                        self.open_magnet()
                    else:
                        print('Bad selected page.')
                else:
                    logging.info('Nothing selected.')
                    raise SystemExit()
        except:
            logging.info('\nAn error has ocurred: \n')
            logging.error(traceback.format_exc())
            raise SystemExit()

    def build_table(self):
        """Build table."""
        headers = ['Title', 'Seeders', 'Leechers', 'Age', 'Size']
        titles = []
        seeders = []
        leechers = []
        ages = []
        sizes = []

        if self.page == 'torrent_project':
            titles = [span.find('a').get_text()
                      for span in self.elements[0]]
            seeders = [span.get_text() for span in self.elements[1]]
            leechers = [span.get_text() for span in self.elements[2]]
            ages = [span.get_text() for span in self.elements[3]]
            sizes = [span.get_text() for span in self.elements[4]]

            # Torrents
            self.hrefs = [self.domain +
                          span.find(href=re.compile('torrent.html'))['href']
                          for span in self.elements[0]]

        elif self.page == 'the_pirate_bay':
            for elem in self.elements[0]:
                title = elem.find('a', {'class': 'detLink'}).get_text()
                titles.append(title)

                font_text = elem.find(
                    'font', {'class': 'detDesc'}).get_text()
                dammit = UnicodeDammit(font_text)
                age, size = dammit.unicode_markup.split(',')[:-1]
                ages.append(age)
                sizes.append(size)

                # Torrents
                href = self.domain + \
                    elem.find('a', title=re.compile('magnet'))['href']
                self.hrefs.append(href)

            seeders = [elem.get_text() for elem in self.elements[1]]
            leechers = [elem.get_text() for elem in self.elements[2]]

        elif self.page == '1337x':
            titles = [elem.get_text() for elem in self.elements[0]]
            seeders = [elem.get_text() for elem in self.elements[1]]
            leechers = [elem.get_text() for elem in self.elements[2]]
            ages = [elem.get_text() for elem in self.elements[3]]
            sizes = [elem.get_text('|').split('|')[0]
                     for elem in self.elements[4]]

            # Torrent
            self.hrefs = [self.domain +
                          elem.find(href=re.compile('torrent'))['href']
                          for elem in self.elements[0]]

        elif self.page == 'eztv':
            titles = [elem.get_text() for elem in self.elements[0]]
            seeders = [elem.get_text() for elem in self.elements[4]]
            leechers = ['-' for elem in self.elements[4]]
            ages = [elem.get_text() for elem in self.elements[3]]
            sizes = [elem.get_text() for elem in self.elements[2]]

            # Magnets
            self.hrefs = [elem.find(href=re.compile('magnet'))['href']
                          for elem in self.elements[1]]

        elif self.page == 'limetorrents':
            titles = [elem.get_text() for elem in self.elements[0]]
            seeders = [elem.get_text() for elem in self.elements[3]]
            leechers = [elem.get_text() for elem in self.elements[4]]
            ages = [elem.get_text() for elem in self.elements[1]]
            sizes = [elem.get_text() for elem in self.elements[2]]

            # Magnets
            self.hrefs = [elem.find('a', href=re.compile('torrent'))['href']
                          for elem in self.elements[0]]

        elif self.page == 'isohunt':
            titles = [elem.get_text() for elem in self.elements[0]]
            seeders = [elem.get_text() for elem in self.elements[5]]
            leechers = ['-' for elem in self.elements[5]]
            ages = [elem.get_text() for elem in self.elements[3]]
            sizes = [elem.get_text() for elem in self.elements[4]]

            # Torrents
            self.hrefs = [self.domain +
                          elem.find(href=re.compile('torrent_details'))['href']
                          for elem in self.elements[0]]
        else:
            print('Error page')

        self.table = [[Colors.BOLD + titles[i] + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else titles[i],
                       Colors.SEEDER + seeders[i] + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LIGHTGREEN + seeders[i] + Colors.ENDC,
                       Colors.LEECHER + leechers[i] + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LIGHTRED + leechers[i] + Colors.ENDC,
                       Colors.BLUE + ages[i] + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LIGHTBLUE + ages[i] + Colors.ENDC,
                       Colors.PURPLE + sizes[i] + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LIGHTPURPLE + sizes[i] + Colors.ENDC]
                      for i in range(len(self.hrefs))]

        print(tabulate(self.table,
                       headers=headers,
                       tablefmt='fancy_grid',
                       numalign='right',
                       stralign='left',
                       showindex=True))

    def soupify(self):
        """Get proper torrent/magnet information.

        If search_mode is rated then get torrent/magnet.
        If not, get all the elements to build the table.
        There are different ways for each page.
        """
        soup = BeautifulSoup(self.content_page.content, 'lxml')
        if self.page == 'torrent_project':
            main = soup.find('div', {'id': 'similarfiles'})
            if self.mode_search == 'rated':
                rated_url = self.domain + \
                    main.find(href=re.compile('torrent.html'))['href']
                self.get_magnet(rated_url)
            else:
                divs = main.find_all('div', limit=30)[1:]
                self.elements = list(
                    zip(*[d.find_all('span') for d in divs]))  # Torrents

        elif self.page == 'the_pirate_bay':
            main = soup.find('table', {'id': 'searchResult'})
            if self.mode_search == 'rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile('torrent'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*[tr.find_all('td')[1:] for tr in trs]))  # Magnets

        elif self.page == '1337x':
            main = soup.find('table', {'class': 'table'})
            if self.mode_search == 'rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile('torrent'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*([tr.find_all('td')[:-1] for tr in trs])))  # Torrents

        elif self.page == 'eztv':
            main = soup.find('table', {'class': 'forum_header_border'})
            if self.mode_search == 'rated':
                self.magnet = main.find('a', {'class': 'magnet'})['href']
            else:
                trs = main.find_all('tr', limit=30)[2:]
                self.elements = list(
                    zip(*([tr.find_all('td')[1:-1] for tr in trs])))  # Magnets

        elif self.page == 'limetorrents':
            main = soup.find('table', {'class': 'table2'})
            if self.mode_search == 'rated':
                self.magnet = main.find(
                    'a', href=re.compile('torrent'))['href']
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*([tr.find_all('td')[:-1] for tr in trs])))  # Magnets

        elif self.page == 'isohunt':
            main = soup.find('table', {'class': 'table'})
            if self.mode_search == 'rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile(
                        'torrent_details'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:-1]
                self.elements = list(
                    zip(*([tr.find_all('td')[1:-1] for tr in trs])))  # Torrent
        else:
            logging.info('Cannot soupify current page. Try again.')

    def select_torrent(self):
        """Select torrent.

        First check if specific element/info is obtained in content_page.
        Specify to user if it wants best rated torrent or select one from list.
        If the user wants best rated: Directly obtain magnet/torrent.
        Else: build table with all data and enable the user select the torrent.
        """
        try:
            self.found = bool(self.key_search not in self.content_page)

            if not(self.found):
                logging.info('No torrents found.')
                return
            self.soupify()
            if self.mode_search != "rated":
                self.build_table()
                logging.info('Select one of the following torrents.')
                logging.info(
                    'Enter a number between: 0 and ' + len(self.hrefs))
                logging.info('If you want to exit write "Q".')
                self.selected = input('>> ')
                if self.selected in ['Q', 'q']:
                    logging.info('\nGood bye!')
                    raise SystemExit()
                elif 0 <= int(self.selected) <= len(self.hrefs):
                    pass
                else:
                    logging.info('Wrong index.')
                    self.selected = None

        except:
            logging.info('\nAn error has ocurred: \n')
            logging.error(traceback.format_exc())
            raise SystemExit()

    def build_url(self):
        """Build appropiate encoded URL.

        This implies the same way of searching a torrent as in the page itself.
        """
        url = requests.utils.requote_uri(
            self.torrent_page + self.string_search)
        if self.page == '1337x':
            return(url + '/1/')
        elif self.page == 'limetorrents':
            return(url + '/')
        else:
            return(url)

    def get_content(self):
        """Get content of the page through url."""
        url = self.build_url()
        try:
            self.content_page = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.info('\nAn error has ocurred: \n' + str(e))
            logging.error(traceback.format_exc())
            raise SystemExit()


def insert(args):
    """Insert args values into instance variables."""
    page = list(TORRENTS[args.torr_page].keys())[0]
    mode_search = MODES[args.mode]
    torrent_page = TORRENTS[args.torr_page]['page']
    string_search = args.str_search
    key_search = TORRENTS[args.torr_page]['key_search']
    domain = TORRENTS[args.torr_page]['domain']
    return([page, mode_search, torrent_page,
            string_search, key_search, domain])


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
                        choices=range(len(MODES)),
                        type=int,
                        help='Select mode of torrent download.\n'
                             'e.g: 0 or 1')
    parser.add_argument('torr_page', action='store',
                        choices=range(len(TORRENTS)),
                        type=int,
                        help='Select torrent page to download from.\n'
                             'e.g: 0 or 1 or .. N')
    parser.add_argument('str_search', action='store',
                        type=str,
                        help='Input torrent string to search.\n'
                             'e.g: "String search"')
    return(parser.parse_args())


def run_it():
    """Search and download torrents until the user says it so."""
    initialize()
    args = parse()  # TODO: Parse input as ARGS.
    auto = AutoPy(*insert(args))
    while(auto.keep_search):
        auto.get_content()
        auto.select_torrent()
        auto.download_torrent()
        auto.next_step()


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
