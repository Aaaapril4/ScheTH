import datetime as dt
import webbrowser
import configparser
import sys
import random


def _num_distribute(begin, end, eachday, binn, rand):
    '''
    Calculate the number in each bin
    Return:
        list of the end of each bin
    '''

    if eachday != "":
        each = int(eachday)
    else:    
        total = end - begin + 1
        each = total // binn + int(bool(total % binn))
    
    if rand:
        lst = list(range(begin, end+1))
        random.shuffle(lst)
        distribution = [lst[i:i+each] for i in range(0,len(lst),each)]
    else:
        distribution = list(range(begin+each-1, end, each))
        (end not in distribution) and (distribution.append(end))

    return distribution



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



def _get_date_begin_end(begindate, enddate, interval, buffer, rest):
    '''
    Calculate the work time according to the begin and end time
    Return:
        A list of work date
    '''

    interval = int(interval) if interval != '' else 0
    buffer = int(buffer) if buffer != '' else 0
    rest_index = _get_rest_index(rest, begindate)
    
    work_date = []
    total = (enddate - begindate).days - buffer
    i = 0

    while i in rest_index:
        i = i + 1

    while i <= total:
        work_date.append((begindate + dt.timedelta(i)).isoformat())
        i = i + 1 + interval + _get_rest_num(i, interval, rest_index)

    return work_date



def _timesetting(para):
    setting = para["TODOINFO"].get("deadline or day")
    if setting.lower() == "deadline":
        return "deadline"
    elif setting.lower() == "day":
        return "when"



def create_project(para):
    string = ""
    if para["PROJECT"].get("area").lower() != 'none' and para["PROJECT"].get("area") != '':
        string = "&".join((string, f'area={para["PROJECT"].get("area")}'.replace(' ', '%20')))
    url = 'things:///add-project?title={}'.format(para["PROJECT"].get("project").replace(' ', '%20')) + string
    webbrowser.open(url)

    return



def open_url(title, workdate, projectname, notes, timesetting):
    try:
        url = f'things:///add?title={title}&{timesetting}={workdate}&list={projectname}&notes={notes}'
    except IndexError:
        sys.exit(f"You need more days to complete.")
            
    webbrowser.open(url)

    return



def todo_url(work_date, distribution, para):
    '''
    Generate todo from url
    Return:
        None
    '''

    if para["PROJECT"].getboolean("create_project"):
        create_project(para)

    prefix = para["TODOINFO"].get("prefix")
    suffix = para["TODOINFO"].get("suffix")
    projectname = para["PROJECT"].get("project").replace(' ','%20')
    notes = para["TODOINFO"].get("notes").replace(' ','%20')
    timesetting = _timesetting(para)

    for i in range(len(distribution)):
        if type(distribution[i]) == list:
            for j in range(len(distribution[i])):
                title = f'{prefix} {distribution[i][j]} {suffix}'.replace(' ', '%20')
                open_url(title, work_date[i], projectname, notes, timesetting)
        else:
            title = f'{prefix} {distribution[i]} {suffix}'.replace(' ', '%20')
            open_url(title, work_date[i], projectname, notes, timesetting)
        
    return
    


def config(para):
    '''
    The main function
    Return:
        None
    '''

    begindate = dt.date.fromisoformat(para["DISTRIBUTED"].get("begindate"))
    enddate = dt.date.fromisoformat(para["DISTRIBUTED"].get("enddate"))
    if para["GENERATE TYPE"].get("type") == "distributed":
        work_date = _get_date_begin_end(begindate, enddate, para["DISTRIBUTED"].get("interval"), int(para["DISTRIBUTED"].get("buffer")), para["DISTRIBUTED"].get("rest").lower().split(','))
    else:
        sys.exit("Need to define begin-end or fix-interval")

    distribution = _num_distribute(int(para["CONTENT"].get("begin")), int(para["CONTENT"].get("end")), para["CONTENT"].get("eachday"), len(work_date), para["DISTRIBUTED"].getboolean("random"))

    todo_url(work_date, distribution, para)

    return



if __name__ == "__main__":
    para = configparser.ConfigParser()
    para.read("para.ini")
    config(para)