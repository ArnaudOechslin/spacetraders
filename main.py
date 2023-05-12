import account
import api_request
import sys
import contracts
import json
import systems

def main() -> int:
    f = open("token.txt","r")
    token=f.read()
    systems.list_systems(token,2)
    print(systems.list_shipyards(token))
    return 0

if __name__ == '__main__':
    sys.exit(main())  