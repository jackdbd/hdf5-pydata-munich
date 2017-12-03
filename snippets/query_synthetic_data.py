import time
import os
import tables as tb
from hurry.filesize import size


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-synthetic-data.h5')

    with tb.open_file(file_path, 'r') as hdf:
        table = hdf.root.data_table
        print(table)
        print('Table size in memory: {}'.format(size(table.size_in_memory)))
        print('Table size on disk: {}'.format(size(table.size_on_disk)))
        print('Row size: {}'.format(size(table.rowsize)))

        # querying with numpy is possible only it the table fits in memory
        t0 = time.time()
        results = [x['bool_field'] for x in table.read()
                   if -100 < x['int_field'] < 100 and x['float_field'] > 0.5]
        t1 = time.time()
        print('Querying with numpy took {:.2f}ms'.format((t1 - t0) * 1000))

        # table.iterrows() returns an iterator that iterates over all rows.
        # This allow us to avoid loading the entire table in memory.
        t0 = time.time()
        results = [x['bool_field'] for x in table.iterrows()
                   if -100 < x['int_field'] < 100 and x['float_field'] > 0.5]
        t1 = time.time()
        print('Querying with table.iterrows took {:.2f}ms'
              .format((t1 - t0) * 1000))

        t0 = time.time()
        results = [x['bool_field'] for x in table.where(
            """((-100 < int_field) & (int_field < 100)) & (float_field > 0.5)""")]
        t1 = time.time()
        print('Querying with table.where took {:.2f}ms'
              .format((t1 - t0) * 1000))

        t0 = time.time()
        results = [x['bool_field'] for x in table.read_where(
            """((-100 < int_field) & (int_field < 100)) & (float_field > 0.5)""")]
        t1 = time.time()
        print('Querying with table.read_where took {:.2f}ms'
              .format((t1 - t0) * 1000))

        # this won't work: you can't use Python's standard boolean operators in
        # NumExpr expressions
        condition = """(-100 < int_field < 100) & (float_field > 0.5)"""

        # this one works
        condition = """((-100 < int_field) & (int_field < 100)) & (float_field > 0.5)"""
        # we can make it more readable
        cond0 = '((-100 < int_field) & (int_field < 100))'
        cond1 = '(float_field > 0.5)'
        condition = '{} & {}'.format(cond0, cond1)
        results = [x['bool_field'] for x in table.read_where(condition)]
        print('Rows that match the condition: {}'.format(len(results)))


if __name__ == '__main__':
    main()
