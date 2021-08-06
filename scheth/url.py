import webbrowser
import sys

def _timesetting(para):
    '''
    Set time type
    '''
    setting = para["TODOINFO"].get("deadline or day")
    if setting.lower() == "deadline":
        return "deadline"
    elif setting.lower() == "day":
        return "when"



def create_project(para):
    '''
    Create project if need
    '''
    string = ""
    if para["PROJECT"].get("area"):
        string = "&".join((string, f'area={para["PROJECT"].get("area")}'.replace(' ', '%20')))
    url = 'things:///add-project?title={}'.format(para["PROJECT"].get("project").replace(' ', '%20')) + string
    webbrowser.open(url)

    return



def _projectsetting(para):
    '''
    Set project info
    '''
    string = ""
    if para["PROJECT"].get("project"):
        string = "&".join((string, f'list={para["PROJECT"].get("project")}'.replace(' ', '%20') ))

    return string



def open_url(title, workdate, projectstring, notes, timesetting):
    try:
        url = f'things:///add?title={title}&{timesetting}={workdate}&notes={notes}' + projectstring
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
    projectstring = _projectsetting(para)
    notes = para["TODOINFO"].get("notes").replace(' ','%20')
    timesetting = _timesetting(para)

    for i in range(len(distribution)):
        if type(distribution[i]) == list:
            for j in range(len(distribution[i])):
                title = f'{prefix} {distribution[i][j]} {suffix}'.replace(' ', '%20')
                open_url(title, work_date[i], projectstring, notes, timesetting)
        else:
            title = f'{prefix} {distribution[i]} {suffix}'.replace(' ', '%20')
            open_url(title, work_date[i], projectstring, notes, timesetting)
        
    return