#!/usr/bin/python3
#
# Top level tool for Google Drive Client
#

import sys
import os
import argparse

from gDrive.gdcExceptions import *

#
# Default parser along with common options
#
parser = argparse.ArgumentParser(prog="gdt")
parser.add_argument('-n', '--dry-run',
                        action='store_true', help='simulate what would happen')
subparsers = parser.add_subparsers(help='sub-command help')

#
#  Collect the subcommands
#
from gDrive.create import gDriveCreate
gDriveCreate.add_subparser(subparsers)

from gDrive.pull import gDrivePull
gDrivePull.add_subparser(subparsers)

from gDrive.update import gDriveUpdate
gDriveUpdate.add_subparser(subparsers)


flags = parser.parse_args()

print(flags)

#exit(0)

# global catcher. Format exceptions consistently.
debug = False

if debug:
    flags.func(flags)
else:
    try:
        app = flags.object(flags)
        flags.func(app)
    except gdcSuccess as e:
        print("Success!")
    except gdcException as e:
        print("Error: " + str(e))
    except:
        print("Failed to complete")
        print("")
        #debug
        import traceback
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)
        
