
import sys
import os
import json
import datetime

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from gDrive import gdcUtils
from gDrive import gdcExceptions


class gDriveApp(object):
    """Parent of all sub-command apps."""

    GDC_FOLDER = '.gdc'
    GDC_CREDENTIALS_FILE = 'credentials.json'
    GDC_CONFIG_FILE = 'config'


    def __init__(self):
        self._root_dir = None
        self._root = None
        self._about = None
        self._config = None

        import gDrive
        self._install_base = gDrive.__file__.rsplit(os.path.sep, 1)[0]

        self._authenticate()

    def root_dir(self):
        if not self._root_dir:
            from gDrive.gdcUtils import locate_root_dir
            self._root_dir = locate_root_dir()
        return self._root_dir

    def about(self):
        if not self._about:
            self._about = self.drive.GetAbout()
        return self._about
        
    def root(self):
        if not self._root:
            about = self.about()
            sf = self.drive.auth.service.files()
            r_md = sf.get(fileId=about['rootFolderId']).execute(http=drive.http)
            self._root = drive.CreateFile(metadata=r_md)
            return self._root

    def get_config_file(self):
        rdir = self.root_dir()
        return os.path.join(rdir, self.GDC_FOLDER, self.GDC_CONFIG_FILE)

    def get_credentials_file(self):
        rdir = self.root_dir()
        return os.path.join(rdir, self.GDC_FOLDER, self.GDC_CREDENTIALS_FILE)

    def config(self):
        if not self._config:
            cfile = self.get_config_file()
            
            fp = open(cfile)
            self._config = json.load(fp)
            fp.close()
            
        return self._config

    def install_base(self):
        return self._install_base
    
    def _authenticate(self, cfg=None, user_authenticate=False):

        # load the config file
        cfg = self.config()

        # base authentication unit
        gauth = GoogleAuth()

        ccf = os.path.join(self.install_base(), 'app-info', 'client_secret.json')
        
        # setup the settings
        gauth.settings['client_config_backend'] = 'file' 
        gauth.settings['client_config_file'] = ccf
        gauth.settings['save_credentials'] = True
        gauth.settings['save_credentials_backend'] = 'file' 
        credFile = self.get_credentials_file()
        gauth.settings['save_credentials_file'] = credFile 

        # load the creds
        gauth.LoadCredentialsFile(credFile)
        print("Creds: " + gauth.settings['save_credentials_file'])
        
        # manually collect credentials
        if not gauth.credentials or gauth.credentials.invalid:
            if not user_authenticate:
                raise gdcExceptions.NoCredentialsError()
            else:
                print("")
                print("Make sure you log in as the USER you wish to be.")
                print("")
                gauth.CommandLineAuth()

        # build the service
        drive = GoogleDrive(gauth)

        # make sure to scream if this does not work
        if not drive or drive is None:
            raise NoDriveService()

        # done
        self.gauth = gauth
        self.drive = drive
