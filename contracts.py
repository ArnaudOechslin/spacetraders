import api_request

contract_list=None

def list_contracts(token:str,limit:int = None, page:int = None):
    data={}
    if limit is not None:
        data["limit"]=limit
    if page is not None:
        data["page"]=page
    return api_request.fetch_api(["my","contracts"],token=token,request="get",data=data)

def get_contract(token:str,id:str):
    return api_request.fetch_api(["my","contracts",id],token=token,request="get")

def accept_contract(token:str,id:str):
    return api_request.fetch_api(["my","contracts",id,"accept"],token=token)

def deliver_contract(token:str,id:str,shipSymbol:str = None, tradeSymbol:str = None, units:int = None):
    data={
        "shipSymbol":shipSymbol,
        "tradeSymbol":tradeSymbol,
        "units":units
    }
    return api_request.fetch_api(["my","contracts",id,"deliver"],token=token,json=data)

def fulfill_contract(token:str,id:str):
    return api_request.fetch_api(["my","contracts",id,"fullfill"],token=token)