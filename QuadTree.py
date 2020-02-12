import h5py
import numpy as np

class ObjectMask:

    quad_root = None

    def __init__(self, path):
        self.path = path
        format = path.split(".")[-1]
        assert format in {"json", "hdf5"}, "Wrong datatype."
        self.format = format

    def read(self, path):
        # if else
        # __read_json bzw. __read_hdf5
        pass

    def __read_json(self, path):
        # Construct the QuadTree here
        pass

    def __read_hdf5(self, path):
        with h5py.File(path, 'r') as f:
            N, M = f["data"].shape
            trees = []
            grid_size = 1000
            for j in range((M + grid_size - 1) // grid_size):
                tmp = []
                for i in range((N + grid_size - 1) // grid_size):
                    #tmp.append()
                    #f["data"][i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
                    #Construct the QuadTree here
                    pass
                trees.append(tmp)



    def check(self, obj, list):
        pass

    def extract(self, obj):
        pass

    def output_json(self, obj):
        pass

    def output_hdf5(self, obj):
        pass

    def json_to_hdf5(self, file):
        pass

    def hdf5_to_json(self, file):
        pass

class QuadNode:
    """
    coordinates: left, right, top, bottom
    children: northeast, southeast, southwest, northwest
    value: cluster-value
    """

    def __init__(self, left, right, top, bottom, ne=None, se=None, sw=None, nw=None, value=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.ne = ne
        self.se = se
        self.sw = sw
        self.nw = nw

        self.value = value
