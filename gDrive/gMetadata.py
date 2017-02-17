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
    e = time_epoch()

    # pass back in milliseconds
    return (dt - e).total_seconds() * 1000
    
def time_epoch(md=False):
    # create the epoch
    e = datetime.datetime.utcfromtimestamp(0)
    
    # not sure why this is necessary as the prior call
    # *should* set the tzinfo to UTC...
    e = e.replace(tzinfo=datetime.timezone.utc)

    # convert as requested
    if md:
        e = time_datetime_to_metadata(e)

    return e
