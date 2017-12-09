import os
import time
import tables as tb
import pandas as pd


def date_to_timestamp_ms(date_obj):
    timestamp_in_nanoseconds = date_obj.astype('int64')
    timestamp_in_ms = (timestamp_in_nanoseconds / 1000000).astype('int64')
    return timestamp_in_ms


def fill_table(table, mapping, df):
    num_records = df.shape[0]  # it's equal to the chunksize used in read_csv
    row = table.row
    for i in range(num_records):
        row['vendor_id'] = df[mapping['vendor_id']].values[i]

        pickup_ms = date_to_timestamp_ms(df[mapping['pickup_datetime']].values[i])
        row['pickup_timestamp_ms'] = pickup_ms
        dropoff_ms = date_to_timestamp_ms(df[mapping['dropoff_datetime']].values[i])
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

        row['payment_type'] = df['payment_type'].values[i]
        row.append()
    table.flush()


def get_year_and_month(file_name):
    # we could also use a regex like '[0-9]){4}-([0-9]){2}\.csv'
    a, b, c = file_name.split('_')
    period, extension = c.split('.')
    year, month = period.split('-')
    return year, month


def get_csv_mapping(year, month):
    """CSV files from different year/month have some different field names.

    Parameters
    ----------
    year : int
    month : int

    Returns
    -------
    mapping : dict

    See Also
    --------
    data dictionary for NY yellow taxi CSV files
    http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
    """
    # To the left, the key we want to use. To the right, the key in the CSV file
    if year == '2014':
        mapping = {
            'vendor_id': 'vendor_id',
            'pickup_datetime': 'pickup_datetime',
            'dropoff_datetime': 'dropoff_datetime',
            # 'rate_code_id': 'rate_code',
        }
    elif year == '2015' or (year == '2016' and 1 <= int(month) <= 6):
        mapping = {
            'vendor_id': 'VendorID',
            'pickup_datetime': 'tpep_pickup_datetime',
            'dropoff_datetime': 'tpep_dropoff_datetime',
            # sometimes it's RateCodeID, others RatecodeID...
            # 'rate_code_id': 'RateCodeID',
        }
    else:
        raise NotImplementedError('data dictionary not defined for this period')

    return mapping


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    h5_file_path = os.path.join(data_dir, 'NYC-yellow-taxis.h5')
    nyc_dir = os.path.join(data_dir, 'nyctaxi')
    years = os.listdir(nyc_dir)

    # Open the HDF5 file in 'a'ppend mode and populate the table with CSV data
    with tb.open_file(filename=h5_file_path, mode='a') as f:
        for year in years:
            year_dir = os.path.join(data_dir, 'nyctaxi', year)
            csv_files = os.listdir(year_dir)

            for csv_file in csv_files:
                year, month = get_year_and_month(csv_file)
                mapping = get_csv_mapping(year, month)
                # define the dtype to use when reading the CSV with pandas (this
                # has nothing to do with the HDF5 table)
                dtype = {
                    mapping['vendor_id']: 'category',
                    'store_and_fwd_flag': 'category',
                    'payment_type': 'category',
                }
                parse_dates = [
                    mapping['pickup_datetime'], mapping['dropoff_datetime']
                ]

                table_where = '/yellow_{}_{}'.format(year, month)
                table = f.get_node(where=table_where)

                t0 = time.time()
                print('Processing {} started'.format(csv_file))
                csv_file_path = os.path.join(year_dir, csv_file)

                # read in chunks because these CSV files are too big
                chunksize = 10000
                for chunk in pd.read_csv(
                    csv_file_path, chunksize=chunksize, dtype=dtype,
                    skipinitialspace=True, parse_dates=parse_dates):
                    # print('Processing chunk')
                    df = chunk.reset_index(drop=True)
                    # print(df.describe())
                    # print(df.head())
                    fill_table(table, mapping, df)
                    # debugging tip: put a break here, so you can inspect what
                    # has been written in the table
                    break
                    # print('Next chunk')

                t1 = time.time()
                print('Processing {} took {:.2f}s'.format(csv_file, (t1 - t0)))


if __name__ == '__main__':
    main()
