import api_request

def my_agent_details(token:str):
    return api_request.fetch_api(["my","agent"],request="get",token=token)
