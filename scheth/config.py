import configparser
import sys

def _check_num(para, group, key):

    if not para[group].get(key):
        para[group][key] = "0"

    return para



def _remove_null(string):
    '''
    Remove all " " in list
    '''
    string = string.replace(" ", "")
    
    return string




def config(path_to_para):
    '''
    Read and validate parameters
    Return:
        para
    '''

    para = configparser.ConfigParser()
    para.read(path_to_para)

    if not para["PROJECT"].get("create_project"):
        para["PROJECT"]["create_project"] = "False"
    
    if not para["PROJECT"].get("project"):
        para["PROJECT"]["create_project"] = "False"

    if not para["TODOINFO"].get("deadline or day"):
        sys.exit("deadline or day must be specified")

    if not para["CONTENT"].get("begin") or not para["CONTENT"].get("end"):
        sys.exit("Begin and end of the content must be specified")

    if not para["TIME"].get("begindate"):
        sys.exit("Begindate must be specified")

    if not para["GENERATE TYPE"].get("type"):
        sys.exit("Type must be specified")

    if not para["TIME"].get("enddate") and not para["CONTENT"].get("eachday"):
        sys.exit("enddate or eachday load must be specified at least one")

    if para["DISTRIBUTED"].get("rest"):
        string = _remove_null(para["DISTRIBUTED"].get("rest"))
        para["DISTRIBUTED"]["rest"] = string.lower()
    
    if para["DISTRIBUTED"].get("rest"):
        string = _remove_null(para["DISTRIBUTED"].get("rest"))
        para["DISTRIBUTED"]["rest"] = string.lower()

    if para["SPECIFIC"].get("week day"):
        string = _remove_null(para["SPECIFIC"].get("week day"))
        para["SPECIFIC"]["week day"] = string.lower()

    para = _check_num(para, "DISTRIBUTED", "interval")
    para = _check_num(para, "DISTRIBUTED", "buffer")

    return para