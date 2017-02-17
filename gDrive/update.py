
from gDrive.app import gDriveApp
from gDrive import gdcExceptions

class gDriveUpdate(gDriveApp):

    def __init__(self, flags):
        super().__init__()
        
        self._flags = flags

    @staticmethod
    def add_subparser(p_subparsers):
        # generate a custom subparser
        sp = p_subparsers.add_parser('update',
                                        help='updating a gDrive map')

        # configure it
        sp.add_argument('--force', action='store_true',
                            help='overwrite existing files')
        sp.add_argument('--no_recurse',
                        action='store_true', help='do not climb the filesystem')

        # define the lauch routine
        sp.set_defaults(object=gDriveUpdate)
        sp.set_defaults(func=gDriveUpdate.do_it)

    def do_it(self):
        print("updating ...")

        # done
        raise gdcExceptions.gdcSuccess()
