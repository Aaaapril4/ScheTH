import datetime as dt


def _remove_null(list):
    '''
    Remove all "" in list
    '''
    while "" in list:
        list.remove("")
    
    return list



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



def get_date_begin_end_distributed(para_time, para_generate, len = 1):
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
    if para_time.get("enddate"):
        enddate = dt.date.fromisoformat(para_time.get("enddate"))
        len = (enddate - begindate).days - para_time.getint("buffer")

    rest_index = _get_rest_index(_remove_null(para_generate.get("rest").lower().split(',')), begindate)
    
    work_date = []
    
    i = 0

    while i in rest_index:
        i = i + 1

    while i <= len:
        work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1 + para_generate.getint("interval") + _get_rest_num(i, para_generate.getint("interval"), rest_index)

    return work_date