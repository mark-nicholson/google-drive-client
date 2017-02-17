
import os
import json
from datetime import datetime

from gDrive.gdcExceptions import *

from gDrive.app import gDriveApp

class gDriveCreate(gDriveApp):

    def __init__(self, flags):

        # define our root dir and make it absolute
        root_dir = flags.dir
        if not os.path.isabs(flags.dir):
            root_dir = os.path.abspath(flags.dir)

        # build out
        super().__init__(root_dir=root_dir)

        # configure default configuration
        self._config = gDriveApp.GDC_DEFAULT_CONFIG

        # should break these out...
        self._flags = flags


    @staticmethod
    def touch(fname, mode=0o666, dir_fd=None, **kwargs):
        """Credit to
        http://stackoverflow.com/questions/1158076/implement-touch-using-python
        """
        flags = os.O_CREAT | os.O_APPEND
        with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
            os.utime(f.fileno() if os.utime in os.supports_fd else fname,
                dir_fd=None if os.supports_fd else dir_fd, **kwargs)

    @staticmethod
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
        sp.set_defaults(object=gDriveCreate)
        sp.set_defaults(func=gDriveCreate.do_it)

    def do_it(self):
        print("creating thing ...")

        # make sure things are ready to create
        if os.path.exists(self._flags.dir):
            if self._flags.nuke:
                import shutil
                shutil.rmtree(self._flags.dir)
            else:
                raise NotCleanSlateError("Cannot proceed. Directory '%s' pre-exists." % self._flags.dir)


        # setup the directories
        os.mkdir(self.root_dir())
        os.mkdir(self.gdc_dir())

        # fake a credentials file
        credFile = self.get_credentials_filepath()
        self._config['credentials'] = credFile
        gDriveCreate.touch(credFile, 0o600)

        # baseline is in place, now authenticate, creds must be generated
        self._authenticate(user_authenticate=True)

        # update basic config
        now = gmd.time_datetime_to_metadata(datetime.now())
        cfg = self.config()
        cfg['drive-folder'][0][1] = self.about()['rootFolderId']
        cfg['creation'] = now
        cfg['last-sync'] = now
        print(cfg)

        # should have the user do additional config mods...

        raise gdcSuccess()
        
        ndir = self._flags.dir
        os.mkdir(ndir)
        ndir = os.path.join(ndir, gDriveApp.GDC_FOLDER)
        os.mkdir(ndir)

        credFile = os.path.join(ndir, gDriveApp.GDC_CREDENTIALS_FILE)
        gDriveCreate.touch(credFile, 0o600)

        conFile = os.path.join(ndir, gDriveApp.GDC_CONFIG_FILE)

        # write it out
        fp = open(conFile, "w+")
        json.dump(gDriveApp.GDC_DEFAULT_CONFIG, fp)
        fp.close()

        # go into the dir
        os.chdir(self._flags.dir)


        # create an app instance
        app = gDriveApp(user_authenticate=True)
        




        # back up
        os.chdir("..")

        # done
        raise gdcSuccess()
