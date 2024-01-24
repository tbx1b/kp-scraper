# src/utils.py
from fake_useragent import UserAgent
import requests
import random
import re

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_random_proxy():
    response = requests.get("http://pubproxy.com/api/proxy")
    proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
    return random.choice(proxies)
