
import os

from gDrive import gdcAction

def do_pull(flags):
    print("In do_pul()")
    gdp = gDrivePull(flags)
    gdp.do_it()

def add_subparser(p_subparsers):
    # generate a custom subparser
    sp = p_subparsers.add_parser('pull',
                                    help='pull a new gDrive map')

    # configure it
    sp.add_argument('--force', action='store_true',
                        help='overwrite existing files')
    sp.add_argument('--no_recurse',
                    action='store_true', help='do not climb the filesystem')

    # define the lauch routine
    sp.set_defaults(func=do_pull)


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from gDrive import gdcUtils
from gDrive import gdcAuth
from gDrive import gdcExceptions

from gDrive.app import gDriveApp

from contextlib import ContextDecorator
class FolderContext(ContextDecorator):
    def __init__(self, folder, basepath=None):
        self.folder = folder
        self.path = item['title']
        if basepath is not None:
            self.path = os.path.join(basepath, item['title'])

        self.revpath = ''
        for p in self.path.split(os.path.sep):
            self.revpath = os.path.join(self.revpath, '..')
        
    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self):
        os.chdir(self.revpath)


class gDrivePull(gDriveApp):

    def __init__(self, flags):
        super().__init__()
        
        self._flags = flags

    def do_it(self):
        print("pulling ...")

        # locate the root
        #rdir = gdcUtils.locate_root_dir()
        print("RootDIR: " + self.root_dir())

        # make it the working dir
        os.chdir(self.root_dir())

        # Google Drive root
        #root = 
        
        # get the service
        #self.drive = gdcAuth.authenticate()
        
        # quick query test

        # folders...
        folders = []

        if not self.config()['folders'] or
            self.config()['folders'][0][0] == 'root':
            folders.append(self.root)
        else:
            # collect the root folder info
            query = {'q': "'root' in parents and trashed=false"}
            file_list = self.drive.ListFile(query).GetList()

            for (name, id) in self.config()['folders']:
                for f in file_list:
                    if f['title'] == name:
                        folders.append(f)
                        break

        print("List: %d" % len(file_list))
            


        # recurse
        for item in file_list:

            print('id: %s, par: %s, title: %s' %
                      (item['id'][-8:], 'root', item['title']))

            #import pprint
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(item)
            
            # identify
            action_builder = gdcAction.find_action(item)

            # cook it up
            action = action_builder(item)
            
            # process it
            action.pull(self)

            # remember folders for later....
            #if type(action) is GdcFolder:
            #    folders.append(action)


        #if not self._flags.no_recurse:
        #    for folder in folders:

                
        # done
        raise gdcExceptions.gdcSuccess()
