from api_call import fetch_data
import pandas as pd
from utils import create_logger
from utils import bq_ingestion
from dotenv import load_dotenv
import os
from google.cloud import bigquery
from google.oauth2 import service_account



schema= {
   'flight_number': 'int',
   'mission_name': 'string',
   'launch_year': 'int',
   'launch_date_utc': 'timestamp',
   'rocket_rocket_id': 'string',
   'rocket_rocket_type': 'string',
   'rocket_rocket_name': 'string'
}

required_columns=['flight_number', 'rocket_rocket_id' ]

l= create_logger()

def main()-> None :
    content= fetch_data().json()
    df= pd.json_normalize(content, sep= '_')
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
        err= bq_ingestion(df)
        l.warning(err)
    except:
        l.exception("Could not ingest data")

l.warning('Exiting...')

if __name__== "__main__":
    main()

