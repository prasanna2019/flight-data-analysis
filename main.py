from api_call import fetch_data
import pandas as pd
from utils import create_logger

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

l= create_logger()

def main()-> None :
    content= fetch_data().json()
    df= pd.json_normalize(content)
    difference= set(required_columns)- set(df.columns)
    if difference:
        l.error('Required columns not in the data')
        return
    df= df[schema.keys()]
    for col, dtype in schema.items():
        if dtype in ['int', 'float']:
            converted= pd.to_numeric(df[col], errors='coerce')
            failed= df[col].notna() & converted.isna()
           
        elif dtype in ['timestamp', 'datetime']:
            converted= pd.to_datetime(df[col], errors='coerce')
            failed= df[col].notna() & converted.isna()

        else:
            converted= df[col].astype('string')
        failed= df[col].notna() & converted.isna()

        if(failed.any()):
            l.info(f'Errors in converting {col} data')
        df[col]= converted
    
    l.warning('Done processing')

    


    
    

main()

