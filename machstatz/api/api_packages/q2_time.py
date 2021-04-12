import time
from . import fetch_json

def main_(start,end):
    start_time = fetch_json.validate_input(start)
    end_time = fetch_json.validate_input(end)
    if (start_time[0] and end_time[0]):
        return get_result(start_time,end_time)
    else:
        return {"invalid_data":{start_time[1],end_time[1]}}

def time_format(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%Hh:%Mm:%Ss",ty_res)
    return res

def get_result(start_time,end_time):
    json_url = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json"
    start,end,json_data = fetch_json.find_range(start_time,end_time,json_url)
    if start==None or end==None:
        query_result = {"invalid_request":"Check date and time format"}
    else:
        rt = 0
        dt = 0
        start = json_data.index(start)
        end = json_data.index(end)
        for i in range(start,end+1):
            if json_data[i]['runtime'] < 1021:
                rt+=json_data[i]['runtime']
            else:
                dt+=json_data[i]['runtime']-1021
                rt+=1021
            if json_data[i]['downtime'] != 0:
                dt+=json_data[i]['downtime']
        utlz = round((((rt)/(rt+dt))*100),2)
        rt = time_format(rt)
        dt = time_format(dt)
        query_result = {"runtime":rt,"downtime":dt,"utilization":utlz}
    return query_result
