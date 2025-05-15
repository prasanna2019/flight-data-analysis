import requests
__url= 'https://api.aviationstack.com/v1/flights?access_key='
__key= ''
print(__url+__key)
def fetch_data():
    response= requests.get(__url+__key)
    data= response.json()
    return data


