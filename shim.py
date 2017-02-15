#!/usr/bin/ipython3
#

import pprint
import IPython

from gDrive.app import gDriveApp

# create a generic app
app = gDriveApp()

# basic query
query = {'q': "'root' in parents and trashed=false"}
file_list = app.drive.ListFile(query).GetList()

# enter a shell
IPython.embed()
