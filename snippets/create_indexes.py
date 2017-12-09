"""Create indexes in a table.

Once the indexes have been created, querying with table.read or table.iterrows
should take the same amount of time, while querying with table.where or
table.read_where should be faster.

See Also
--------
- create_csindex: Create a completely sorted index (CSI) 
- Search with index might be slower than without index.
  This happens when the number of results is big.
  https://stackoverflow.com/questions/20769818/search-with-index-is-slower-than-without-index-in-pytables-when-the-result-is-la
"""
import os
import time
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    h5_file_path = os.path.join(data_dir, 'NYC-yellow-taxis-indexed.h5')

    table_where = '/yellow_{year}_{month}'.format(year='2015', month='01')

    # Indexes support compression!
    filters = tb.Filters(complevel=5, complib='blosc')

    t0 = time.time()
    # Indexes create a group in the HDF5 file, so we must open in 'a'ppend mode
    with tb.open_file(filename=h5_file_path, mode='a') as f:
        table = f.get_node(where=table_where)
        
        try:
            table.cols.total_amount.create_index(filters=filters)
        except ValueError as e:
            print(e)
            table.cols.total_amount.remove_index()
            print('Index removed. Create new index')
            table.cols.total_amount.create_index(filters=filters)

        try:
            table.cols.passenger_count.create_index(filters=filters)
        except ValueError as e:
            print(e)
            table.cols.passenger_count.remove_index()
            print('Index removed. Create new index')
            table.cols.passenger_count.create_index(filters=filters)

        try:
            table.cols.trip_distance.create_index(filters=filters)
        except ValueError as e:
            print(e)
            table.cols.trip_distance.remove_index()
            print('Index removed. Create new index')
            table.cols.trip_distance.create_index(filters=filters)

    t1 = time.time()
    print('Creating indexes took {:.2f}s'.format(t1 - t0))

if __name__ == '__main__':
    main()
