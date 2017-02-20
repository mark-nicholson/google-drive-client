#!/usr/bin/ipython3
#

import pprint
import IPython

from gDrive.app import gDriveApp
from gDrive.pull import gDrivePull
from gDrive.create import gDriveCreate

pp = pprint.PrettyPrinter(indent=4)

appType = 'pull'

# create  app
if appType == 'create':
    app = gDriveCreate({})
elif appType == 'pull':
    app = gDrivePull({})
else:
    app = gDriveApp()
    app._authenticate()

# connect it

# basic query
#query = {'q': "'root' in parents and trashed=false"}
#file_list = app.drive.ListFile(query).GetList()

# enter a shell
IPython.embed()
