from json import dumps
from req import post

def send(webhook_url, content: dict):
    response = post(webhook_url, payload=dumps(content), header={
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    return response