import requests
import time

last_update=time.time()

def fetch_api(url:list[str], data:str = None, token:str = None, request:str = None):
    baseUrl="https://api.spacetraders.io/v2/"
    mockUrl="https://stoplight.io/mocks/spacetraders/spacetraders/96627693"
    headers={}
    global last_update
    time_to_wait=1.1-(time.time()-last_update)
    if(time_to_wait>0):
        time.sleep(time_to_wait)
    if data is not None:
        headers["Content-Type"]="application/json"
        headers["Accept"]="application/json"
    if token is not None:
        headers["Authorization"]="Bearer "+token
    if request is not None and request=="get":
        response=requests.get(url=baseUrl+"/".join(url),params=data,headers=headers)
    else:
        response=requests.post(url=baseUrl+"/".join(url),json=data,headers=headers)
    if response.status_code!=200:
        print(response.content)
    last_update=time.time()
    return response

