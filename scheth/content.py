import random


def _cal_bin(para, binn = 1):
    '''
    Calculate the load num for each day
    Parameter:
        para["CONTENT"]
    Return:
        num for each day
    '''
    if para.get("eachday"):
        each = para.getint("eachday")
    else:
        total = para.getint("end") - para.getint("begin") + 1
        each = total // binn + int(bool(total % binn))

    return each



def content_dist(para, binn = 1):
    '''
    Calculate the load of content for each day
    Parameter:
        para["CONTENT"]
    Return:
        Load distribution with time
    '''
    
    each = _cal_bin(para, binn)
    begin = para.getint("begin")
    end = para.getint("end")

    if para.getboolean("random"):
        lst = list(range(begin, end+1))
        random.shuffle(lst)
        dist = [lst[i:i+each] for i in range(0,len(lst),each)]
    else:
        dist = list(range(begin+each-1, end, each))
        (end not in dist) and (dist.append(end))

    return dist