import os
import time
import datetime
import numpy as np
import tables as tb
import pandas as pd


class TaxiTableDescription(tb.IsDescription):
    # vendor_id = tb.UInt8Col(pos=0)
    vendor_id = tb.StringCol(8, pos=0)  # 8-character String
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


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    h5_file_path = os.path.join(data_dir, 'pytables-ny-taxis.h5')
    nyc_dir = os.path.join(data_dir, 'nyctaxi')

    filters = tb.Filters(complevel=5, complib='zlib')

    with tb.open_file(h5_file_path, 'w') as f:
        f.create_table(
            where='/', name='TaxiTable', description=TaxiTableDescription,
            title='NY Yellow Taxi data', filters=filters)


if __name__ == '__main__':
    main()
