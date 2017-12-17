import os
import time
import datetime
import numpy as np
import tables as tb
import pandas as pd

# data dictionary for NY yellow taxi CSV files
# http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
data_dictionary = {
    'vendor_id': 'A code indicating the TPEP provider that provided the record',
    'trip_distance': 'The elapsed trip distance in miles reported by the taximeter',
    'payment_type': 'A numeric code signifying how the passenger paid for the trip',
    'pickup_latitude': 'Pickup latitude in Mercator projection',
    'pickup_longitude': 'Pickup longitude in Mercator projection',
    'dropoff_latitude': 'Dropoff latitude in Mercator projection',
    'dropoff_longitude': 'Dropoff longitude in Mercator projection',
    'pickup_x': 'Pickup X location in meters',
    'pickup_y': 'Pickup Y location in meters',
    'dropoff_x': 'Dropoff X location in meters',
    'dropoff_y': 'Dropoff Y location in meters',
}


class TaxiTableDescription(tb.IsDescription):
    vendor_id = tb.UInt8Col(pos=0)
    pickup_timestamp_ms = tb.Int64Col()
    dropoff_timestamp_ms = tb.Int64Col()
    passenger_count = tb.UInt8Col()
    trip_distance = tb.Float32Col()
    pickup_latitude = tb.Float32Col()
    pickup_longitude = tb.Float32Col()
    dropoff_latitude = tb.Float32Col()
    dropoff_longitude = tb.Float32Col()
    pickup_x = tb.Float32Col()
    pickup_y = tb.Float32Col()
    dropoff_x = tb.Float32Col()
    dropoff_y = tb.Float32Col()
    fare_amount = tb.Float32Col()
    tip_amount = tb.Float32Col()
    total_amount = tb.Float32Col()
    payment_type = tb.UInt8Col()
    # rate_code_id = tb.UInt8Col(pos=13)


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    h5_file_path = os.path.join(data_dir, 'NYC-yellow-taxis-10k.h5')
    nyc_dir = os.path.join(data_dir, 'nyctaxi')
    years = os.listdir(nyc_dir)
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    filters = tb.Filters(complevel=5, complib='zlib')

    with tb.open_file(filename=h5_file_path, mode='w') as f:
        for year in years:
            for month in months:
                name = 'yellow_{}_{}'.format(year, month)
                title = 'NYC Yellow Taxi data for {}-{}'.format(month, year)
                f.create_table(
                    where='/', name=name, description=TaxiTableDescription,
                    title=title, filters=filters)
                table_where = '/{}'.format(name)
                for key, val in data_dictionary.items():
                    f.set_node_attr(
                        where=table_where, attrname=key, attrvalue=val)


if __name__ == '__main__':
    main()
