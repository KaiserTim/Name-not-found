# Data for HHU course "Algorithms & Advanced Programming (2020)"

This repository contains data for HHU course __Algorithms & Advanced Programming (2020).__

## Install

Datalad and git annex can be installed using anaconda by running

```bash
conda install datalad
```

If you already have git-annex installed and want to use pip instead of anaconda, run

```bash
pip install datalad
```

## Getting the data

Clone to dataset to your local machine using

```bash
# datalad clone git@jugit.fz-juelich.de:hhu_course_algorithms_and_advanced_programming/data.git
datalad clone https://jugit.fz-juelich.de/hhu_course_algorithms_and_advanced_programming/data.git
cd data
datalad update --merge
```

To download the data of a folder (e.g. the `json`), use the following commands:

```bash
# Get an individual file
datalad get hdf5_image/B01_0361_annotations_spacing64.json
# Get a complete folder (be careful with this, it may download several gigabytes of data)
datalad get hdf5_image/
```

To drop downloaded data, run

```bash
# Drop a single file
datalad drop hdf5_image/B01_0361_annotations_spacing64.json
# Drop a folder
datalad drop hdf5_image/
# Drop all files
datalad drop .
```

After dropping a file, you can use `datalad get` to get files back to your system (see above).

## Structure

- `json`: JSON files containing polygons.
- `hdf5_polygon`: HDF5 files containing polygons.
- `hdf5_image`: HDF5 files containing image data (masks).
- `tif`: TIFF files containing image data (masks).
- `png`: PNG files containing image data (masks).
- `scripts`: Some scripts to work with the data.

## Useful packages

The following python packages may be helpful to work with the provided data:

- `h5py` for reading and writing of HDF5 files
- `pytiff` for reading and writing of BigTIFF files (required for TIFF files >4GB)
- `shapely` for handling of polygons
- `descartes` for visualizing shapely polygons
- `imageio` to read image files

## Further information

- [datalad homepage](https://www.datalad.org/)
- [datalad handbook](http://handbook.datalad.org/en/latest/)
- [datalad developer documentation](http://docs.datalad.org/en/latest/)
- [git annex](https://git-annex.branchable.com/)
- [git annex standalone binary](https://git-annex.branchable.com/install/Linux_standalone/)
