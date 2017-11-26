"""Create indexes in a table.

Run the snippet 'open_big_hdf5.py' first, and take note of the timings.
The run this snippet, which creates indexes for the columns used when querying
the data in 'open_big_hdf5.py'.
Run the snippet 'open_big_hdf5.py' once again. Querying with numpy or .iterrows
should take the same amount of time. Querying with .where or .read_where should
be faster.
"""
import os
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'big_file.h5')

    # open file in append mode
    with tb.open_file(file_path, 'a') as hdf:
        table = hdf.root.Day_001.control

        # Create indexes
        blosc_filter = tb.Filters(complevel=9, complib='blosc')
        table.cols.heart_rate.create_csindex(filters=blosc_filter)
        table.cols.hematocrit.create_csindex(filters=blosc_filter)

if __name__ == '__main__':
    main()
