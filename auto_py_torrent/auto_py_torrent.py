#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""auto_py_torrent.

This module provides utilities to download a torrent within specific types.
"""

# Author: Gabriel Scotillo
# URL: https://github.com/ocslegna/auto_py_torrent
# Please do not download illegal torrents or torrents that you do not have
#     permission to own.
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


MODES = 'best_rated list'.split()

# {'torrentz2':
#  {'page': 'https://torrentz2.eu/search?f=',
#   'key_search': 'did not match'}},
# {'rarbg':
#  {'page': 'https://rarbg.to/torrents.php?search=',
#   'key_search': '<div id="pager_links"></div>'}},

TORRENTS = ({'torrent_project':
             {'page': 'https://torrentproject.se/?t=',
              'key_search': 'No results',
              'domain': 'https://torrentproject.se'}},
            {'the_pirate_bay':
             {'page': 'https://proxyspotting.in/s/?q=',
              'key_search': 'No hits',
              'domain': 'https://proxyspotting.in'}},
            {'1337x':
             {'page': 'https://1337x.to/search/',
              'key_search': 'No results were returned',
              'domain': 'https://1337x.to'}},
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
              'domain': 'https://isohunt.to'}})
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
    PINK = '\033[95m'
    PURPLE = '\033[35m'
    LIGHTBLUE = '\033[94m'
    LGREEN = '\033[0m\033[32m'
    LIGHTCYAN = '\033[0m\033[36m'
    LRED = '\033[0m\033[31m'
    LIGHTPURPLE = '\033[0m\033[35m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


def get_parser():
    """Load parser for command line arguments.

    It parses argv/input into args variable.
    """
    desc = Colors.LIGHTBLUE + textwrap.dedent(
        '''\
        Welcome to
                      _                           _                            _
           __ _ _   _| |_ ___      _ __  _   _   | |_ ___  _ __ _ __ ___ _ __ | |_
          / _` | | | | __/ _ \    | '_ \| | | |  | __/ _ \| '__| '__/ _ \ '_ \| __|
         | (_| | |_| | || (_) |   | |_) | |_| |  | || (_) | |  | | |  __/ | | | |_
          \__,_|\__,_|\__\___/____| .__/ \__, |___\__\___/|_|  |_|  \___|_| |_|\__|
                            |_____|_|    |___/_____|

        ------------------------------------
          auto_py_torrent is an automated tool for download files by obtaining
        torrents or magnets that are in different provided pages that the
        user can choose.

          Its goal is to make it easier for users to find the files they want
        and download them instantly.

          An auto_py_torrent command is provided in which the user can
        currently choose between two modes, best_rated and list mode, then it
        selects one of the torrent tracking pages for multimedia content and
        finally enter the text of what you want to download.
        ------------------------------------
        ''') + Colors.ENDC
    usage_info = Colors.LGREEN + textwrap.dedent(
        '''\

        Use "%(prog)s --help" for more information.
        Examples:
            use "%(prog)s MODE SELECTED_PAGE STRING_TO_SEARCH # generic.
            use "%(prog)s 0 0 "The simpsons" # best rated.
            use "%(prog)s 1 0 "The simpsons" # list rated.

        Mode options:
            0: best_rated. # Download the most rated file.
            1: list. # Get a list, and select one of them.

        Page list options:
            0: torrent project.
            1: the pirate bay.
            2: 1337x.
            3: eztv.
            4: limetorrents.
            5: isohunt.
        ''') + Colors.ENDC
    epi = Colors.LIGHTPURPLE + textwrap.dedent(
        '''\
        -> Thanks for using auto_py_torrent!
        ''') + Colors.ENDC

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
                        help='Select mode of file download.\n'
                             '    e.g: 0(rated) or 1(list).')
    parser.add_argument('torr_page', action='store',
                        choices=range(len(TORRENTS)),
                        type=int,
                        help='Select tracking page to download from.\n'
                             '    e.g: 0 to .. ' + str(len(TORRENTS)-1) + '.')
    parser.add_argument('str_search', action='store',
                        type=str,
                        help='Input torrent string to search.\n'
                             '    e.g: "String search"')
    return(parser)


def is_num(var):
    """Check if var string is num. Should use it only with strings."""
    try:
        int(var)
        return True
    except ValueError:
        return False


class AutoPy:
    """AutoPy class for instance variables."""

    def __init__(self, args, string_search, mode_search,
                 page, key_search, torrent_page, domain):
        """Args not entered will be defaulted."""
        self.args = args
        self.back_to_menu = False
        self.content_page = None
        self.domain = domain
        self.elements = None
        self.found_torrents = False
        self.hrefs = []
        self.keep_search = True
        self.key_search = key_search
        self.magnet = ""
        self.mode_search = mode_search
        self.page = page
        self.picked_choice = False
        self.selected = ""
        self.string_search = string_search
        self.table = None
        self.torrent = ""
        self.torrent_page = torrent_page

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
            print('Wrong page to get magnet!')
            sys.exit(1)

    def download_torrent(self):
        """Download torrent.

        Rated implies download the unique best rated torrent found.
        Otherwise: get the magnet and download it.
        """
        try:
            if self.back_to_menu is True:
                return
            if self.found_torrents is False:
                print('Nothing found.')
                return
            if self.mode_search == 'best_rated':
                print('Downloading..')
                self.open_magnet()
            elif self.mode_search == 'list':
                if self.selected is not None:
                    # t_p, pirate and 1337x got magnet inside, else direct.
                    if self.page in ['eztv', 'limetorrents']:
                        self.magnet = self.hrefs[int(self.selected)]
                        print('Downloading..')
                        self.open_magnet()
                    elif self.page in ['the_pirate_bay',
                                       'torrent_project',
                                       '1337x',
                                       'isohunt']:
                        url = self.hrefs[int(self.selected)]
                        self.get_magnet(url)
                        print('Downloading..')
                        self.open_magnet()
                    else:
                        print('Bad selected page.')
                else:
                    print('Nothing selected.')
                    sys.exit(1)
        except Exception:
            print(traceback.format_exc())
            sys.exit(0)

    def build_table(self):
        """Build table."""
        headers = ['Title', 'Seeders', 'Leechers', 'Age', 'Size']
        titles = []
        seeders = []
        leechers = []
        ages = []
        sizes = []

        if self.page == 'torrent_project':
            titles = [list(span.find('a').stripped_strings)[0]
                      for span in self.elements[0]]

            seeders = [span.get_text() for span in self.elements[1]]
            leechers = [span.get_text() for span in self.elements[2]]
            ages = [span.get_text() for span in self.elements[3]]
            sizes = [span.get_text() for span in self.elements[4]]

            # Torrents
            self.hrefs = [self.domain +
                          span.find('a')['href']
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
                # Torrent
                href = self.domain + \
                    elem.find('a', title=re.compile('magnet'))['href']
                self.hrefs.append(str(href))

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

        self.table = [[Colors.BOLD +
                       UnicodeDammit(titles[i][:75].strip(), ["utf-8"]).unicode_markup +
                       Colors.ENDC
                       if (i + 1) % 2 == 0
                       else UnicodeDammit(
                           titles[i][:75].strip()).unicode_markup,
                       Colors.SEEDER + seeders[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LGREEN + seeders[i].strip() + Colors.ENDC,
                       Colors.LEECHER + leechers[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LRED + leechers[i].strip() + Colors.ENDC,
                       Colors.LIGHTBLUE + ages[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.BLUE + ages[i].strip() + Colors.ENDC,
                       Colors.PINK + sizes[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.PURPLE + sizes[i].strip() + Colors.ENDC]
                      for i in range(len(self.hrefs))]

        print(tabulate(self.table,
                       headers=headers,
                       tablefmt='psql',
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
            if self.mode_search == 'best_rated':
                rated_url = self.domain + \
                    main.find(href=re.compile('torrent.html'))['href']
                self.get_magnet(rated_url)
            else:
                divs = main.find_all('div', limit=30)[2:]
                self.elements = list(
                    zip(*[d.find_all('span', recursive=False)
                          for d in divs]))  # Torrents

        elif self.page == 'the_pirate_bay':
            main = soup.find('table', {'id': 'searchResult'})
            if self.mode_search == 'best_rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile('torrent'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*[tr.find_all('td', recursive=False)[1:]
                          for tr in trs]))  # Magnets

        elif self.page == '1337x':
            main = soup.find('table', {'class': 'table'})
            if self.mode_search == 'best_rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile('torrent'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*([tr.find_all('td', recursive=False)[:-1]
                           for tr in trs])))  # Torrents

        elif self.page == 'eztv':
            main = soup.find_all('table', {'class': 'forum_header_border'})[2]
            if self.mode_search == 'best_rated':
                self.magnet = main.find('a', href=re.compile('magnet'))['href']
            else:
                trs = main.find_all('tr', limit=30)[2:]
                self.elements = list(
                    zip(*([tr.find_all('td', recursive=False)[1:-1]
                           for tr in trs])))  # Magnets

        elif self.page == 'limetorrents':
            main = soup.find('table', {'class': 'table2'})
            if self.mode_search == 'best_rated':
                self.magnet = main.find(
                    'a', href=re.compile('torrent'))['href']
            else:
                trs = main.find_all('tr', limit=30)[1:]
                self.elements = list(
                    zip(*([tr.find_all('td', recursive=False)[:-1]
                           for tr in trs])))  # Magnets

        elif self.page == 'isohunt':
            main = soup.find('table', {'class': 'table'})
            if self.mode_search == 'best_rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile(
                        'torrent_details'))['href']
                self.get_magnet(rated_url)
            else:
                trs = main.find_all('tr', limit=30)[1:-1]
                self.elements = list(
                    zip(*([tr.find_all('td', recursive=False)[1:-1]
                           for tr in trs])))  # Torrent
        else:
            print('Cannot soupify current page. Try again.')

    def handle_select(self):
        """Handle user's input in list mode."""
        self.selected = input('>> ')
        if self.selected in ['Q', 'q']:
            sys.exit(1)
        elif self.selected in ['B', 'b']:
            self.back_to_menu = True
            return True
        elif is_num(self.selected):
            if 0 <= int(self.selected) <= len(self.hrefs) - 1:
                self.back_to_menu = False
                return True
            else:
                print(Colors.FAIL +
                      'Wrong index. ' +
                      'Please select an appropiate one or other option.' +
                      Colors.ENDC)
                return False
        else:
            print(Colors.FAIL +
                  'Invalid input. ' +
                  'Please select an appropiate one or other option.' +
                  Colors.ENDC)
            return False

    def select_torrent(self):
        """Select torrent.

        First check if specific element/info is obtained in content_page.
        Specify to user if it wants best rated torrent or select one from list.
        If the user wants best rated: Directly obtain magnet/torrent.
        Else: build table with all data and enable the user select the torrent.
        """
        try:
            self.found_torrents = not bool(self.key_search in
                                           self.content_page.text)
            if not self.found_torrents:
                print('No torrents found.')
                sys.exit(1)
            self.soupify()
            if self.mode_search == 'list':
                self.build_table()
                if len(self.hrefs) == 1:
                    print('Press "0" to download it.')
                elif len(self.hrefs) >= 2:
                    print('\nSelect one of the following torrents. ' +
                          'Enter a number between: 0 and ' +
                          str(len(self.hrefs) - 1))

                print('If you want to exit write "' +
                      Colors.LRED + 'Q' + Colors.ENDC + '" or "' +
                      Colors.LRED + 'q' + Colors.ENDC + '".')
                print('If you want to go back to menu and search again write "' +
                      Colors.LGREEN + 'B' + Colors.ENDC + '" or "' +
                      Colors.LGREEN + 'b' + Colors.ENDC + '".')
                while not(self.picked_choice):
                    self.picked_choice = self.handle_select()
        except Exception:
            print('ERROR select_torrent: ')
            logging.error(traceback.format_exc())
            sys.exit(0)

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
            if not(self.content_page.status_code == requests.codes.ok):
                self.content_page.raise_for_status()
        except requests.exceptions.RequestException as ex:
            logging.info('A requests exception has ocurred: ' + str(ex))
            logging.error(traceback.format_exc())
            sys.exit(0)


def insert(args):
    """Insert args values into instance variables."""
    string_search = args.str_search
    mode_search = MODES[args.mode]
    page = list(TORRENTS[args.torr_page].keys())[0]
    key_search = TORRENTS[args.torr_page][page]['key_search']
    torrent_page = TORRENTS[args.torr_page][page]['page']
    domain = TORRENTS[args.torr_page][page]['domain']
    return([args, string_search, mode_search, page,
            key_search, torrent_page, domain])


def initialize():
    """Initialize script."""
    print("Welcome to auto_py_torrent!\n")


def run_it():
    """Search and download torrents until the user says it so."""
    initialize()
    parser = get_parser()
    args = None
    first_parse = True
    while(True):
        if first_parse is True:
            first_parse = False
            args = parser.parse_args()
        else:
            print(textwrap.dedent(
                '''\
                Search again like in the beginning.
                  -- You can either choose best rated or list mode.
                  -- This time, you can insert the search string without double quotes.
                  Remember the list mode options!
                    0: torrent project.
                    1: the pirate bay.
                    2: 1337x.
                    3: eztv.
                    4: limetorrents.
                    5: isohunt.
                '''))

            print('Or.. if you want to exit just write "' +
                  Colors.LRED + 'Q' + Colors.ENDC + '" or "' +
                  Colors.LRED + 'q' + Colors.ENDC + '".')
            input_parse = input('>> ').replace("'", "").replace('"', '')
            if input_parse in ['Q', 'q']:
                sys.exit(1)

            args = parser.parse_args(input_parse.split(' ', 2))

        if args.str_search.strip() == "":
            print('Please insert an appropiate non-empty string.')
        else:
            auto = AutoPy(*insert(args))
            auto.get_content()
            auto.select_torrent()
            auto.download_torrent()


def main():
    """Entry point for app script."""
    try:
        run_it()
    except KeyboardInterrupt:
        print('\nSee you the next time.')
    except Exception:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
