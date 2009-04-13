import datetime

def fuzzy_time_diff(begin, end=None):
    """
    Returns a humanized string representing time difference
    between now() and the input timestamp.
    
    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns "4 days"
    0 days 4 hours 3 minutes returns "4 hours", etc...
    """
    if end is None:
        end = datetime.datetime.now()
    timeDiff = end - begin
    days = timeDiff.days
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60
    
    str = ""
    tStr = ""
    if days > 0:
        if days == 1:   tStr = "day"
        else:           tStr = "days"
        str = str + "%s %s" %(days, tStr)
        return str
    elif hours > 0:
        if hours == 1:  tStr = "hour"
        else:           tStr = "hours"
        str = str + "%s %s" %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = "minutes"
        else:           tStr = "minutes"           
        str = str + "%s %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "second"
        else:           tStr = "seconds"
        str = str + "%s %s" %(seconds, tStr)
        return str
    else:
        return None

