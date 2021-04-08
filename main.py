import datetime as dt
import webbrowser
import configparser

def check_date():
    
    return


def _num_distribute(begin, end, binn):
    '''
    Calculate the number in each bin
    Return:
        list of the end of each bin
    '''
    
    total = end - begin
    each = total // binn + int(bool(total % binn))
    distribution = list(range(begin, end, each))
    if end not in distribution:
        distribution.append(end)
    distribution.pop(0)

    return distribution



def get_work_date(begindate, enddate, buffer, rest):
    '''
    Get the date for working
    Return:
        A list of work date
    '''

    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    rest_index = []
    for i in range(0,7):
        if (begindate + dt.timedelta(i)).weekday() in [weekdays.index(day.strip()) for day in rest]:
            rest_index.append(i)
    
    work_date = []
    total = (enddate - begindate).days - buffer
    for i in range(total):
        if i % 7 not in rest_index:
            work_date.append((begindate + dt.timedelta(i)).isoformat())

    return work_date



def todo_url(work_date, distribution, para):
    '''
    Generate todo from url
    Return:
        None
    '''

    string = ""
    if para.getboolean("create_project"):
        if para.get("area").lower() != 'none' and para.get("area") != '':
            string = "&".join((string, f'area={para.get("area")}'.replace(' ', '%20')))
        url = 'things:///add-project?title={}'.format(para.get("project").replace(' ', '%20')) + string
        webbrowser.open(url)

    string = ""
    prefix = para.get("prefix") if para.get("prefix").lower() != 'none' else ''
    suffix = para.get("suffix") if para.get("suffix").lower() != 'none' else ''

    for i in range(len(distribution)):
        url = 'things:///add?title={}&when={}&list={}'.format(f'{prefix} {distribution[i]} {suffix}'.replace(' ', '%20'), work_date[i], para.get("project").replace(' ','%20'))
        webbrowser.open(url)
    
    return



def regular(para):
    '''
    The main routine to generate a list of todos
    Return:
        None
    '''

    totalnum = int(para["REGULAR"].get("end")) - int(para["REGULAR"].get("begin"))

    begindate = dt.date.fromisoformat(para["REGULAR"].get("begindate"))
    enddate = dt.date.fromisoformat(para["REGULAR"].get("enddate"))
    work_date = get_work_date(begindate, enddate, int(para["REGULAR"].get("buffer")), para["REGULAR"].get("rest").lower().split(','))
    distribution = _num_distribute(int(para["REGULAR"].get("begin")), int(para["REGULAR"].get("end")), len(work_date))
    todo_url(work_date, distribution, para["DEFAULT"])
    
    return
    




if __name__ == "__main__":
    para = configparser.ConfigParser()
    para.read("para.ini")
    regular(para)