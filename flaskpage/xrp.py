import requests

def get_xrp_price():
    #TODO get last updated time stamp from api (query param see api docs)
    payload={}
    headers = {}
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["ripple"]["usd"]


