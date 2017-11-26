import time
import os
import tables as tb
import numpy as np


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'big_file.h5')

    with tb.open_file(file_path, 'r') as hdf:
        table = hdf.root.Day_001.control
        print(table)

        # t0 = time.time()
        # np.where(arr[:] > 0.5)
        # we can also use .read()
        # np.where(arr.read() > 0.5)
        # t1 = time.time()
        # print('np.where took {:.2f}ms'.format((t1 - t0) * 1000))

        # t0 = time.time()
        # tb.where
        # aa = np.where(arr[:] > 0.5)
        # t1 = time.time()
        # print('np.where took {:.2f}ms'.format((t1 - t0) * 1000))


if __name__ == '__main__':
    main()
