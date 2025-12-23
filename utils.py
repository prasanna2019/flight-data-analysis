import pandas as pd
import logging
from google.cloud import bigquery
import os
from google.oauth2 import service_account
from google.api_core import retry, exceptions

account= os.getenv('__service_account')

custom_retry = retry.Retry(
predicate=retry.if_exception_type(
    exceptions.ServiceUnavailable,
    exceptions.InternalServerError,
    exceptions.DeadlineExceeded
),
initial=1.0,  # seconds
multiplier=2.0,
maximum=60.0  # max wait time
)

def bq_ingestion(df, project, destination):
    credentials = service_account.Credentials.from_service_account_file(
    account
    )   
    client = bigquery.Client(project= destination, credentials=credentials, default_retry=custom_retry)
    job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND"
    )



    job = client.load_table_from_dataframe(
        df,
        project+'.'+destination,
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


