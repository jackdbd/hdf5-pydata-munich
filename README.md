# hdf5-pydata-munich

Introduction to HDF5 in Python.

![An image showing a subset of pickup locations of New York City yellow taxis during January 2015](https://github.com/jackdbd/hdf5-pydata-munich/blob/master/img/nyc-yellow-taxis-pickups.png "A subset of pickup locations of New York City yellow taxis during January 2015")

If you are just curious and want to have a look at the notebook without installing anything, go to [http://nbviewer.jupyter.org/](http://nbviewer.jupyter.org/) and type `jackdbd/hdf5-pydata-munich` in the search bar.


### Installation

Create a Python 3.5 virtual environment. It seems that at this moment Bokeh has some issues with Python 3.6.

```shell
pip install -r requirements.txt
```


### Usage

```shell
# start the notebook server
jupyter notebook  --port 8085
# open your browser and go to:
# http://localhost:8085/notebooks/hdf5_in_python.ipynb
```