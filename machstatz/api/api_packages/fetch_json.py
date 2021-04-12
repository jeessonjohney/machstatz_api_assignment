import requests, json

def validate_input(str_inp):
    try:
        date,time = str_inp.split('T')
        date = date.strip('"').split('-')
        time = time.strip('"').strip('Z').split(':')    
        date = list(map(int,date))
        time = list(map(int,time))
        if time[0] >23 or time[1]>60 or time[2]>60:
            return [False]
        else:
            return [True,date,time]
    except ValueError as v_err:
        return [False]

def validate_json(str_inp):
    date,time = str_inp.split(' ')
    date = date.strip('"').split('-')
    time = time.strip('"').strip('Z').split(':')    
    date = list(map(int,date))
    time = list(map(int,time))
    return [date,time]


def find_range(s_time,e_time,json_url):
    
    url = requests.get(json_url)
    json_data = json.loads(url.text)
    i=0
    end = None
    start = None
    for json_ in json_data:
        date,time = validate_json(json_['time']) 
        
        if time[0]<=24 and time[1]<=60 and time[2]<=60:
            if date[2] == (s_time[1][2]) and ((s_time[2][0]*60)+s_time[2][1] <= (time[0]*60)+time[1]+(time[2]/60)):
                start = json_
                break
        i+=1
    j=0
    for json_ in json_data[i:]:
        date,time = validate_json(json_['time'])
        if time[0]<=24 and time[1]<=60 and time[2]<=60:   
            if date[2] == (e_time[1][2]) and ((e_time[2][0]*60)+e_time[2][1]+(e_time[2][2]/60) == (time[0]*60)+time[1]+(time[2]/60)): 
                end = json_
                break
            if date[2] == (e_time[1][2]) and ((e_time[2][0]*60)+e_time[2][1]+(e_time[2][2]/60) < (time[0]*60)+time[1]+(time[2]/60)):
                end = json_data[j+i-1]
                break
        j+=1
    return [start,end,json_data]
        