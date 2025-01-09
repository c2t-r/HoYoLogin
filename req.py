import requests

def get(url: str, header: dict):
    response = requests.get(url, headers=header)
    return response

def post(url: str, header: dict, payload: dict):
    response = requests.post(url, headers=header, data=payload)
    return response

def parse_resp(response: requests.Response):
    if response.ok:
        resp_obj = response.json()
        return resp_obj
    else:
        response.raise_for_status()