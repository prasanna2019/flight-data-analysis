import pandas as pd
import logging
from google.cloud import bigquery
import os
from google.oauth2 import service_account




def bq_ingestion(df):
    account= os.getenv('__service_account')
    project= os.getenv('__project')
    destination= os.getenv('__destination')
    credentials = service_account.Credentials.from_service_account_file(
        account
    )   
    table_ref= f"{project}.{destination}"
    client = bigquery.Client(project= project, credentials=credentials)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"
    )



    job = client.load_table_from_dataframe(
        df,
       table_ref,
        job_config=job_config
    )
    return job.result()


def create_logger():
    logging.basicConfig(
        filename='logs.log',
        format= '%(asctime)s | %(levelname)s | %(message)s',
        filemode='a'
    )

    # Creating an object
    logger = logging.getLogger()
    return logger

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df['flight_date']= pd.to_datetime(df['flight_date'], errors='coerce')
    df.drop_duplicates()
    df = df.dropna(subset=['flight_date'])
    return df

def viz(df: pd.DataFrame, str: str) -> str:
    return 'l'

def clean_flight_data(df):
    df = df.copy()
    
    # Strip whitespace and standardize text case
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype(str).str.strip().str.title()
    
    # Drop exact duplicates
    df = df.drop_duplicates()

    # Handle missing values (e.g., drop or fill)
    df = df.dropna(subset=['flight_date', 'departure', 'arrival'])

    return df


def transform(content: dict, schema: dict, required_columns: list, logger):
    df = pd.json_normalize(content, sep='_')

    difference = set(required_columns) - set(df.columns)
    if difference:
        logger.error('Required columns not in the data')
        return None

    df = df[list(schema.keys())]

    for col, dtype in schema.items():
        if dtype in ['int', 'float']:
            converted = pd.to_numeric(df[col], errors='coerce')

        elif dtype in ['timestamp', 'datetime']:
            converted = pd.to_datetime(df[col], errors='coerce')

        else:
            converted = df[col].astype('string')

        failed = df[col].notna() & converted.isna()
        if failed.any():
            logger.info(f'Errors in converting {col} data')

        df[col] = converted
    df= df.drop_duplicates(subset=['flight_number'], keep= 'last')
    return df


