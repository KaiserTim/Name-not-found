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
        output_path = path[:-5] + '_hdf5fromjson.hdf5'
        f = h5py.File(output_path, "w")
        mask = f.create_dataset("maskdataset", (size,size))
        with open(path) as json_file:
            polygon_dict = json.load(json_file)
        for i in range(size//step_size):
            for j in range(len(polygon_dict)):
                polygon = Polygon(polygon_dict[j]['polygon'])
                sub_polygon = shapely.affinity.translate(polygon, xoff=-step_size*i)
                sub_grid = rasterio.features.rasterize([(sub_polygon,1)], out_shape = (size,step_size))
                mask[:,step_size*i:step_size*(i+1)] = sub_grid

    def hdf5_to_json(self, file):
       pass


if __name__ == '__main__':
    bowtie = ObjectMask('/home/steven/PycharmProjects/Name-not-found/data/json/bowtie.json')
    bowtie.json_to_hdf5(10, 10)
