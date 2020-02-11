import h5py

class ObjectMask:

    quadtree_root = None

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

class Node:
    # coordinates: topright, bottomright, bottomleft, topleft
    tr = None
    br = None
    bl = None
    tl = None

    # children: northeast, southeast, southwest, northwest
    ne = None
    se = None
    sw = None
    nw = None

    # leaf; no children
    def Node(self, tr, br, bl, tl):
        self.tr = tr
        self.br = br
        self.bl = bl
        self.tl = tl

    # non-leaf
    def Node(self, tr, br, bl, tl, ne, se, sw, nw):
        self.tr = tr
        self.br = br
        self.bl = bl
        self.tl = tl

        self.ne = ne
        self.se = se
        self.sw = sw
        self.nw = nw
