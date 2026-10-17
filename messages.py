#!/usr/bin/env python3
"""Manage gettext messages.

Usage:
  messages.py extract
  messages.py init <locale>
  messages.py update
  messages.py compile
  messages.py (-h | --help)
"""
from babel.messages.frontend import CommandLineInterface
from docopt import docopt


def messages(arguments):
    cli = CommandLineInterface()
    if arguments['extract']:
        cli.run([
            "pybabel",
            "extract",
            "--charset=UTF-8",
            "-o", "archmaster/locales/messages.pot",
            "archmaster",
        ])
    elif arguments['init']:
        cli.run([
            "pybabel",
            "init",
            "-i", "archmaster/locales/messages.pot",
            "-d", "archmaster/locales",
            "-l", arguments['<locale>']
        ])
    elif arguments['update']:
        cli.run([
            "pybabel",
            "update",
            "-i", "archmaster/locales/messages.pot",
            "-d", "archmaster/locales",
        ])
    elif arguments['compile']:
        cli.run([
            "pybabel",
            "compile",
            "-d", "archmaster/locales",
        ])


if __name__ == '__main__':
    arguments = docopt(__doc__)
    messages(arguments)
