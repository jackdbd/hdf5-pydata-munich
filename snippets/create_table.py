import os
import tables as tb


class Particle(tb.IsDescription):
    # character String
    identity = tb.StringCol(itemsize=22, dflt=' ', pos=0)
    # short integer
    idnumber = tb.Int16Col(dflt=1, pos=1)
    # single-precision
    speed = tb.Float32Col(dflt=1, pos=2)


def fill_table(table, num_records):
    # Get the record object associated with the table:
    row = table.row
    for i in range(num_records):
        row['identity'] = 'This is particle: {}'.format(i)
        row['idnumber'] = i
        row['speed'] = i * 2.0
        # inject the Record values into the table
        row.append()
    # Flush the table buffers
    table.flush()


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-tables.h5')

    with tb.open_file(file_path, 'w') as f:
        group0 = f.create_group(where=f.root, name='group0')
        group1 = f.create_group(where='/', name='group1')
        table0 = f.create_table(group0, 'table0', description=Particle)
        table1 = f.create_table('/group1', 'table1', description=Particle)

        for table in (table0, table1):
            fill_table(table, 10)


if __name__ == '__main__':
    main()
