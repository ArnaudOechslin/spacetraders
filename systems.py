import api_request
import json

def _list_systems(token:str,page:int = 1, limit:int = 20):
    if page<1:
        page=1
    if limit<1 or limit>20:
        limit=20
    return api_request.fetch_api(["systems"],token=token,request="get",data={"page":page,"limit":limit})

def _get_system(token:str,systemSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol],token=token,request="get")

def _list_waypoints(token:str,systemSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol,"waypoints"],token=token,request="get")

def _get_waypoint(token:str,systemSymbol:str,waypointSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol,"waypoints",waypointSymbol],token=token,request="get")

def _get_market(token:str,systemSymbol:str,waypointSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol,"waypoints",waypointSymbol,"market"],token=token,request="get")

def _get_shipyard(token:str,systemSymbol:str,waypointSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol,"waypoints",waypointSymbol,"shipyard"],token=token,request="get")

def _get_jumpgate(token:str,systemSymbol:str,waypointSymbol:str):
    return api_request.fetch_api(["systems",systemSymbol,"waypoints",waypointSymbol,"jump-gate"],token=token,request="get")



systems=None
markets=None
shipyards=None
jumpgate=None

def list_systems(token:str,maxPages:int = 1):
    global systems
    if systems is None or len(systems)/20<maxPages:
        if systems is None:
            systems=[]
        for i in range(len(systems)//20+1,maxPages+1):
            print(f'Loading systems page {i}/{maxPages}')
            systems+=json.loads(_list_systems(token,page=i).content)["data"]
    return systems

def find_system(systemSymbol:str):
    global systems
    for system in systems:
        if system["symbol"]==systemSymbol:
            return system
    return None

def get_system(token:str,systemSymbol:str):
    global systems
    if systems is None:
        list_systems(token)
    return find_system(systemSymbol)

def list_waypoints(token:str,systemSymbol:str):
    global systems
    if systems is None:
        list_systems(token)
    index=0
    for i in range(len(systems)):
        if systems[i]["symbol"]==systemSymbol:
            index=i
    if len(systems[index]["waypoints"]) > 0 and "traits" not in systems[index]["waypoints"][0].keys():
        systems[index]["waypoints"]=json.loads(_list_waypoints(token,systemSymbol).content)["data"]
    return systems[index]["waypoints"]

def find_waypoint(system,waypointSymbol:str):
    for waypoint in system["waypoints"]:
        if waypoint["symbol"]==waypointSymbol:
            return waypoint
    return None

def get_waypoint(token:str,systemSymbol:str,waypointSymbol:str):
    index=0
    system=find_system(systemSymbol)
    if "traits" not in system["waypoints"][0].keys():
        list_waypoints(token,systemSymbol)
    return find_waypoint(system,waypointSymbol)

def get_market(token:str,systemSymbol:str,waypointSymbol:str):
    global markets
    key=systemSymbol+"|"+waypointSymbol
    if markets is None or key not in markets.keys():
        if markets is None:
            markets={}
        markets[key]=json.loads(_get_market(token,systemSymbol,waypointSymbol).content)["data"] 
    return markets[key]
    
def get_shipyard(token:str,systemSymbol:str,waypointSymbol:str):
    global shipyards
    key=systemSymbol+"|"+waypointSymbol
    if shipyards is None or key not in shipyards.keys():
        if shipyards is None:
            shipyards={}
        shipyards[key]=json.loads(_get_shipyard(token,systemSymbol,waypointSymbol).content)["data"] 
    return shipyards[key]

def get_jumpgate(token:str,systemSymbol:str,waypointSymbol:str):
    global jumpgates
    key=systemSymbol+"|"+waypointSymbol
    if jumpgates is None or key not in jumpgates.keys():
        if jumpgates is None:
            jumpgates={}
        jumpgates[key]=json.loads(_get_jumpgate(token,systemSymbol,waypointSymbol).content)["data"] 
    return jumpgates[key]

def find_waypoints_with_trait(token:str,systemSymbol:str,traitName:str):
    waypoints=[]
    
    for waypoint in list_waypoints(token,systemSymbol):
        for trait in waypoint["traits"]:
            if trait["symbol"].lower()==traitName.lower():
                waypoints+=[waypoint]
                break
    return waypoints

def list_shipyards(token:str):
    for systemSymbol in [system["symbol"] for system in list_systems(token)]:
        for waypointSymbol in [waypoint["symbol"] for waypoint in find_waypoints_with_trait(token,systemSymbol,"shipyard")]:
            get_shipyard(token,systemSymbol,waypointSymbol) #lazy updating
    return shipyards