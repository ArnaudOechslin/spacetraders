import account
import api_request
import sys
import contracts
import json
import systems
import agents
import fleet
import time

def main() -> int:
    f = open("token.txt","r")
    token=f.read()
    contract=json.loads(contracts.list_contracts(token).content)["data"][0]
    ore=contract["terms"]["deliver"][0]["tradeSymbol"]
    systems.load_all_systems()
    ship=json.loads(fleet.list_ships(token).content)["data"][0]
    shipSymbol=ship["symbol"]
    systemSymbol=ship["nav"]["systemSymbol"]
    cargo=fleet.get_ship_cargo(token,shipSymbol)
    survey=fleet.survey_specific_ressource(token,shipSymbol,"ALUMINUM_ORE",20)
    if survey is not None:
        timeToSleep=survey["cooldown"]["remainingSeconds"]
        print("Waiting for cooldown")
        time.sleep(timeToSleep)
        response=fleet.extract_ressources(token,shipSymbol,survey)
        print(response.content)
    else:
        response=fleet.extract_ressources(token,shipSymbol)
        print(response.content)
    return 0

if __name__ == '__main__':
    sys.exit(main())  