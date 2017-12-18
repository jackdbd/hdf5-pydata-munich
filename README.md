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

### Instructions to build the HDF5 file used in the notebook

1. Visit the [NYC Taxi & Limousine Commission website](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml) and download the CSV files from the 2015 **Yellow** taxi dataset (TLC Trip Record Data). You can also download just one month (e.g. [January](https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2015-01.csv)) to try these snippets out.

2. Place the csv files here: `hdf5-pydata-munich/data/nyctaxi/2015/<your-file-here>.csv`

3. Create the HDF5 file which contains all the tables (1 table per month) with:

```shell
cd snippets
python create_taxi_table.py
```

This creates the HDF5 file `NYC-yellow-taxis-10k.h5`.

4. store a sample of each CSV file in the tables with:

```shell
python append_to_taxi_table.py
```

This reads a chunk of 10000 rows from all the CSV files that you downloaded, then stores the results in the HDF5 file `NYC-yellow-taxis-10k.h5`. This is just a small sample of the original dataset. If you want to store the entire dataset (~12 million rows per month), just remove the `break` statement in `append_to_taxi_table.py`.

To view the structure of the tables you can use a HDF5 viewer like [HDFView](https://support.hdfgroup.org/products/java/hdfview/), [HDF Compass](https://support.hdfgroup.org/projects/compass/) or [ViTables](http://vitables.org/).


### Create a huge HDF5 file

If you want to play around with a huge HDF5 file, I created a snippet that generates some synthetic data. You can run it with:

```shell
python create_huge_hdf5_file.py
```

This takes roughly 5 minutes to run and creates the HDF5 file `pytables-clinical-study.h5` which should be around 5GB in size. You can tweak the code just a little bit to create even bigger files.
