#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Tool for automate torrent download.
TODO: Fill.
"""

# Author: Gabriel Scotillo
# URL: https://ocslegna.herokuapp.com
# Please do not download illegal torrents or torrents that you do not have permisson to own.
# This tool is for educational purposes only. Any damage you make will not affect the author.


import os
import sys
import re
import requests

from bs4 import BeautifulSoup


keep_search = True
torrents = {'torrent_project': {'key_search': 'No results'},
            'kickass': {'key_search': 'Download torrent'}}
torr_page = ""
str_search = ""
found = False


def next_step():
    """Decide next step of the program."""
    # TODO: do.
    print(1)


def download_torrent():
    """Download torrent."""
    # TODO: do.
    if found:
        # download torrent


def torrents_found(content):
    """Check if specific element/info is obtained."""
    # TODO: Modify first key with selected global input.
    if (torrents["torrent_project"]["key_search"]) is not in content:
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
        """Specify to user if it wants best rated torrent or select one from the list.
        If user wants best rated: change some global bool value for download_torrent.
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
    """User input to search and download torrent."""
    print("Insert torrent page name and string search in different lines: ")
    global torr_page
    torr_page = input()
    global str_search
    str_search = input()


def initialize():
    """Initialize script """
    # TODO: Add all reference for the user here or in insert method.
    print("Welcome to auto_py_torrent!")


def run_it():
    """Search and download torrents until the user says it so."""
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
