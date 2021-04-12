from . import fetch_json
import json

def main_(start,end):
    start_time = fetch_json.validate_input(start)
    end_time = fetch_json.validate_input(end)
    if (start_time[0] and end_time[0]):
        return get_result(start_time,end_time)
    else:
        return {"invalid_data":"check format and range of date and time. Make sure the request is in follwoing text format "}


def get_result(start_time,end_time):
    json_url = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json"
    start,end,json_data = fetch_json.find_range(start_time,end_time,json_url)
    if start==None or end==None:
        query_result = {"invalid_request":"check format and range of date and time. Make sure the request is in follwoing text format "}
    else:
        shiftA = {"production_A_count":0,"production_B_count":0}
        shiftB = {"production_A_count":0,"production_B_count":0}
        shiftC = {"production_A_count":0,"production_B_count":0}

        start = json_data.index(start)
        end = json_data.index(end)
        for i in range(start,end+1):
            if (json_data[i]['production_A']):
                date,time = fetch_json.validate_json(json_data[i]['time'])
                if (time[0]*60)+time[1]+(time[2]/60) >= 360 and (time[0]*60)+time[1]+(time[2]/60) <= 840:
                    shiftA["production_A_count"]=shiftA["production_A_count"]+1
                elif (time[0]*60)+time[1]+(time[2]/60) >= 840 and (time[0]*60)+time[1]+(time[2]/60) <= 1200:
                    shiftB["production_A_count"]=shiftB["production_A_count"]+1
                else:
                    shiftC["production_A_count"]=shiftC["production_A_count"]+1
            if (json_data[i]['production_B']):
                date,time = fetch_json.validate_json(json_data[i]['time'])
                if (time[0]*60)+time[1]+(time[2]/60) >= 360 and (time[0]*60)+time[1]+(time[2]/60) <= 840:
                    shiftA["production_B_count"]=shiftA["production_B_count"]+1
                elif (time[0]*60)+time[1]+(time[2]/60) >= 840 and (time[0]*60)+time[1]+(time[2]/60) <= 1200:
                    shiftB["production_B_count"]=shiftB["production_B_count"]+1
                
                else:
                    shiftC["production_B_count"]=shiftC["production_B_count"]+1
        query_result = str({"shiftA":shiftA,"shiftB":shiftB,"shiftC":shiftC}) 
        query_result = json.loads(query_result.replace("'",'"'))
        
    return query_result
