import os
import numpy as np
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-earray.h5')

    # One (and only one) of the shape dimensions *must* be 0. The dimension
    # being 0 means that the resulting EArray object can be extended along it.
    # Multiple enlargeable dimensions are not supported right now.
    shape = (0, 300)

    # An EArray contains homogeneous data. Every atomic object (i.e. every
    # single element) has the same type and shape.
    atom = tb.Float32Atom()
    # An EArray supports compression
    filters = tb.Filters(complevel=5, complib='zlib')

    with tb.open_file(file_path, 'w') as f:
        # create an empty EArray
        earray = f.create_earray(where='/', name='Array0', atom=atom,
                                 shape=shape, title='My EArray',
                                 filters=filters)

        # number of times that we need to write some data
        num = 100
        for i in range(num):
            rows = np.random.randint(low=10, high=100)
            cols = shape[1]
            # define some data
            sequence = np.random.random((rows, cols)).astype('float32')
            # append the data to the EArray
            earray.append(sequence=sequence)


if __name__ == '__main__':
    main()
