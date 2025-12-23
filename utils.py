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

def transform_flight_data(df):
    df = df.copy()
    
    # Convert flight_date to datetime
    df['flight_date'] = pd.to_datetime(df['flight_date'], errors='coerce')

    # Extract new time-based features
    df['year'] = df['flight_date'].dt.year
    df['month'] = df['flight_date'].dt.month
    df['day'] = df['flight_date'].dt.day
    df['weekday'] = df['flight_date'].dt.day_name()

    return df


