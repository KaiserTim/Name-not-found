import h5py


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
        import json
        from shapely.geometry import Polygon
        with open(self.path) as json_file:
            polygon_dict = json.load(json_file)
        polygon = Polygon(polygon_dict[0]['polygon'])
        self.quadtree = polygon

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

if __name__ == '__main__':
    a = ObjectMask('data/json/bowtie.json')
    a.read()
    print(a.quadtree)