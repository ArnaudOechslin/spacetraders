import api_request
import time
import datetime
import json
import contracts

def list_ships(token:str,limit:int = 20, page:int = 1):
    limit=max(min(limit, 20), 1)
    page=max(1,page)
    return api_request.fetch_api(["my","ships"],token=token,request="get",data={"page":page,"limit":limit})

def purchase_ship(token:str,shipType:str,waypointSymbol:str):
    return api_request.fetch_api(["my","ships"],token=token,data={"shipType":shipType,"waypointSymbol":waypointSymbol})

def get_ship(token:str,shipSymbol:str):
    return api_request.fetch_api(["my","ships",shipSymbol],request="get",token=token)

def get_ship_cargo(token:str,shipSymbol:str):
    return api_request.fetch_api(["my","ships",shipSymbol,"cargo"],request="get",token=token)

def orbit_ship(token:str,shipSymbol:str):
    return api_request.fetch_api(["my","ships",shipSymbol,"orbit"],token=token)

def ship_refine(token:str,shipSymbol:str,produce:str):
    return api_request.fetch_api(["my","ships",shipSymbol,"refine"],token=token,data={"produce":produce})

def create_chart(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"chart"],token=token)

def get_ship_cooldown(token:str,shipSymbol:str):
    return api_request.fetch_api(["my","ships",shipSymbol,"cooldown"],request="get",token=token)

def dock_ship(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"dock"],token=token)

def create_survey(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"survey"],token=token)

def extract_ressources(token:str,shipSymbol:str, survey:str = None):
     if survey is not None:
          return api_request.fetch_api(["my","ships",shipSymbol,"extract"],token=token,data=survey)
     else:
          return api_request.fetch_api(["my","ships",shipSymbol,"extract"],token=token)

def jettison_cargo(token:str,shipSymbol:str,cargoSymbol:str,units:int = 1):
     units=max(1,units)
     return api_request.fetch_api(["my","ships",shipSymbol,"jettison"],token=token,data={"symbol":cargoSymbol,"units":units})

def jump_ship(token:str,shipSymbol:str,systemSymbol):
     return api_request.fetch_api(["my","ships",shipSymbol,"jump"],token=token,data={"systemSymbol":systemSymbol})

def navigate_ship(token:str,shipSymbol:str,waypointSymbol):
     return api_request.fetch_api(["my","ships",shipSymbol,"navigate"],token=token,data={"waypointSymbol":waypointSymbol})

def get_ship_nav(token:str,shipSymbol:str):
    return api_request.fetch_api(["my","ships",shipSymbol,"nav"],request="get",token=token)

def warp_ship(token:str,shipSymbol:str,waypointSymbol):
     return api_request.fetch_api(["my","ships",shipSymbol,"warp"],token=token,data={"waypointSymbol":waypointSymbol})

def sell_cargo(token:str,shipSymbol:str,cargoSymbol:str,units:int = 1):
     units=max(1,units)
     return api_request.fetch_api(["my","ships",shipSymbol,"sell"],token=token,data={"symbol":cargoSymbol,"units":units})

def scan_systems(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"scan","systems"],token=token)

def scan_waypoints(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"scan","waypoints"],token=token)

def scan_ships(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"scan","ships"],token=token)

def refuel_ship(token:str,shipSymbol:str):
     return api_request.fetch_api(["my","ships",shipSymbol,"refuel"],token=token)

def purchase_cargo(token:str,shipSymbol:str,cargoSymbol:str,units:int = 1):
     return api_request.fetch_api(["my","ships",shipSymbol,"purchase"],token=token,data={"symbol":cargoSymbol,"units":units})

def transfer_cargo(token:str,shipSymbol:str,targetShipSymbol:str,cargoSymbol:str,units:int = 1):
     return api_request.fetch_api(["my","ships",shipSymbol,"transfer"],token=token,data={"symbol":cargoSymbol,"units":units,"tradeSymbol":targetShipSymbol})


def survey_specific_ressource(token:str,shipSymbol:str,ressource:str,attempts:int = 5):
     survey=None
     attemps=max(1,min(20,attempts))-1
     response=create_survey(token,shipSymbol)
     while ressource not in str(response.content) and attempts>0:
          attemps-=1
          print(f'No {ressource} found in <{response.content}>, waiting for the next survey')
          wait_for_cooldown(response)  
          response=create_survey(token,shipSymbol)
     if ressource in str(response.content):
          survey=json.loads(response.content)["data"]
     return survey

def wait_for_cooldown(token:str,shipSymbol:str):
    response=get_ship_cooldown(token,shipSymbol)
    if response.status_code==204:
        print("No cooldown")
        return None
    if response.status_code!=200:
         print("Error")
         return None
    timeToSleep=json.loads(response.content)["data"]["remainingSeconds"]
    for i in range(timeToSleep):
        #if (timeToSleep-i)%5==0:
            #print(f'{timeToSleep-i} seconds left on cooldown')
        time.sleep(1)

def cargo_left(token:str,shipSymbol:str):
     response=get_ship_cargo(token,shipSymbol)
     return json.loads(response.content)["data"]["capacity"]-json.loads(response.content)["data"]["units"]

def get_inventory(token:str,shipSymbol:str):
    shipInfo=json.loads(get_ship(token,shipSymbol).content)["data"]
    return shipInfo["cargo"]["inventory"]

def sell_everything(token:str,shipSymbol:str,keep = ["ANTIMATTER"]):
    inventory = get_inventory(token,shipSymbol)
    for item in inventory:
        if item["symbol"] not in keep:
          response=sell_cargo(token,shipSymbol, item["symbol"],item["units"])
          if response.status_code==201:
               totalPrice=json.loads(response.content)["data"]["transaction"]["totalPrice"]
               print(f'{shipSymbol} sold {item["units"]} {item["symbol"]} for {totalPrice}')

def deliver_all(token:str,contractId:str,shipSymbol:str,items):
    inventory = get_inventory(token,shipSymbol)
    for item in inventory:
        if item["symbol"] in items:
            print(f'{shipSymbol} delivering {item["symbol"]}')
            contracts.deliver_contract(token,contractId,shipSymbol,item["symbol"],item["units"])

def dump_all_cargo(token:str,shipSymbol:str,keep = ["ANTIMATTER"]):
    inventory = get_inventory(token,shipSymbol)
    for item in inventory:
        if item["symbol"] not in keep:
            print(f'{shipSymbol} dumping {item["symbol"]}')
            jettison_cargo(token,shipSymbol,item["symbol"],item["units"])

def wait_for_ship_arrival(token:str,shipSymbol:str):
    response=get_ship_nav(token,shipSymbol)
    arrivalTime=datetime.datetime.fromisoformat(json.loads(response.content)["data"]["route"]["arrival"])
    timeToSleep=int(arrivalTime.timestamp()-time.time())
    if timeToSleep>0:
        for i in range(timeToSleep):
            #if (timeToSleep-i)%5==0:
               #print(f'{timeToSleep-i} seconds left until arrival')
            time.sleep(1)
