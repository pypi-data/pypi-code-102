from .DateTime import DateTime
import time
import requests
import sys
import os
import json
import datetime
data_dict=None
def get_holiday_from_api(year=None):
    if not year:
        year=DateTime.Now().Year
    url="http://timor.tech/api/holiday/year/"+str(year)
    result=[]
    data=None
    for i in range(0, 3):
        try:
            # r = requests.post(url,data=json.dumps(params), headers={"Content-Type": "application/json"}, timeout=5)
            r = requests.get(url,timeout=5)
            data=r.json()
            break
        except:
            time.sleep(1)
            pass
    for key in data["holiday"]:
        if data["holiday"][key]["holiday"]:
            result.append(data["holiday"][key]["date"])

    return result

def get_holiday(year=None):
    global data_dict
    if not year:
        year=DateTime.Now().Year
    if not os.path.exists(".exobj"):
        os.mkdir(".exobj")
    if not os.path.exists(".exobj/exstock.json"):
        with open(".exobj/exstock.json","w",encoding='utf-8') as file:
            file.write("{}")
    
    if not data_dict:
        data_dict=json.loads(open(".exobj/exstock.json").read())

    holidays=data_dict.get(str(year))
    if not holidays:
        holidays=get_holiday_from_api(year)
        data_dict[str(year)]=holidays
        with open(".exobj/exstock.json","w+",encoding='utf-8') as file:
            file.write(json.dumps(data_dict))

    return holidays

def is_trading_day(dt)->bool:
    _dt=""
    if type(dt) is DateTime:
        _dt=dt.ToString('yyyy-MM-dd')
    elif type(dt) is datetime.datetime:
        _dt=dt.strftime('%Y-%m-%d')
    elif type(dt) is datetime.date:
        _dt=str(dt)
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    else:
        raise Exception("UNSUPPORTED TYPE:"+str(type(dt)))

    if _dt in get_holiday():
        return False
    if DateTime.Convert(_dt,"yyyy-MM-dd").WeekDay>=6:
        return False
    return True

def get_next_trading_day(dt)->DateTime:
    _dt=None
    if type(dt) is DateTime:
        _dt=dt
    elif type(dt) is datetime.datetime:
        _dt=DateTime.Convert(dt.strftime('%Y-%m-%d'),"yyyy-MM-dd")
    elif type(dt) is datetime.date:
        _dt=DateTime.Convert(str(dt),"yyyy-MM-dd")
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    
    if not _dt:
        raise Exception("UNSUPPORTED dt")

    while True:
        _dt=_dt.AddDays(1)
        if(is_trading_day(_dt)):
            return _dt.Date()

def get_last_trading_day(dt)->DateTime:
    _dt=None
    if type(dt) is DateTime:
        _dt=dt
    elif type(dt) is datetime.datetime:
        _dt=DateTime.Convert(dt.strftime('%Y-%m-%d'),"yyyy-MM-dd")
    elif type(dt) is datetime.date:
        _dt=DateTime.Convert(str(dt),"yyyy-MM-dd")
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    
    if not _dt:
        raise Exception("UNSUPPORTED dt")

    while True:
        _dt=_dt.AddDays(-1)
        if(is_trading_day(_dt)):
            return _dt.Date()