
import os

from gDrive import gdcAction
from gDrive import gdcExceptions
from gDrive.app import gDriveApp


class gDrivePull(gDriveApp):

    def __init__(self, flags):
        super().__init__()
        print("gDrivePull.__init__()")        
        self._flags = flags

        # authenticate
        self._authenticate()


    @staticmethod
    def add_subparser(p_subparsers):
        # generate a custom subparser
        sp = p_subparsers.add_parser('pull',
                                        help='pull a new gDrive map')

        # configure it
        sp.add_argument('--check', action='store_true',
                            help='validate the existing files')
        sp.add_argument('--force', action='store_true',
                            help='overwrite existing files')
        sp.add_argument('--no_recurse',
                        action='store_true', help='do not climb the filesystem')

        # define the lauch routine
        sp.set_defaults(object=gDrivePull)
        sp.set_defaults(func=gDrivePull.do_it)

    def do_it(self):
        print("pulling ...")

        # get the config
        cfg = self.config()

        # locate the root
        print("RootDIR: " + self.root_dir())

        # make it the working dir
        #os.chdir(self.root_dir())

        # gRoot is the gFile which maps to the base folder in GoogleDrive
        #  and is *NOT* necessarily 'My Drive', ie. true google-drive-root
        gRoot = self.gfile_by_id(cfg['drive-folder'][1])

        # identify
        action_builder = gdcAction.find_action(gRoot)

        # cook it up
        action = action_builder(gRoot, self.root_dir())
            
        # process it, and begin the recursion
        action.pull(self)

        # done
        raise gdcExceptions.gdcSuccess()
