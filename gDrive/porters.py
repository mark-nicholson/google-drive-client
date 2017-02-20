#
#  Support for Importing / Exporting file formats
#

import os
import sys
import platform

from gDrive.app import gDriveApp
from gDrive.gdcAction import *

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

class BasePorter(object):
    def __init__(self, action):
        self.action = action
        
    def extension(self):
        raise NotImplementedError("Porter not implemented")

    def export(self):
        raise NotImplementedError("Porter not implemented")

    def icon_filepath(self, tag):
        return os.path.join(
            gDriveApp.icon_base(),
            'google-logos', '128px',
            'logo_{}_128px.png'.format(tag)
            )


class GooglePorter(BasePorter):
    """Export some sort of Google Apps item"""

    def extension(self):
        tag = gDriveApp.mime_to_file_extension(self.action.exportMimeType())
        return '.' + tag

    def export(self):
        action = self.action
        action.gFile.GetContentFile(action.localPath, action.exportMimeType())


class WindowsDesktopPorter(BasePorter):

    def extension(self):
        if isinstance(self.action, GdcGoogleDoc):
            return '.gdoc'
        if isinstance(self.action, GdcGoogleSheet):
            return '.gsheet'
        return ''

    def export(self):
        action = self.action
        action.gFile.GetContentFile(action.localPath)

class LinuxDesktopPorter(BasePorter):
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

#
# define a helpful default position
#
DefaultPorter = LinuxDesktopPorter
if platform.system == 'Windows':
    DefaultPorter = WindowsDesktopPorter
        
