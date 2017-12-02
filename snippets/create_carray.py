import os
import numpy as np
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-carray.h5')

    # A CArray is not enlargeable: we define its shape here and we cannot
    # enlarge the array later.
    shape = (200, 300)
    # A Carray contains homogeneous data. Every atomic object (i.e. every
    # single element) has the same type and shape.
    atom = tb.Float32Atom()
    # A Carray supports compression
    filters = tb.Filters(complevel=5, complib='zlib')

    with tb.open_file(file_path, 'w') as f:
        # create an empty CArray
        carray = f.create_carray(where='/', name='Array0', atom=atom,
                                 shape=shape, title='My CArray',
                                 filters=filters)
        # define some data
        n_rows = 50
        n_cols = 20
        data = np.ones((n_rows, n_cols))

        # fill a hyperslab (i.e. a region in the array) with the data
        i_row = 10
        i_col = 5
        carray[i_row:i_row+n_rows, i_col:i_col+n_cols] = data

        # define some other data
        n_rows = 100
        n_cols = 100
        data = 100 * np.random.random((n_rows, n_cols))

        # fill another hyperslab
        i_row = 50
        i_col = 120
        carray[i_row:i_row + n_rows, i_col:i_col + n_cols] = data

    # Tip: open the file in HDF View and view it as an image


if __name__ == '__main__':
    main()
