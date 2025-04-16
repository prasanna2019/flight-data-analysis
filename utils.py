import pandas as pd

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df['flight_date']= pd.to_datetime(df['flight_date'], errors='coerce')
    df.drop_duplicates()
    df = df.dropna(subset=['flight_date'])
    return df

def viz(df: pd.DataFrame, str: str) -> str:
    return 'l'