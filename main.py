from api_call import fetch_data
import pandas as pd
from utils import create_logger
from utils import bq_ingestion
from utils import transform




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
    df = transform(content, schema, required_columns, l)

    if df is None:
        return

    try:
        err = bq_ingestion(df)
        l.warning(err)
    except Exception:
        l.exception("Could not ingest data")

l.warning('Exiting...')

if __name__== "__main__":
    main()

