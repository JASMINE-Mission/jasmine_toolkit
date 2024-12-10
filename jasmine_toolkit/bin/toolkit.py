#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Executable command for JASMINE Toolkit '''


__description__ = '''JASMINE Toolkit command'''


def setup_dump_table(parser):
  from jasmine_toolkit.utils.table import dump_table
  from jasmine_toolkit.utils.table import setup_parser

  setup_parser(parser)
  parser.set_defaults(handler=dump_table)


def main():
    import sys
    from argparse import ArgumentParser as ap

    parser = ap(__description__)

    subparser = parser.add_subparsers(required=True)

    parser_table = subparser.add_parser(
        'table', help='dump Parameters')

    setup_dump_table(parser_table)

    args = parser.parse_args(sys.argv[1:])

    if hasattr(args, 'handler'):
        args.handler(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
