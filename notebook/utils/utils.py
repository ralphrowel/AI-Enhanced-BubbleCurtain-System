# utils/utils.py
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def get_db_engine(user, password, host, port, db):
    """Return SQLAlchemy engine for PostgreSQL"""
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def fetch_table(engine, table_name):
    """Fetch entire table from DB"""
    return pd.read_sql_table(table_name, engine)

def preprocess_signal(df):
    """Example preprocessing for signal data"""
    df = df.sort_values("timestamp")
    df = df.fillna(method="ffill")
    return df
