
import os
import json

# Constants
GDC_FOLDER = '.gdc'
GDC_CREDENTIALS_FILE = 'credentials.json'
GDC_CONFIG_FILE = 'config'


# locate the root dir
def locate_root_dir():
    cwd = os.path.abspath(os.path.curdir)
    while cwd != os.path.sep:
        tdir = os.path.join(cwd, GDC_FOLDER)
        if os.path.isdir(tdir) and os.path.exists(os.path.join(tdir, GDC_CREDENTIALS_FILE)):
            return cwd

        # iterate
        cwd = os.path.dirname(cwd)

    raise gdcExceptions.NoRootDir(os.path.abspath(os.path.curdir))

def get_credentials_file():
    rdir = locate_root_dir()
    return os.path.join(rdir, GDC_FOLDER, GDC_CREDENTIALS_FILE)

def get_config_file():
    rdir = locate_root_dir()
    return os.path.join(rdir, GDC_FOLDER, GDC_CONFIG_FILE)

def load_config():
    """Find and load the top level configuration information
    for this instance."""
    cfile = get_config_file()

    fp = open(cfile)
    cfg = json.load(fp)
    fp.close()

    return cfg


import datetime

#
#  Time support
#

def time_metadata_to_datetime(s):
    sz = s.replace('Z', ' +0000')
    return datetime.datetime.strptime(sz, '%Y-%m-%dT%H:%M:%S.%f %z')

def time_datetime_to_metadata(dt):
    return dt.isoformat()[:-9] + 'Z'

def time_ms_from_epoch(dt):
    """Float of milliseconds since epoch"""

    # accept passing in the string-repr
    if type(dt) is str:
        dt = time_metadata_to_datetime(dt)

    # create a reference
    e = datetime.datetime.utcfromtimestamp(0)

    # not sure why this is necessary as the prior call
    # *should* set the tzinfo to UTC...
    e = e.replace(tzinfo=datetime.timezone.utc)

    # pass back in milliseconds
    return (dt - e).total_seconds() * 1000
    
