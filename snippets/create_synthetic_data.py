"""Create synthetic data to benchmark PyTables queries.

Usage
-----
# Generate 10 datasets of synthetic data
python create_synthetic_data.py -n 1000000
"""
import os
import argparse
import time
import tables as tb
import numpy as np


class SyntheticDataDescription(tb.IsDescription):
    unsigned_int_field = tb.UInt8Col(pos=0)
    int_field = tb.Int32Col(pos=1)
    float_field = tb.Float32Col(pos=2)
    bool_field = tb.BoolCol(pos=3)


def fill_table(table, data):
    num_records = len(data['integers'])
    print('Fill up the table with {} records'.format(num_records))
    # Get the record object associated with the table:
    row = table.row
    for i in range(num_records):
        row['unsigned_int_field'] = data['uintegers'][i]
        row['int_field'] = data['integers'][i]
        row['float_field'] = data['floats'][i]
        row['bool_field'] = data['booleans'][i]
        row.append()
    # Flush the table buffers
    table.flush()

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', '--num_records', type=int, default=1000, 
        help='Number of records to generate')
    return parser.parse_args()


def main():
    args = parse_args()
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-synthetic-data.h5')
    filters = tb.Filters(complevel=5, complib='zlib')

    size = args.num_records
    data = {
        'uintegers': np.random.randint(0, 255, size, dtype='uint8'),
        'integers': np.random.randint(low=-123, high=456, size=size, dtype='int32'),
        'floats': np.random.normal(loc=0, scale=1, size=size).astype(np.float32),
        'booleans': np.random.choice([True, False], size=size),
    }

    t0 = time.time()
    with tb.open_file(file_path, 'w') as f:
        table = f.create_table(
            where='/', name='data_table', description=SyntheticDataDescription,
            title='Synthetic data', filters=filters)

        fill_table(table, data)

    t1 = time.time()
    print('Creating the HDF5 file took {:.2f}s'.format(t1 - t0))


if __name__ == '__main__':
    main()
