
import os
import json

def do_create(flags):
    print("In do_create()")
    gdc = gDriveCreate(flags)
    gdc.do_it()

def add_subparser(p_subparsers):
    # generate a custom subparser
    sp = p_subparsers.add_parser('create',
                                    help='create an new gDrive map')

    # configure it
    sp.add_argument('--dir', help='local directory name', required=True)
    sp.add_argument('--google-user', help='google-username')
    sp.add_argument('--drive-subdir', help='google drive base folder')
    sp.add_argument('--nuke', help='annihilate pre-existing dir', action='store_true')

    # define the lauch routine
    sp.set_defaults(func=do_create)


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from gDrive import gdcUtils
from gDrive import gdcExceptions

class gDriveCreate():

    def __init__(self, flags):
        self._flags = flags
        

    def do_it(self):
        print("creating thing ...")

        if os.path.exists(self._flags.dir):
            if self._flags.nuke:
                os.rmdir(self._flags.dir)
            else:
                print("Cannot proceed. Directory '%s' pre-exists." % self._flags.dir)
                exit(-1)

        try:
            os.mkdir(self._flags.dir)
            os.mkdir(os.path.join(self._flags.dir, gdcUtils.GDC_FOLDER))
        except OSError:
            print("Failed to create directory structure.")
            exit(-1)

        # generate the configuration file
        cfg = {
            'credentials': gdcUtils.GDC_CREDENTIALS_FILE,
            'folders': [
                ['root', 'root']
            ]
        }
            
        fp = open(gdcUtils.get_config_file(), "w+")
        json.dump(cfg, fp)
        fp.close()
        
        # authenticate
        drive = gdcAuth.authenticate(cfg, True)
        
        # slurp the configuration
        #gauth = GoogleAuth('settings.yaml')

        # define the credentials file
        #gauth.settings['save_credentials_file'] = os.path.join(
        #    self._flags.dir,
        #    gdcUtils.GDC_FOLDER,
        #    gdcUtils.GDC_CREDENTIALS_FILE)
        
        # manually collect credentials
        #if not gauth.credentials or gauth.credentials.invalid:
        #    print("")
        #    print("Make sure you log in as the USER you wish to be.")
        #    print("")
        #    gauth.CommandLineAuth()

        # done
        raise gdcExceptions.gdcSuccess()
