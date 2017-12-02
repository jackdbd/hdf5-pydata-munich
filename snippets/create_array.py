import os
import numpy as np
import tables as tb


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-array.h5')

    # An Array contains homogeneous data. Every atomic object (i.e. every
    # single element) has the same type and shape.
    atom = tb.Float32Atom()
    # we need to fill all the data in one go. The data must be consistent with
    # the atomic element.
    data = np.random.random((200, 300)).astype('float32')

    with tb.open_file(file_path, 'w') as f:
        f.create_array(
            where='/', name='Array0', obj=data, atom=atom, title='My Array')


if __name__ == '__main__':
    main()
