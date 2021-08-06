import configparser
import sys

def check_num(para, group, key):

    if not para[group].get(key):
        para[group][key] = "0"

    return para



def config():
    '''
    Read and validate parameters
    Return:
        para
    '''

    para = configparser.ConfigParser()
    para.read("para.ini")

    if not para["PROJECT"].get("create_project"):
        para["PROJECT"]["create_project"] = "False"
    
    if not para["PROJECT"].get["Project_Name"]:
        para["PROJECT"]["create_project"] = "False"

    if not para["TODOINFO"].get["deadline or day"]:
        sys.exit("deadline or day must be specified")

    if not para["CONTENT"].get["begin"] or not para["CONTENT"].get["end"]:
        sys.exit("Begin and end of the content must be specified")

    if not para["TIME"].get["begindate"]:
        sys.exit("Begindate must be specified")

    if not para["GENERATE TYPE"].get["type"]:
        sys.exit("Type must be specified")

    if not para["TIME"].get["enddate"] and not para["CONTENT"].get["eachday"]:
        sys.exit("enddate or eachday load must be specified at least one")

    para = check_num(para, "DISTRIBUTED", "interval")
    para = check_num(para, "DISTRIBUTED", "buffer")

    return para

if __name__ == "__main__":
    config()