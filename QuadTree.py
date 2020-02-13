import json
import h5py
import numpy as np
from shapely.geometry import Polygon
import rasterio.features
import shapely.affinity

class ObjectMask:

    quadtree = None

    def __init__(self, path):
        self.path = path
        format = path.split(".")[-1]
        assert format in {"json", "hdf5"}, "Wrong datatype."
        self.format = format

    def read(self):
        if self.format == 'json':
            self.__read_json()
        # if else
        # __read_json bzw. __read_hdf5

    def __read_json(self):
       pass
    def extract(self, obj):
        pass

    def output_json(self, obj):
        pass

    def output_hdf5(self, obj):
        pass

    def json_to_hdf5(self, size, step_size):
        path = self.path
        output_path = path[:-4] + 'hdf5fromjson.hdf5'
        f = h5py.File(output_path, "w")
        mask = f.create_dataset("maskdataset", (size,size))
        with open(path) as json_file:
            polygon_dict = json.load(json_file)
        polygon = Polygon(polygon_dict[0]['polygon'])

        for i in range(size//step_size):
            mask[:,step_size*i:step_size*(i+1)] =

    def hdf5_to_json(self, file):
        pass

if __name__ == '__main__':
   pass