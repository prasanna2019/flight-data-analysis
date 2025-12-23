from api_call import fetch_data
import pandas as pd
from utils import create_logger
from utils import bq_ingestion
from dotenv import load_dotenv
import os

load_dotenv()
project= os.getenv('__project')
destination= os.getenv('__destination')

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
           
        elif dtype in ['timestamp', 'datetime']:
            converted= pd.to_datetime(df[col], errors='coerce')
            

        else:
            converted= df[col].astype('string')

        failed= df[col].notna() & converted.isna()
        if(failed.any()):
            l.info(f'Errors in converting {col} data')
        df[col]= converted
    try:

        test= bq_ingestion(df, project, destination)
    except:
        l.fatal(f'Could not ingest data in table')
    
    l.warning('Exiting...')

    


    
    

main()

