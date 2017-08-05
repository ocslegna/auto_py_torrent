#!/usr/bin/env python3

import os
import sys


from codecs import open

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

packages = ['auto_py_torrent']

requires = [
    'requests>=2.18.1',
    'beautifulsoup4>=4',
    'tabulate>=0.7.7',
    'coloredlogs>=7.1',
    'lxml'
]

about = {}
with open(os.path.join(here, 'auto_py_torrent', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    python_requires='>=3',
    install_requires=requires,
    license=about['__license__'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Terminals',
    ),
    keywords='automate torrent torrent downloads',
    entry_points={
        'console_scripts': ['auto_py_torrent=auto_py_torrent.auto_py_torrent:main'],
    }
)
