from api_call import fetch_data
import pandas as pd

schema= {
   'flight_number': 'int',
   'mission_name': 'string',
   'launch_year': 'int',
   'launch_date_utc': 'timestamp',
   'rocket.rocket_id': 'string',
   'rocket.rocket_type': 'string',
   'rocket.rocket_name': 'string'
}

required_columns=['flight_number', 'rocket.rocket_id' ]

def main():
    content= fetch_data().json()
    df= pd.json_normalize(content)
    difference= [s for s in schema.keys() if s not in df.columns]
    if difference and set(required_columns) - set(difference):
        print("loggng code for later")
    else:
        df= df[schema.keys()]
        for col, dtype in schema.items():
            if dtype in ['int', 'float']:
                df[col]= pd.to_numeric(df[col], errors='coerce')
            else:
                df[col]= df[col].astype('string')
        print(df)


    
    

main()

