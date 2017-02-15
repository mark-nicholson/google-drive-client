#!/usr/bin/python3
#
# Top level tool for Google Drive Client
#

import sys
import argparse

from gDrive.gdcExceptions import *

parser = argparse.ArgumentParser(prog="gdt")
parser.add_argument('-n', '--dry-run', action='store_true', help='simulate what would happen')
subparsers = parser.add_subparsers(help='sub-command help')

from gDrive.create import add_subparser as subparser_create
subparser_create(subparsers)

from gDrive.pull import add_subparser as subparser_pull
subparser_pull(subparsers)

parser_update = subparsers.add_parser('update', help='update a new gDrive map')
parser_update.add_argument('--force', help='clobber anything incorrect locally')

parser_sync = subparsers.add_parser('sync', help='sync gDrive')
parser_sync.add_argument('--force', help='clobber anything incorrect locally')


flags = parser.parse_args()

print(flags)

# global catcher. Format exceptions consistently.
debug = False

if debug:
    flags.func(flags)
else:
    try:
        flags.func(flags)
    except gdcSuccess as e:
        print("Success!")
    except gdcException as e:
        print("Error: " + str(e))
    except:
        print("Failed to complete")

        # original
        #e = sys.exc_info()[0]
        #print(e)

        #debug
        import traceback
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)
        
