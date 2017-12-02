import os
import h5py


def print_name(name):
    print(name)


def print_name_and_type(name, obj):
    msg = '{} is a {}'.format(name, obj.__class__.__name__)
    print(msg)


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.abspath(os.path.join(here, '..', 'data'))
    file_path = os.path.join(data_dir, 'h5py-groups-datasets-attributes.h5')

    with h5py.File(file_path, 'r') as f:
        # the callable to supply to visit has <member name>
        f.visit(print_name)
        # the callable to supply to visititems has <member name>, <object>
        f.visititems(print_name_and_type)


if __name__ == '__main__':
    main()
