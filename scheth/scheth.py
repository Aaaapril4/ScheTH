from .config import config
from .content import content_dist
from .date import get_date_begin_end_distributed, get_date_begin_end_specific
from .url import todo_url

def scheth(path_to_para):
    para = config(path_to_para)
    if para["GENERATE TYPE"].get("type").lower() == "distributed":
        if para["CONTENT"].get("eachday"):
            distribution = content_dist(para["CONTENT"])
            work_date = get_date_begin_end_distributed(para["TIME"], para["DISTRIBUTED"], len(distribution))
        else:
            work_date = get_date_begin_end_distributed(para["TIME"], para["DISTRIBUTED"])
            distribution = content_dist(para["CONTENT"], len(work_date))
    
    if para["GENERATE TYPE"].get("type").lower() == "specific":
        if para["CONTENT"].get("eachday"):
            distribution = content_dist(para["CONTENT"])
            work_date = get_date_begin_end_specific(para["TIME"], para["SPECIFIC"], len(distribution))
        else:
            work_date = get_date_begin_end_specific(para["TIME"], para["SPECIFIC"])
            distribution = content_dist(para["CONTENT"], len(work_date))
    
    todo_url(work_date, distribution, para)

if __name__ == "__main__":
    scheth("para.ini")