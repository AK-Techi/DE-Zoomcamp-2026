#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click



dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table-name', default='yellow_taxi_data', help='Target table name')
def run(pg_user, pg_password, pg_host, pg_port, pg_db, table_name):
    year = 2020
    month = 10
    chunksize = 100000

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    ingest_file = f'yellow_tripdata_{year}-{month}.csv.gz'
    tripdata = f'{prefix}/{ingest_file}'

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')


    df_iter = pd.read_csv(
        prefix + ingest_file,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            #create table schema with no data
            df_chunk.head(0).to_sql(
                name=table_name, 
                con=engine, 
                if_exists='replace'
            )
            first = False
            print("Table created")

        #insert data in chunks
        df_chunk.to_sql(
            name=table_name, 
            con=engine, 
            if_exists='append'
        )

        #print the status of data insertion
        print("Inserted:", len(df_chunk))


if __name__ == '__main__':
    run()





