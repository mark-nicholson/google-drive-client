#!/usr/bin/python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# slurp the configuration
gauth = GoogleAuth('settings.yaml')

# check to see if we need manual intervention
if not gauth.credentials or gauth.credentials.invalid:
    gauth.LocalWebserverAuth()

# build the service
drive = GoogleDrive(gauth)

# quick query test
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
print("List: %d" % len(file_list))

# results ...
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
