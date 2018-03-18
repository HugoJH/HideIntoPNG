#!/usr/bin/env python

from setuptools import setup

config = { 'name': 'HideIntoPNG',
           'version': '0.1',
           'description': 'Encrypt and embed a File and its name inside a PNG File as custom PNG chunks',
           'author': 'Hugo Jiménez Hernández',
           'author_email': 'hjimenezhdez@gmail.com',
           'url': 'https://github.com/HugoJH/HideIntoPNG',
           'entry_points': {
              'console_scripts': ['hip = hideintopng.__main__:main']
           },
         }
setup(**config)
