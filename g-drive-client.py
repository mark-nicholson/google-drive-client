#!/usr/bin/python3

import argparse

from oauth2client import tools

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

argParser = argparse.ArgumentParser(parents=[tools.argparser])
flags = argParser.parse_args()


rootDir = locate_root()


exit(0)

# slurp the configuration
gauth = GoogleAuth('settings.yaml')

# check to see if we need manual intervention
if not gauth.credentials or gauth.credentials.invalid:
    #gauth.LocalWebserverAuth()
    gauth.CommandLineAuth()

# build the service
drive = GoogleDrive(gauth)

# quick query test
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
print("List: %d" % len(file_list))

# results ...
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
