#!/usr/bin/python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# hard override...  tidy this up with yaml?
GoogleAuth.DEFAULT_SETTINGS = {
    'client_config_backend': 'file',
    'client_config_file': 'client_secret.json',
    'oauth_scope': ['https://www.googleapis.com/auth/drive'],
    'save_credentials': True,
    'save_credentials_backend': 'file',
    'save_credentials_file': 'creds.json'
}



gauth = GoogleAuth()
#gauth = GoogleAuth('/work/mjn/gDriveClient/.gdriveclient/settings.yaml' )
print("Here 1")
#pp.pprint(gauth)

#gauth.LoadClientConfigFile('/work/mjn/gDriveClient/.gdriveclient/client_secrets.json')
#gauth.LoadClientConfigSettings() #'/work/mjn/gDriveClient/.gdriveclient/settings.yaml')
print("Here 2")

#gauth.LoadCredentialsFile('/work/mjn/gDriveClient/.gdriveclient/credentials.json')
print("Here 3")
if not gauth.credentials or gauth.credentials.invalid:
    #gauth.LocalWebserverAuth('localhost', [8090])
    gauth.LocalWebserverAuth()

#gauth.Authorize()
#gauth.ServiceAuth()
print("Here 4")

drive = GoogleDrive(gauth)
print("Here 5")

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
print("List: %d" % len(file_list))

for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
