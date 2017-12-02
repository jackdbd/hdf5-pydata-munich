import os
import numpy as np
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-vlarray.h5')

    # A VLArray contains homogeneous data.
    # Like Table datasets, variable length arrays can have only one dimension,
    # and the elements (atoms) of their rows can be fully multidimensional.
    atom = tb.Float32Atom()
    # A VLArray supports compression (although compression is only performed on
    # the data structures used internally by the HDF5)
    # https://support.hdfgroup.org/HDF5/doc/TechNotes/VLTypes.html
    filters = tb.Filters(complevel=5, complib='zlib')

    with tb.open_file(file_path, 'w') as f:
        # Create a VLArray
        vlarray = f.create_vlarray(where=f.root, name='Array0', atom=atom,
                                   title='My VLArray', filters=filters)

        # Append some rows of variable length
        for i in range(200):
            length = np.random.randint(low=1, high=300)
            data = np.ones(length).astype('float32')
            vlarray.append(data)


if __name__ == '__main__':
    main()
