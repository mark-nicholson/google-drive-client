#
#  File Actions
#

import sys
import os
import json
import platform

from contextlib import ContextDecorator

from gDrive.app import gDriveApp
from gDrive.gdcExceptions import *
from gDrive import gMetadata as gmd


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



class GdcEntity(object):
    """A generic file."""
    def __init__(self, app, gFile, localPath):
        self.app = app
        self.gFile = gFile

        # full path to the item
        self.localPath = localPath

    def pull(self):
        name = self.localPath
        modDate = self.gFile['modifiedDate']
        modDate_ms = gmd.time_ms_from_epoch(modDate)
        
        # configure the attributes - LINUX
        atime_ns = modDate_ms * 1000 * 1000
        mtime_ns = atime_ns
        os.utime(name, ns=(atime_ns,mtime_ns), follow_symlinks=False)


    def push(self):
        pass

    def sync(self):
        pass

    def load_local_config(self):
        gdcDir = os.path.join(self.localPath, gDriveApp.GDC_FOLDER)
        if not os.path.isdir(gdcDir):
            return {}
        confFile = os.path.join(gdcDir, gDriveApp.GDC_CONFIG_FILE)
        if not os.path.exists(confFile):
            return {}
        fp = open(confFile)
        lconfig = json.load(fp)
        fp.close()
        return lconfig

class GdcFolder(GdcEntity):
    """Folder Construct"""

    MimeType = 'application/vnd.google-apps.folder'
    
    def __init__(self, app, gFile, local_path):
        super().__init__(app, gFile, local_path)
        print("FOLDER: %s # %s" % (local_path, gFile['title']))

    def pull(self):
        print("Folder:PULL")

        #
        # manage the current directory
        #

        # common configs
        super().pull()

        # read an parse local directory config, if any
        cfg = self.load_local_config()
        
        # collect info of all drive sub-entities...
        query = { 'q': "'%s' in parents and trashed=false" % self.gFile['id'] }
        entity_list = self.app.drive.ListFile(query).GetList()

        work_list = []
        folder_list = []
        file_list = []
        
        # separate the folders and files
        for entity in entity_list:
            if entity['mimeType'] == "application/vnd.google-apps.folder":
                folder_list.append(entity)
            else:
                file_list.append(entity)


        if 'subfolders' in cfg:
            # filter to the selection of subfolders
            for f in folder_list:
                for (name,gid) in cfg['subfolders']:
                    if f['title'] == name:
                        worklist.append(f)
        else:
            # grab everything
            work_list += folder_list

        if 'subfiles' in cfg:
            # filter to the selection of subfiles
            for f in file_list:
                for (name,gid) in cfg['subfiles']:
                    if f['title'] == name:
                        worklist.append(f)
        else:
            # grab everything
            work_list += file_list

        # debug
        print("List: %d" % len(work_list))
            


        # handle the files
        for item in file_list:

            print('FILE: id: %s, par: %s, title: %s' %
                      (item['id'][-8:], 'root', item['title']))

            # identify
            action_builder = find_action(item)

            # cook it up
            itemPath = os.path.join(self.localPath, item['title'])
            action = action_builder(self.app, item, itemPath)
            
            # process it, and begin the recursion
            action.pull()


        # recurse
        for item in folder_list:

            print('FOLDER: id: %s, par: %s, title: %s' %
                      (item['id'][-8:], 'root', item['title']))

            # pre-check
            dir_name = os.path.join(self.localPath, item['title'])
            if os.path.exists(dir_name) or os.path.isdir(dir_name):
                raise NotCleanSlateError(dir_name)

            # build the new directory
            os.mkdir(dir_name)

            # dig?
            if self.app._flags.no_recurse:
                return
            
            # identify
            action_builder = find_action(item)

            # cook it up
            itemPath = os.path.join(self.app, self.localPath, item['title'])
            action = action_builder(self.app, item, itemPath)
            
            # process it, and begin the recursion
            action.pull()


class GdcSimple(GdcEntity):
    """Basic File"""
    def __init__(self, app, gFile, localPath):
        super().__init__(app, gFile, localPath)

    def pull(self):
        print("Simple:PULL")

        # pre-check
        if os.path.exists(self.localPath) or os.path.isfile(self.localPath):
            raise NotCleanSlateError(self.localPath)

        # download the contents
        self.gFile.GetContentFile(self.localPath)

        # update the file attribs
        super().pull()

    def push(self):
        pass

    def sync(self):
        pass


_desktop_file_format = \
"""#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.0
Encoding=UTF-8
Name={0[title]}
Type=Link
URL={1}
Icon={2}
MimeType={0[mimeType]}
"""

class BaseExporter(object):
    def __init__(self, action):
        self.action = action
        
    def extension(self):
        raise NotImplementedError("Exporter not implemented")

    def export(self):
        raise NotImplementedError("Exporter not implemented")

    def icon_filepath(self, tag):
        return os.path.join(
            gDriveApp.icon_base(),
            'google-logos', '128px',
            'logo_{}_128px.png'.format(tag)
            )


class GoogleExporter(BaseExporter):
    """Export some sort of Google Apps item"""

    def extension(self):
        tag = gDriveApp.mime_to_file_extension(self.action.exportMimeType())
        return '.' + tag

    def export(self):
        action = self.action
        action.gFile.GetContentFile(action.localPath, action.exportMimeType())


class WindowsDesktopExporter(BaseExporter):

    def extension(self):
        if isinstance(self.action, GdcGoogleDoc):
            return '.gdoc'
        if isinstance(self.action, GdcGoogleSheet):
            return '.gsheet'
        return ''

    def export(self):
        action = self.action
        action.gFile.GetContentFile(action.localPath)

class LinuxDesktopExporter(BaseExporter):
    """Create a .desktop file for Ubuntu ..."""

    def extension(self):
        return '.desktop'

    def export(self):
        action = self.action
            
        # define the content first in case of issues
        content = _desktop_file_format.format(
            action.gFile,
            action.gFile['embedLink'].replace('/htmlembed', ''),
            self.icon_filepath(action.tag)
            )

        # create the file -- probably should lock it...
        f = open(action.localPath, "w+")

        # splat the content
        f.write(content)

         # make them read-only so the contents are not edited
        os.fchmod(f.fileno(), 0o444)

        # done
        f.close()


# define a helpful default position
DefaultExporter = LinuxDesktopExporter
import platform
if platform.system == 'Windows':
    DefaultExporter = WindowsDesktopExporter
        

class GdcGoogleApp(GdcEntity):
    """GoogleApp Construct"""
    tag = 'drive'
    MimeType = None
    
    def __init__(self, app, gFile, localPath):
        super().__init__(app, gFile, localPath)
        self._exportMimeType = None

        # figure out an exporter
        if self.exportMimeType() is None:
            self.exporter = DefaultExporter(self)
        else:
            self.exporter = GoogleExporter(self)

        # update the filename
        self.localPath = self.localPath + self.exporter.extension()


    def _available_export_formats(self):
        about = self.app.about()
        for expFmt in about['exportFormats']:
            if expFmt['source'] == self.MimeType:
                return expFmt['targets']

        return []

    def exportMimeType(self):
        if self._exportMimeType:
            return self._exportMimeType            

        # any mappings at all?
        cfg = self.app.config()
        if 'export-formats' not in cfg:
            self._exportMimeType = None
            return None

        # do we have a definition in the config at for this kind?
        try:
            emt = cfg['export-formats'][self.gFile['mimeType']]
        except KeyError:
            self._exportMimeType = None
            return None

        # is it a *valid* kind
        aef = self._available_export_formats()
        for ef in aef:
            if ef == emt:
                self._exportMimeType = ef
                return ef

        # nope, default then...
        self._exportMimeType = None
        return None

    def pull(self):
        print("GoogleApp:PULL")
        
        # pre-check
        if os.path.exists(self.localPath) or os.path.isfile(self.localPath):
            raise NotCleanSlateError(self.localPath)

        # export/download the contents
        self.exporter.export()

        # update the file attribs
        super().pull()

    def push(self):
        pass

    def sync(self):
        pass

class GdcGoogleDoc(GdcGoogleApp):

    tag = 'docs'
    MimeType = 'application/vnd.google-apps.document'


class GdcGoogleSheet(GdcGoogleApp):

    tag = 'sheets'
    MimeType = 'application/vnd.google-apps.spreadsheet'

class GdcGoogleMap(GdcGoogleApp):

    tag = 'maps'
    MimeType = 'application/vnd.google-apps.map'

class GdcGoogleForm(GdcGoogleApp):

    tag = 'forms'
    MimeType = 'application/vnd.google-apps.form'

class GdcGoogleDrawing(GdcGoogleApp):

    tag = 'draw'
    MimeType = 'application/vnd.google-apps.drawing'

class GdcGoogleScript(GdcGoogleApp):

    tag = 'script'
    MimeType = 'application/vnd.google-apps.script'

class GdcGooglePresentation(GdcGoogleApp):

    tag = 'slides'
    MimeType = 'application/vnd.google-apps.presentation'


#
# Identify what to do based on the known type...
#
mime_map = {
    GdcFolder.MimeType: GdcFolder,
    GdcGoogleDoc.MimeType: GdcGoogleDoc,
    GdcGoogleSheet.MimeType: GdcGoogleSheet,
    GdcGoogleMap.MimeType: GdcGoogleMap,
    GdcGoogleForm.MimeType: GdcGoogleForm,
    GdcGoogleDrawing.MimeType: GdcGoogleDrawing,
    GdcGoogleScript.MimeType: GdcGoogleScript,
    GdcGooglePresentation.MimeType: GdcGooglePresentation,
    'application/pdf': GdcSimple,
    }

def find_action(item):
    """Figure out what it is and create a handler"""
    try:
        constructor = mime_map[item['mimeType']]
    except KeyError:
        constructor = GdcSimple

    return constructor
