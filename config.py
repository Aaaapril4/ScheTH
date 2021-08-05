import configparser

def config(para):
    '''
    The main function
    Return:
        None
    '''

    begindate = dt.date.fromisoformat(para["DISTRIBUTED"].get("begindate"))
    enddate = dt.date.fromisoformat(para["DISTRIBUTED"].get("enddate"))
    interval = int(para["DISTRIBUTED"].get("interval")) if para["DISTRIBUTED"].get("interval") != '' else 0
    buffer = int(para["DISTRIBUTED"].get("buffer")) if para["DISTRIBUTED"].get("buffer") != '' else 0
    
    if para["GENERATE TYPE"].get("type") == "distributed":
        work_date = _get_date_begin_end(begindate, enddate, interval, buffer, para["DISTRIBUTED"].get("rest").lower().split(','))
    else:
        sys.exit("Need to define begin-end or fix-interval")

    distribution = _num_distribute(int(para["CONTENT"].get("begin")), int(para["CONTENT"].get("end")), para["CONTENT"].get("eachday"), len(work_date), para["DISTRIBUTED"].getboolean("random"))

    todo_url(work_date, distribution, para)

    return