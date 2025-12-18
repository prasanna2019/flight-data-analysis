from api_call import fetch_data
import pandas as pd
import os
import requests


#api call for dummy data
data= requests.get("https://jsonplaceholder.typicode.com/users")
data= data.json()
df= pd.json_normalize(data)


schema= {
    "address.geo.lat": "float",
    "address.geo.lng": "float",
    "address.street": "string",
    "website2": "string",
    "website": "string",
    "company.name": "string",
    "phone": "string",
    "name": "string",
    "username": "string",
    "phone": "string"
}
'''

for col, type in schema.items(): 
    if col not in df.columns:
        print(f'column {col} not in dataframe')
        continue

    if type in ['int', 'int64', 'float', 'float64']:
        df[col]= pd.to_numeric(df[col],errors='coerce')
        continue

    if type in ['datetime', 'timestamp']:
        df[col]= pd.to_datetime(df[col], errors='coerce')
        continue

    else:
        df[col]= df[col].astype('string')
'''

    



#print(df.dtypes)



#content= fetch_data()
#data= content['data']
#df= pd.json_normalize(data)

#df1= df[["flight_date", "flight_status", "flight.number","flight.iata","airline.name", "airline.iata"]]


#print(df[(df['id']==1) | (df['id'] ==2)])

#select rows and columns using loc
#print(df.loc[3, ['id', 'name']])

#print(df.loc[df['website'].isnull() , ['name', 'id']])
'''
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "age": [25, 30, 35, 18, 22],
    "city": ["Delhi", "Mumbai", "Chennai", "Delhi", "Mumbai"]
})

def adults(x):
    return x > 18

df.loc[df['age']> 18, 'adults']= 'Adults'
df.loc[df['age']<= 18, 'adults']= 'Child'
print(df.groupby('city')['age'].mean())

'''

data = {
    'date': [
        '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',
        '2024-01-06', '2024-01-07', '2024-01-08', pd.NA , '2024-01-10'
    ],
    'city': [
        'Delhi', 'Mumbai', 'Chennai', 'Delhi', 'Mumbai',
        'Chennai', 'Delhi', 'Mumbai', 'Chennai', 'Delhi'
    ],
    'temperature': [12, 25, 30.3, 15.232323, 26, 31, 13, 27, 32, 49],
    'sales': [100, 120, 90, 130, 150, 80, 110, 160, 70, 140]
} 

df = pd.DataFrame(data)

#print(df.dtypes)

types={'date': 'date', 'temperature':'float' }

for col, type in types.items():
    if col== 'date':
        df[col]= pd.to_datetime(df[col], errors= 'coerce')
    if col=='temperature':
        df[col]= pd.to_numeric(df[col], errors= 'coerce')

grouped= df.groupby('city')['sales'].sum().reset_index(name='sales')
dates_full= pd.date_range(df['date'].min(), df['date'].max(),freq='D')
d= dates_full.difference(df['date'])
df.loc[df['temperature']> 30, 'temperature']= 30
df['weather']= pd.cut(df['temperature'], bins=[10, 20, 30,float('inf')], labels=['cold', 'moderate', 'hot'], right= False)
print(df)
      
