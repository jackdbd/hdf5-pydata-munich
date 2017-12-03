import os
import time
import tables as tb
import numpy as np


class Patient(tb.IsDescription):
    identifier = tb.UInt16Col(pos=0)
    age = tb.UInt8Col(pos=1)
    heart_rate = tb.UInt8Col(pos=2)
    diastolic_pressure = tb.Float32Col(pos=3)
    systolic_pressure = tb.Float32Col(pos=4)
    hematocrit = tb.UInt8Col(pos=5)
    blood_sugar = tb.Float32Col(pos=6)

    class XRay(tb.IsDescription):
        # 2-D float array (single-precision)
        data = tb.Float32Col(shape=(256, 256))  # 512x512 is too big!


def fill_table(table, num_records):
    table.attrs.heart_rate = 'Beats per minute'
    table.attrs.dyastolic_pressure = 'mmHg'
    table.attrs.systolic_pressure = 'mmHg'
    table.attrs.hematocrit = 'volume percentage'
    table.attrs.blood_sugar = 'mg/dl'

    # reuse the same data to save time
    x_ray = np.random.normal(loc=0, scale=1, size=(256, 256)).astype('float32')
    age = np.random.randint(0, 100, dtype='uint8')
    heart_rate = np.random.randint(40, 200, dtype='uint8')
    diastolic_pressure = np.random.uniform(low=60, high=140)
    systolic_pressure = np.random.uniform(low=80, high=200)
    hematocrit = np.random.randint(low=30, high=60)
    blood_sugar = np.random.uniform(low=50, high=150)

    # Get the record object associated with the table:
    row = table.row
    for i in range(num_records):
        row['identifier'] = i
        row['age'] = age
        row['heart_rate'] = heart_rate
        row['diastolic_pressure'] = diastolic_pressure
        row['systolic_pressure'] = systolic_pressure
        row['hematocrit'] = hematocrit
        row['blood_sugar'] = blood_sugar
        row['XRay/data'] = x_ray
        # inject the Record values into the table
        row.append()
    # Flush the table buffers
    table.flush()


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'pytables-clinical-study.h5')
    filters = tb.Filters(complevel=5, complib='zlib')

    t0 = time.time()
    with tb.open_file(file_path, 'w') as f:
        num_days = 15

        # this should produce a bit more than 1GB of data at each iteration
        for i in range(num_days):
            group_name = 'Day_{0:03}'.format(i)
            group = f.create_group('/', group_name)

            # define the tables for the study/control group of patients
            table_study = f.create_table(
                where=group, name='study', description=Patient,
                title='Study Group of patients', filters=filters)
            table_control = f.create_table(
                where=group, name='control', description=Patient,
                title='Control group of patients', filters=filters)

            # each day we might have a different number of patients
            num_patients_study = np.random.randint(low=2000, high=2200)
            num_patients_control = np.random.randint(low=2100, high=2300)

            # finally, fill up the tables
            fill_table(table_study, num_patients_study)
            fill_table(table_control, num_patients_control)

    t1 = time.time()
    print('Creating the HDF5 file took {:.2f}s'.format(t1 - t0))


if __name__ == '__main__':
    main()
