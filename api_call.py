import requests, os
from dotenv import load_dotenv
import json

load_dotenv()
url= os.getenv('__url')
key= os.getenv('__api_key')
print(url+key)
def fetch_data():
    response= requests.get(url)
    
    return response




