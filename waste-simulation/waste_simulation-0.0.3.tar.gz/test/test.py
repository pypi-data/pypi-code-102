### pip install waste-simulation
# import waste_simulation as ws 
import pandas as pd
from datetime import datetime
import re
data = pd.read_csv("otp_usage_summary_11.12.21.csv")
data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d"))
data_orders = pd.read_csv("suggested_otp.csv")
map = {"TENDERS": 3201 , "NUGGETS": 70,"BRKFST FILET NAE":72 , "FILETS": 1, "FILET GARLIC HERB":9884,"SPICY FILETS":3581,"NUGGETS GARLIC HERB":10681}
data_orders = data_orders[data_orders["VENDOR"]== "OFFSITE THAW"]
def match(x):
    y = re.search("^[\d]{4}-[\d]{2}-[\d]{2}",str(x))
    if y == None:
        return "hey"
    return re.search("^[\d]{4}-[\d]{2}-[\d]{2}",str(x)).group(0)

data_orders["date"] = data_orders["DATERECEIVED"].apply(lambda x: match(x))
data_orders  = data_orders[data_orders["date"]!= "hey"]
data_orders["date"] = data_orders["date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d"))
data_orders["map"] = data_orders["VENDOR_ITEM_DESCRIPTION"].apply(lambda x: map[re.search("CHICKEN, (.*) THW",x).group(1)])

df= data_orders.groupby(["date","map","storenumber"]).sum().reset_index()

data = data.merge(df,"inner", left_on=["Date","inventory_item_id","Location"], right_on=["date","map","storenumber"])

data["Date"] = data["Date"].apply(lambda x: datetime.strftime(x,"%Y-%m-%d"))
print("Start Process")
waste_data = ws.run(data,"Date","inventory_item_id","Name",3,["adjusted_forecast","forecast_usage","ORDEREDQTY"],
        "total_usage","2021-05-21","2021-10-26",3,None)

print("Finish")

waste_data.to_csv("test.csv")
