from . import fetch_json

def main_(start,end):
    start_time = fetch_json.validate_input(start)
    end_time = fetch_json.validate_input(end)
    if (start_time[0] and end_time[0]):
        return get_result(start_time,end_time)
    else:
        return {"invalid_data":"check format and range of date and time. Make sure the request is in follwoing text format "}


def get_result(start_time,end_time):
    json_url = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json"
    start,end,json_data = fetch_json.find_range(start_time,end_time,json_url)
    if start==None or end==None:
        query_result = {"invalid_request":"Check date and time format"}
    else:
        query_result = []
        start = json_data.index(start)
        end = json_data.index(end)
        id_dict = {}
        for i in range(start,end+1):
            id_ = int(json_data[i]['id'].strip('ch00'))
            belt1 = 0
            belt2 = 0
            if (json_data[i]['state']):
                belt1 = 0
                belt2 = json_data[i]['belt2']
            else:
                belt1 = json_data[i]['belt1']
                
                belt2 = 0
            if id_ in id_dict:
                id_dict[id_]['belt1'][0], id_dict[id_]['belt1'][1] = id_dict[id_]['belt1'][0]+belt1, id_dict[id_]['belt1'][1]+1 
                id_dict[id_]['belt2'][0], id_dict[id_]['belt2'][1] = id_dict[id_]['belt2'][0]+belt2, id_dict[id_]['belt2'][1]+1 
            else:
                new_belt = {'belt1':[int(belt1),1],'belt2':[int(belt2),1]}
                id_dict[id_] = new_belt
        for i in sorted(id_dict):
            b1_avg = id_dict[i]['belt1'][0] / id_dict[i]['belt1'][1]
            b2_avg = id_dict[i]['belt2'][0] / id_dict[i]['belt2'][1]
            query_result.append({"id" : i,"avg_belt1" : int(b1_avg), "avg_belt2" : int(b2_avg)}) 
    return query_result

