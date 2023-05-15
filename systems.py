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
        #lets assume that no system will be inserted in the middle of the list
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
        market=json.loads(_get_market(token,systemSymbol,waypointSymbol).content)
        if "data" in market.keys():
            markets[key]=market["data"]
    return markets[key]
    
def get_shipyard(token:str,systemSymbol:str,waypointSymbol:str):
    global shipyards
    key=systemSymbol+"|"+waypointSymbol
    if shipyards is None or key not in shipyards.keys():
        if shipyards is None:
            shipyards={}
        shipyard=json.loads(_get_shipyard(token,systemSymbol,waypointSymbol).content)
        if "data" in shipyard.keys():
            shipyards[key]=shipyard["data"]
    return shipyards.get(key)

def get_jumpgate(token:str,systemSymbol:str,waypointSymbol:str):
    global jumpgates
    key=systemSymbol+"|"+waypointSymbol
    if jumpgates is None or key not in jumpgates.keys():
        if jumpgates is None:
            jumpgates={}
        jumpgate=json.loads(jumpgate(token,systemSymbol,waypointSymbol).content)
        if "data" in jumpgate.keys():
            jumpgates[key]=jumpgate["data"]
    return jumpgates[key]

def find_waypoints_with_trait(token:str,systemSymbol:str,traitName:str):
    waypoints=[]
    for waypoint in list_waypoints(token,systemSymbol):
        for trait in waypoint["traits"]:
            if trait["symbol"].lower()==traitName.lower():
                waypoints+=[waypoint]
                break
    return waypoints

def find_waypoints_with_type(token:str,systemSymbol:str,typeName:str):
    waypoints=[]
    for waypoint in list_waypoints(token,systemSymbol):
        if waypoint["type"].lower()==typeName.lower():
            waypoints+=[waypoint]
            break
    return waypoints

def list_shipyards(token:str):
    for systemSymbol in [system["symbol"] for system in list_systems(token)]:
        for waypointSymbol in [waypoint["symbol"] for waypoint in find_waypoints_with_trait(token,systemSymbol,"shipyard")]:
            get_shipyard(token,systemSymbol,waypointSymbol) #lazy updating
    return shipyards

def save_all_systems(token:str):
    metadata=json.loads(_list_systems(token,1).content)["meta"]
    list_systems(token,metadata["total"]//metadata["limit"])
    f=open("./systemcache/systems.json","w")
    f.write(json.dumps(systems))
    f.close()


def load_all_systems():
    global systems
    f=open("./systemcache/systems.json","r")
    systems=json.loads(f.read())
    f.close()


def save_all_waypoints(token:str):

    totalSystems=json.loads(_list_systems(token,1).content)["meta"]["total"]
    if totalSystems > len(systems):
        save_all_systems(token)
    for i,system in enumerate(list_systems(token)):
        print(f'Checking waypoints in {system["symbol"]}({i+1}/{totalSystems})')
        if len(system["waypoints"])==0:
            print("No waypoints in this system, continuing")
            continue
        if "traits" not in system["waypoints"][0].keys():
            print("No waypoints stored, querying API")
            list_waypoints(token,system["symbol"])
            print("saving")
            f=open("./systemcache/systems.json","w")
            f.write(json.dumps(systems))
            f.close()
        else:
            print("System up to date, continuing")

def find_all_systems_within_range(token:str,systemSymbol:str,range:int = 5000):
    systemSymbolList=[]
    startSystem=get_system(token,systemSymbol)
    x0,y0=startSystem["x"],startSystem["y"]

    for system in list_systems(token):
        if system["symbol"]==systemSymbol:
            continue
        if "JUMP_GATE" not in str(system):
            continue
        x,y=system["x"],system["y"]
        if (x-x0)**2+(y-y0)**2<=range**2:
            systemSymbolList+=[system["symbol"]]
    return systemSymbolList

def find_jump_route(token:str,startSymbol:str,destinationSymbol:str):
    surveyedSystems=[startSymbol]
    surveyedFrom={}
    systemsToSurvey=[startSymbol]
    for system in systemsToSurvey:
        reachableSystems=find_all_systems_within_range(token,system)
        for reachableSystem in reachableSystems:
            if reachableSystem not in surveyedSystems:
                systemsToSurvey.append(reachableSystem)
                surveyedFrom[reachableSystem]=system
                surveyedSystems.append(reachableSystem)
        if destinationSymbol in surveyedSystems:
            break

    if destinationSymbol not in surveyedSystems:
        return None
    chain=[destinationSymbol]
    currentSystem=destinationSymbol
    while currentSystem!=startSymbol:
        chain=[surveyedFrom[currentSystem]]+chain
        currentSystem=surveyedFrom[currentSystem]
    return chain

