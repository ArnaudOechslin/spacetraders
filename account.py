import api_request

factions=[
    "COSMIC",
    "VOID",
    "GALACTIC",
    "QUANTUM",
    "DOMINION"
]



def create(username:str,faction:str) -> str:
    faction=faction if faction in factions else "COSMIC"
    return api_request.fetch_api(["register"],data={"faction":faction,"symbol":username})

def login(token:str):
    print("Lol")