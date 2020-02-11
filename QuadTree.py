import h5py

class ObjectMask:

    quadtree = None

    def __init__(self, path):
        self.path = path
        format = path.split(".")[-1]
        assert format in {"json", "hdf5"}, "Wrong datatype."
        self.format = format

    def read(self, path):
        # if else
        # __read_json bzw. __read_hdf5

    def __read_json(self, path):
        # Construct the QuadTree here
        pass

    def __read_hdf5(self, path):
        with h5py.File(path, 'r') as f:
            a_group_key = list(f.keys())[0]
            data = list(f[a_group_key])
        # Construct the QuadTree here
        pass

    def check(self, obj, points):
        if quadtree == None:
            read(self.path)
        # run down the tree
        cluster = rundown(point)
        # retrieve the values

        # check for duplicates in the list of points

    def rundown(self, node, point):
        """Find the value for a given point"""
        if node.lr == None:
            return node.value
        else:
            x_mean = (node.bl + node.br) // 2
            y_mean = (node.tl + node.tr) // 2
            if point <= x_mean:
                if point <= y_mean:
                    return rundown(node.nw, point)
                else:
                    return rundown(node.sw, point)
            else:
                if point <= y_mean:
                    return rundown(node.ne, point)
                else:
                    return rundown(node.se, point)


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
