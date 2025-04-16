from api_call import fetch_data
import pandas as pd

flights_info= fetch_data()
flight_status= []
flight_date= []
departure= []
arrival= []

if 'data' in flights_info:
    flights= flights_info['data']
    for f in flights:
        flight_status.append(f['flight_status'])
        flight_date.append(f['flight_date'])
        departure.append(f['departure']['airport'])
        arrival.append(f['arrival']['airport'])
    flights_df= pd.DataFrame(data= {'flight_date': flight_date, 'flight_status': flight_status, 'departure': departure, 'arrival': arrival}) 
    print(flights_df)

