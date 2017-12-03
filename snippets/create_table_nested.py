import os
import numpy as np
import tables as tb


class Particle(tb.IsDescription):
    # 16-character String
    name = tb.StringCol(16)
    # signed 64-bit integer
    idnumber = tb.Int64Col()
    # unsigned short integer
    ADCcount = tb.UInt16Col()
    # unsigned byte
    TDCcount = tb.UInt8Col()
    # integer
    grid_i = tb.Int32Col()
    # integer
    grid_j = tb.Int32Col()

    # A sub-structure (nested data-type)
    class Properties(tb.IsDescription):
        # 2-D float array (single-precision)
        pressure = tb.Float32Col(shape=(2, 3))
        # 3-D float array (double-precision)
        energy = tb.Float64Col(shape=(2, 3, 4))


def fill_table(table, num_records):
    row = table.row
    for i in range(num_records):
        # First, assign the values to the Particle record
        row['name'] = np.random.choice(['Superman', 'Spider-Man', 'Batman'])
        row['idnumber'] = np.random.randint(0, 100, dtype='int64')
        row['ADCcount'] = i * 2.0
        # TDCcount is an unsigned byte. Negative numbers or numbers greater
        # than 255 (2^8 - 1) will be saved, but you will have invalid data in
        # the table (-10 will appear as 246)
        # row['TDCcount'] = -10
        row['TDCcount'] = np.random.randint(0, 255,
                                            Particle.columns['TDCcount'].dtype)
        row['grid_i'] = np.random.randint(0, 100, dtype='int32')
        row['grid_j'] = np.random.randint(0, 100, dtype='int32')

        # Fill the nested data-type Properties
        row['Properties/pressure'] = np.random.random((2, 3))
        row['Properties/energy'] = np.random.random((2, 3, 4))

        row.append()

    table.flush()


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-tables-nested.h5')
    with tb.open_file(file_path, 'w') as f:
        my_table = f.create_table('/', 'my_table', description=Particle)
        fill_table(my_table, 100)

if __name__ == '__main__':
    main()
