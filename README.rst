auto_py_torrent
###############

**auto_py_torrent** is an automated tool for download files by obtaining torrents or magnets that are in different provided pages that the user can choose.

Its goal is to make it easier for users to find the files they want and download them instantly.
  
An ``auto_py_torrent`` command is provided in which the user can currently choose between two modes, ``best_rated`` and ``list`` mode, then it selects one of the torrent tracking pages for multimedia content and finally enter the text of what you want to download.

We Can ``List`` It Out!

.. image:: https://user-images.githubusercontent.com/6371898/28991985-b72c0340-7967-11e7-97a2-c33d96d43706.png
    :target: https://github.com/ocslegna/auto_py_torrent/



With a Little ``Help`` from My Friends!

.. image:: https://user-images.githubusercontent.com/6371898/28991984-b46bb402-7967-11e7-9d39-9f8b55362ac9.png
    :target: https://github.com/ocslegna/auto_py_torrent/



.. contents::

.. section-numbering::

Main features
=============

* Simple and easy search, for file downloads using torrent.
* Formatted and colorized terminal output.


Installation and an usage example.
==================================

First, check your python3 version.
----------------------------------

.. code-block:: bash

    $ python3 --version

Upgrade it as you wish.


Install ``python3-pip``:
------------------------

``Mac``
~~~~~~~
.. code-block:: bash

    $ brew install python3

``Linux``
~~~~~~~~
Using the package manager with different linux distributions:

.. code-block:: bash

    # Ubuntu/Debian.
    $ sudo apt-get update
    $ sudo apt-get install -y python3-pip    

.. code-block:: bash

    # Fedora, CentOS, RHEL.
    $ sudo dnf install python3-pip

.. code-block:: bash

    # Arch.
    $ pacman -S python3-pip


``Windows``
~~~~~~~~~~~

If ``C:\path\to\python\Scripts\pip3`` is not there remite to:

* `<https://www.python.org/downloads/windows/>`_
  for Windows download.


Install virtualenv if necessary and activate it.
------------------------------------------------

.. code-block:: bash

    $ sudo pip3 install virtualenv
    $ cd
    $ virtualenv venv_auto_py
    $ cd venv_auto_py
    $ source bin/activate


Install auto_py_torrent and get an example!
-------------------------------------------

.. code-block:: bash

    # With virtual env activated:
    $ pip3 install auto_py_torrent
    
    # Without virtual env:
    $ sudo pip3 install auto_py_torrent
    
    # This way you are getting a detail list of results from ``torrent_project`` site.
    $ auto_py_torrent 1 0 "The simpsons"


Usage
=====
.. code-block:: bash

    $ auto_py_torrent MODE SELECTED_PAGE STRING_TO_SEARCH


See also ``auto_py_torrent --help``.


Examples
--------

Using ``best_rated`` mode with ``torrent_project`` page:

.. code-block:: bash

    $ auto_py_torrent 0 0 "The simpsons"


Using ``list`` mode with ``the pirate bay`` page:

.. code-block:: bash

    $ auto_py_torrent 1 1 "The simpsons"


Meta
====

Dependencies
------------

**auto_py_torrent** uses this incredibles libraries:

* `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup//>`_
  — Python library for pulling data out of HTML and XML files.
* `Requests <http://docs.python-requests.org/en/master/>`_
  — Requests is an elegant and simple HTTP library for Python, built for human beings.
* `Tabulate <https://bitbucket.org/astanin/python-tabulate>`_
  — Python library for tabular data print in Python, a library and a command-line utility.
* `Coloredlogs <https://pypi.python.org/pypi/coloredlogs/>`_
  — Python package that enables colored terminal output for Python’s logging module.
* `lxml <http://lxml.de/>`_
  — Python library for processing XML and HTML in the Python language.


Release History
---------------

See `HISTORY <https://github.com/ocslegna/auto_py_torrent/blob/master/HISTORY.rst>`_.


Licence
-------

MIT: `LICENSE <https://github.com/ocslegna/auto_py_torrent/blob/master/LICENSE>`_.


Author
-------

`Gabriel Scotillo`_  (`@gabrielscotillo`_)


Package index
-------------

`<https://pypi.python.org/pypi/auto-py-torrent>`_.


.. _Gabriel Scotillo: https://ocslegna.herokuapp.com
.. _@gabrielscotillo: https://twitter.com/gabrielscotillo
