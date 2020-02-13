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
       self.json_to_hdf5()
       self.path = path[:-5] + '_hdf5fromjson.hdf5'
       self.__read_hdf5()
    def extract(self, obj):
        pass

    def output_json(self, obj):
        pass

    def output_hdf5(self, obj):
        pass

    def json_to_hdf5(self, size=None, step_size=100):
        path = self.path
        output_path = path[:-5] + '_hdf5fromjson.hdf5'

        with open(path) as json_file:
            polygon_dict = json.load(json_file)
        if size == None:
            lyst = [polygon_dict[i]['polygon'] for i in range(len(polygon_dict))]
            size = int(np.max(np.array(np.max(lyst))[:, 0])*1.2)
        if step_size > size:
            step_size = size
        f = h5py.File(output_path, "w")
        mask = f.create_dataset("maskdataset", (size, size))
        for j in range(len(polygon_dict)):
            polygon = Polygon(polygon_dict[j]['polygon'])
            for i in range(size//step_size):
                sub_polygon = shapely.affinity.translate(polygon, xoff=-step_size*i)
                sub_grid = rasterio.features.rasterize([(sub_polygon,1)], out_shape = (size,step_size))
                mask[:,step_size*i:step_size*(i+1)] = sub_grid
                print(i)

        f.close()
    def hdf5_to_json(self, file):
       pass


if __name__ == '__main__':
    bowtie = ObjectMask('/home/steven/PycharmProjects/Name-not-found/data/json/B01_0361_annotations.json')
    bowtie.json_to_hdf5(step_size=100)
