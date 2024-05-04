import asyncio
import json
import requests
from ... import config

class InvalidLocalNumberFormat(Exception):
    pass

async def send_simple_sms(message:str, target:str):
    headers = {
        'x-api-key': config.HTTPSMS_API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    payload = {
        "content": message,
        "from": config.HTTPSMS_ACTOR_NUMBER,
        "to": target
    }

    return requests.post(config.HTTPSMS_ENDPOINT_URL, headers = headers, data = json.dumps(payload))

async def send_batch_sms(message:str, targets:list[str]):
    headers = {
        'x-api-key': config.HTTPSMS_API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    for number in targets:
        payload = {
            "content": message,
            "from": config.HTTPSMS_ACTOR_NUMBER,
            "to": number
        }
        requests.post(config.HTTPSMS_ENDPOINT_URL, headers = headers, data = json.dumps(payload))

def format_local_number_philippines(number:str):
    # This just removes the 0 and adds a +63 in local numbers
    if (len(number) != 11) or (number[0] != '0'):
        raise InvalidLocalNumberFormat
    
    return ("+63" + number[1:])