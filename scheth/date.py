import datetime as dt

def _get_rest_num(i, interval, rest_index):
    '''
    Check the num of rest days in days [i, i+interval+1]
    '''
    total = 0
    end = i + interval + 1
    while i <= end:
        if i % 7 in rest_index:
            total = total + 1
        i = i + 1
    
    return total



def _get_rest_index(rest, begindate):
    '''
    Calculate the the index of rest days, begindate as 0
    Return:
        A list of indexes
    '''
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    rest_index = []

    for day in rest:
        dif = weekdays.index(day) - begindate.weekday()
        dif = dif + 7 if dif < 0 else dif
        rest_index.append(dif)

    return rest_index




def _distribute_time(begindate, interval,total, rest_index):
    '''
    For distributed with enddate
    '''
    work_date = []
    
    i = 0

    while i in rest_index:
        i = i + 1

    while i <= total:
        work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1 + interval + _get_rest_num(i, interval, rest_index)

    return work_date



def _distribute_specific(begindate, interval, total, rest_index):
    '''
    For distributed without enddate
    '''
    work_date = []
    
    i = 0

    while i in rest_index:
        i = i + 1

    while len(work_date) < total:
        work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1 + interval + _get_rest_num(i, interval, rest_index)

    return work_date



def _specific_time(begindate, total, dayindex):
    '''
    For specific with enddate
    '''
    work_date = []

    i = dayindex[0]

    while i <= total:
        if i % 7 in dayindex:
            work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1
    
    return work_date



def _specific_specific(begindate, total, dayindex):
    '''
    For specific without enddate
    '''
    work_date = []

    i = dayindex[0]

    while len(work_date) <= total:
        if i % 7 in dayindex:
            work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1
    
    return work_date



def get_date_begin_end_distributed(para_time, para_generate, total = 1):
    '''
    Calculate the work time
    Parameters:
        para["TIME"]
        para["DISTRIBUTED"]
        length of load list
    Return:
        A list of date for each load
    '''

    begindate = dt.date.fromisoformat(para_time.get("begindate"))
    rest_index = _get_rest_index(para_generate.get("rest").split(','), begindate)
    interval = para_generate.getint("interval")

    if para_time.get("enddate"):
        enddate = dt.date.fromisoformat(para_time.get("enddate"))
        total = (enddate - begindate).days - para_time.getint("buffer")

        work_date = _distribute_time(begindate, interval,total, rest_index)
    else:
        work_date = _distribute_specific(begindate, interval,total, rest_index)
    

    return work_date



def get_date_begin_end_specific(para_time, para_generate, total = 1):
    '''
    Calculate the work time
    Parameters:
        para["TIME"]
        para["DISTRIBUTED"]
        length of load list
    Return:
        A list of date for each load
    '''

    begindate = dt.date.fromisoformat(para_time.get("begindate"))
    dayindex = _get_rest_index(para_generate.get("week day").split(','), begindate)
    dayindex.sort()

    if para_time.get("enddate"):
        enddate = dt.date.fromisoformat(para_time.get("enddate"))
        total = (enddate - begindate).days - para_time.getint("buffer")

        work_date = _specific_time(begindate, total, dayindex)
    else:
        work_date = _specific_specific(begindate, total, dayindex)

    return work_date