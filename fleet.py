import api_request
import time
import json

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
          if response.status_code<300:
               timeToSleep=json.loads(response.content)["data"]["cooldown"]["remainingSeconds"]
          else:
               timeToSleep=json.loads(response.content)["error"]["data"]["cooldown"]["remainingSeconds"]
          for i in range(timeToSleep):
               if (timeToSleep-i)%5==0:
                    print(f'{timeToSleep-i} seconds left until next survey')
               time.sleep(1)
                    
          response=create_survey(token,shipSymbol)
     if ressource in str(response.content):
          survey=json.loads(response.content)["data"]
     return survey