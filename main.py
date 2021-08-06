import webbrowser
import sys
from .config import config
from .content import content_dist
from .time import get_date_begin_end_distributed
from .url import

def main(path_to_para):
    para = config(path_to_para)

    if para["GENERATE TYPE"].get("type") == "distributed":
        if para["CONTENT"].get("eachday"):
            distribution = content_dist(para["CONTENT"])
            work_date = get_date_begin_end_distributed(para["TIME"], para["DISTRIBUTED"], len(distribution))
        else:
            work_date = get_date_begin_end_distributed(para["TIME"], para["DISTRIBUTED"])
            distribution = content_dist(para["CONTENT"], len(work_date))
    
    # todo_url(work_date, distribution, para)
