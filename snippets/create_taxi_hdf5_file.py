import os
import time
import datetime
import numpy as np
import tables as tb
import pandas as pd


class TaxiTableDescription(tb.IsDescription):
    vendor_id = tb.UInt8Col(pos=0)
    pickup_timestamp_ms = tb.Int64Col(pos=1)
    dropoff_timestamp_ms = tb.Int64Col(pos=2)
    passenger_count = tb.UInt8Col(pos=3)
    trip_distance = tb.Float32Col(pos=4)
    pickup_longitude = tb.Float32Col(pos=5)
    pickup_latitude = tb.Float32Col(pos=6)
    dropoff_longitude = tb.Float32Col(pos=7)
    dropoff_latitude = tb.Float32Col(pos=8)
    fare_amount = tb.Float32Col(pos=9)
    tip_amount = tb.Float32Col(pos=10)
    total_amount = tb.Float32Col(pos=11)
    # store_and_fwd_flag = tb.Float32Col(pos=12)


def date_to_timestamp_ms(date_obj):
    timestamp_in_nanoseconds = date_obj.astype('int64')
    timestamp_in_ms = (timestamp_in_nanoseconds / 1000000).astype('int64')
    return timestamp_in_ms


def fill_table(table, df):
    num_records = df.shape[0]  # it's equal to the chunksize used in read_csv
    row = table.row
    for i in range(num_records):
        row['vendor_id'] = df['VendorID'].values[i]

        pickup_ms = date_to_timestamp_ms(df['tpep_pickup_datetime'].values[i])
        row['pickup_timestamp_ms'] = pickup_ms
        dropoff_ms = date_to_timestamp_ms(df['tpep_dropoff_datetime'].values[i])
        row['dropoff_timestamp_ms'] = dropoff_ms

        row['passenger_count'] = df['passenger_count'].values[i]
        row['trip_distance'] = df['trip_distance'].values[i]

        row['pickup_longitude'] = df['pickup_longitude'].values[i]
        row['pickup_latitude'] = df['pickup_latitude'].values[i]
        row['dropoff_longitude'] = df['dropoff_longitude'].values[i]
        row['dropoff_latitude'] = df['dropoff_latitude'].values[i]

        row['fare_amount'] = df['fare_amount'].values[i]
        row['tip_amount'] = df['tip_amount'].values[i]
        row['total_amount'] = df['total_amount'].values[i]
        # row['store_and_fwd_flag'] = df['store_and_fwd_flag'].values[i]
        row.append()
    table.flush()


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    h5_file_path = os.path.join(data_dir, 'pytables-ny-taxis.h5')

    nyc_dir = os.path.join(data_dir, 'nyctaxi')
    # years = os.listdir(nyc_dir)
    years = ['2016']

    # data dictionary for NY yellow taxi CSV files
    # http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
    # ATTENTION: the data dictionary changes from year to year! This data
    # dictionary is only valid for 2016 data
    dtype = {
        'VendorID': 'uint8',
        'store_and_fwd_flag': 'category',
    }

    filters = tb.Filters(complevel=5, complib='zlib')

    # create a table that we will fill later on
    with tb.open_file(h5_file_path, 'w') as f:
        f.create_table(
            where='/', name='TaxiTable', description=TaxiTableDescription,
            title='NY Yellow Taxi data', filters=filters)

    # populate the table with data from CSV files
    with tb.open_file(h5_file_path, 'a') as f:
        table = f.root.TaxiTable
        # or, in alternative
        # table = list(f.walk_nodes('/', classname='Table'))[0]

        for year in years:
            year_dir = os.path.join(data_dir, 'nyctaxi', year)
            csv_files = os.listdir(year_dir)

            # read in chunks because these CSV files are too big
            for csv_file in csv_files:
                csv_file_path = os.path.join(year_dir, csv_file)
                chunksize = 1000
                for chunk in pd.read_csv(
                        csv_file_path, dtype=dtype, chunksize=chunksize, 
                        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime']):
                    df = chunk.reset_index()
                    # for debugging
                    # print(df.describe())
                    # print(df.head())
                    fill_table(table, df)


if __name__ == '__main__':
    main()
