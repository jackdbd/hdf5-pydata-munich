import os
import time
import pandas as pd

# data dictionary
# http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
dtype = {
    'vendor_name': 'category',
    'Payment_Type': 'category',
}


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    # TODO: don't read! Too big to fit into my RAM. Use Dask or save it to a
    # SQLite DB
    # http://pythondata.com/dask-large-csv-python/
    # http://pythondata.wpengine.com/working-large-csv-files-python/
    # file_path = os.path.join(data_dir, 'yellow_tripdata_2016-01.csv')
    t0 = time.time()
    # http://tomaugspurger.github.io/scalable-ml-01.html
    df = pd.read_csv(
        file_path, dtype=dtype,
        # parse_dates=['Trip_Pickup_DateTime', 'Trip_Dropoff_DateTime'],
    )
    t1 = time.time()
    print('Reading {} took {:.2f}s'.format(file_path, t1 - t0))
    df.head()

if __name__ == '__main__':
    main()
