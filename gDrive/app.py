
import sys
import os
import json
from datetime import datetime

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import gDrive
from gDrive.gdcExceptions import *
import gDrive.gMetadata as gmd


class gDriveApp(object):
    """Parent of all sub-command apps."""

    GDC_FOLDER = '.gdc'
    GDC_CREDENTIALS_FILE = 'credentials.json'
    GDC_CONFIG_FILE = 'config'
    GDC_APP_INFO_DIR = 'app-info'
    GDC_CLIENT_SECRET_FNAME = 'client_secret.json'
    GDC_DEFAULT_CONFIG = {
        'credentials': GDC_CREDENTIALS_FILE,
        'drive-folder': ['root', 'xxxIDxxx'],
        'subfolders': [
        ],
        'creation': gmd.time_epoch(md=True),
        'last-sync': gmd.time_epoch(md=True)
    }


    def __init__(self, root_dir=None):
        print("gDriveApp.__init__()")
        # locals
        self._config = None
        self._root_dir = root_dir

        # cloud
        self._root = None
        self._about = None

    #
    #  MIME Support
    #
    mimeType_map = None
    @staticmethod
    def mime_to_file_extension(mimeType):
        if gDriveApp.mimeType_map is None:
            fname = os.path.join(
                gDriveApp.install_base(),
                gDriveApp.GDC_APP_INFO_DIR,
                'mime.types')
            f = open(fname)
            gDriveApp.mimeType_map = {}
            for l in f.readlines():
                if not l.startswith('#'):
                    items = l.rstrip().split()
                    gDriveApp.mimeType_map[items[0]] = items[1]
            f.close()

        return gDriveApp.mimeType_map[mimeType]

    def root_dir(self):
        if self._root_dir:
            return self._root_dir

        # snoop ...
        cwd = os.path.abspath(os.path.curdir)
        while cwd != os.path.sep:
            print("CWD:" + cwd)
            tdir = os.path.join(cwd, gDriveApp.GDC_FOLDER)
            if os.path.isdir(tdir) \
                and \
                os.path.exists(os.path.join(tdir, gDriveApp.GDC_CREDENTIALS_FILE)):
                if self:
                    self._root_dir = cwd
                return cwd

            # iterate
            cwd = os.path.dirname(cwd)

        # bad news ...
        raise NoRootDir(os.path.abspath(os.path.curdir))

    def gdc_dir(self):
        return os.path.join(self.root_dir(), gDriveApp.GDC_FOLDER)

    
    def about(self):
        if not self._about:
            self._about = self.drive.GetAbout()
        return self._about
        
    def root(self):
        if not self._root:
            about = self.about()
            sf = self.drive.auth.service.files()
            r_md = sf.get(fileId=about['rootFolderId']).execute(http=self.drive.http)
            self._root = self.drive.CreateFile(metadata=r_md)
        return self._root

    def gfile_by_id(self, gid):
        sf = self.drive.auth.service.files()
        r_md = sf.get(fileId=gid).execute(http=self.drive.http)
        return self.drive.CreateFile(metadata=r_md)

    def get_config_filepath(self):
        return os.path.join(
            self.root_dir(),
            gDriveApp.GDC_FOLDER,
            gDriveApp.GDC_CONFIG_FILE)

    def get_credentials_filepath(self):
        return os.path.join(
            self.root_dir(),
            gDriveApp.GDC_FOLDER,
            gDriveApp.GDC_CREDENTIALS_FILE)

    def platform_config(self):
        """Get a set of platform specific defaults"""
        if not self._plat_config:           
            pcf = os.path.join(self.install_base(),
                               'app-info',
                               'platform-config')
            fp = open(pcf)
            self._plat_config = json.load(fp)
            fp.close()

        return self._plat_config
    
    def config(self):
        if not self._config:
            fp = open(self.get_config_filepath())
            self._config = json.load(fp)
            fp.close()
            
        return self._config

    def store_config_file(self, cfg=None):
        if cfg is None:
            cfg = self._config

        # bread crumbs
        cfg['last-update'] = datetime.isoformat(datetime.now())

        # write it out
        fp = open(self.get_config_filepath(), "w+")
        json.dump(cfg, fp)
        fp.close()
    
    
    @staticmethod
    def install_base():
        return gDrive.__file__.rsplit(os.path.sep, 1)[0]

    @staticmethod
    def icon_base():
        return os.path.join(gDriveApp.install_base(), 'icons')
    
    def client_secret_filepath(self):
        return os.path.join(
            gDriveApp.install_base(),
            gDriveApp.GDC_APP_INFO_DIR,
            gDriveApp.GDC_CLIENT_SECRET_FNAME)
    
    def _authenticate(self, user_authenticate=False):
        print("app._authenticate()")

        # load the config file
        cfg = self.config()

        # base authentication unit
        gauth = GoogleAuth()

        # lookup the client secret file
        ccf = self.client_secret_filepath()
        
        # setup the settings
        gauth.settings['client_config_backend'] = 'file' 
        gauth.settings['client_config_file'] = ccf
        gauth.settings['save_credentials'] = True
        gauth.settings['save_credentials_backend'] = 'file' 
        credFile = self.get_credentials_filepath()
        gauth.settings['save_credentials_file'] = credFile 

        # load the creds
        gauth.LoadCredentialsFile(credFile)
        #print("Creds: " + gauth.settings['save_credentials_file'])
        
        # manually collect credentials
        if not gauth.credentials or gauth.credentials.invalid:
            if not user_authenticate:
                raise NoCredentialsError()
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

        # remember
        self.gauth = gauth
        self.drive = drive

        # kick start the data-stream. Not sure why this is needed, but
        # if I try to fetch a file's metadata first, it chokes like the
        # service is not built.
        about = self.about()
