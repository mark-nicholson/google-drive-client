#
#  File Actions
#

import sys
import os

from gDrive import gdcUtils

from gDrive.gdcExceptions import *

class GdcEntity(object):
    """A generic file."""
    def __init__(self, gfile):
        self.gfile = gfile

    def pull(self, app):
        name = self.gfile['title']
        modDate = self.gfile['modifiedDate']
        modDate_ms = gdcUtils.time_ms_from_epoch(modDate)
        
        # configure the attributes - LINUX
        atime_ns = modDate_ms * 1000 * 1000
        mtime_ns = atime_ns
        os.utime(name, ns=(atime_ns,mtime_ns), follow_symlinks=False)


    def push(self):
        pass

    def sync(self):
        pass

class GdcFolder(GdcEntity):
    """Folder Construct"""
    def __init__(self, gfile):
        super().__init__(gfile)

    def pull(self, app):
        print("Folder:PULL")

        dir_name = self.gfile['title']

        # pre-check
        if os.path.exists(dir_name) or os.path.isdir(dir_name):
            raise NotCleanSlateError(dir_name)

        # build the new directory
        os.mkdir(dir_name)

        # common configs
        super().pull(app)

        # dig?
        if app._flags.no_recurse:
            return

        # recurse..
        os.chdir(dir_name)

        # get the next level files...
        query = {'q': "'%s' in parents and trashed=false" % self.gfile['id']}
        file_list = app.drive.ListFile(query).GetList()
        print("List: %d" % len(file_list))

        # process them
        for item in file_list:
            print('id: %s, par: %s, title: %s' %
                      (item['id'][-8:], self.gfile['id'][-8:], item['title']))

            #import pprint
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(item)

            from gDrive import gdcAction

            # identify
            action_builder = gdcAction.find_action(item)

            # cook it up
            action = action_builder(item)
            
            # process it
            action.pull(app)

        # recurse..
        os.chdir('..')


class GdcSimple(GdcEntity):
    """Basic File"""
    def __init__(self, gfile):
        super().__init__(gfile)

    def pull(self, app):
        print("Simple:PULL")

        name = self.gfile['title']

        # pre-check
        if os.path.exists(name) or os.path.isfile(name):
            raise NotCleanSlateError(name)

        # download the contents
        self.gfile.GetContentFile(name)

        # update the file attribs
        super().pull(app)

    def push(self):
        pass

    def sync(self):
        pass


class GdcGoogleApp(GdcEntity):
    """GoogleApp Construct"""
    def __init__(self, gfile):
        super().__init__(gfile)

    def pull(self, app):
        print("GoogleApp:PULL")

        name = self.gfile['title']
        
        # pre-check
        if os.path.exists(name) or os.path.isfile(name):
            raise NotCleanSlateError(name)

        print("    Skipping " + name)

        # download the contents
        #self.gfile.GetContentFile(name)

        # update the file attribs
        #super.pull(app)

    def push(self):
        pass

    def sync(self):
        pass


#
# Identify what to do based on the known type...
#
mime_map = {
    'application/vnd.google-apps.folder': GdcFolder,
    'application/vnd.google-apps.document': GdcGoogleApp,
    'application/vnd.google-apps.spreadsheet': GdcGoogleApp,
    'application/pdf': GdcSimple,
    }

def find_action(item):
    """Figure out what it is and create a handler"""
    try:
        constructor = mime_map[item['mimeType']]
    except KeyError:
        constructor = GdcSimple

    return constructor
