import h5py

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
            a_group_key = list(f.keys())[0]
            data = list(f[a_group_key])
        # Construct the QuadTree here
        pass

    def check(self, obj, points):
        """docstring"""
        if quadtree == None:
            read(self.path)
        value_hist = {}

        cluster_value, cluster_corners = rundown(quad_root, point)
        # for points in cluster:
        #   fill value_hist with entries
        # check for duplicates in the list of points

    def rundown(self, node, point):
        """Find the value for a given point"""
        if node.lr == None:
            return node.value, (node.tr, node.br, node.tl, node.bl)
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

class Quad_node:
    """
    coordinates: topright, bottomright, bottomleft, topleft
    children: northeast, southeast, southwest, northwest
    value: cluster-value
    """
    tr = None
    br = None
    bl = None
    tl = None

    ne = None
    se = None
    sw = None
    nw = None

    value = None

    def __init__(self, tr, br, bl, tl, ne=None, se=None, sw=None, nw=None, value=None):
        self.tr = tr
        self.br = br
        self.bl = bl
        self.tl = tl

        self.ne = ne
        self.se = se
        self.sw = sw
        self.nw = nw

        self.value = value
