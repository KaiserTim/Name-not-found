import h5py
import numpy as np


class ObjectMask:

    root = None
    obj_cluster = {}

    def __init__(self, path):
        self.path = path
        format = path.split(".")[-1]
        assert format in {"json", "hdf5"}, "Wrong datatype."
        self.format = format

    def read(self):
        if self.format == "json":
            self.__read_json()
        else:
            self.__read_hdf5()

    def __read_json(self):
        # Construct the QuadTree here
        pass

    def __read_hdf5(self):
        with h5py.File(self.path, 'r') as f:
            dset = f["data"]
            n, m = dset.shape
            grid_size = 1000
            trees = []
            for i in range((n + grid_size - 1) // grid_size):
                tmp = []
                for j in range((m + grid_size - 1) // grid_size):
                    tmp.append(self.__create_tree(dset[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size],
                                                  (i * grid_size, j * grid_size)))
                trees.append(tmp)

            # TODO: merge trees

    def __create_tree(self, data, hinge=(0,0), depth=20):

        left, top = hinge
        right = left + data.shape[0]
        bottom = top + data.shape[1]
        node = QuadNode(left, right, top, bottom)

        if np.all(data == data[0, 0]):
            node.value = data[0, 0]
            self.obj_cluster[node.value] = (left, right, top, bottom)
            return node

        if depth == 0:
            self.obj_cluster['chunks'] = (left, right, top, bottom)
            return node

        N, M = data.shape
        node.NW = self.__create_tree(data[:N // 2, :M // 2], (0, 0), depth-1)
        node.NE = self.__create_tree(data[:N // 2, M // 2:], (0, M // 2), depth-1)
        node.SW = self.__create_tree(data[N // 2:, :M // 2], (N // 2, 0), depth-1)
        node.SE = self.__create_tree(data[N // 2:, M // 2:], (N // 2, M // 2), depth-1)

        return node


    def check(self, obj_nr, points, reduced=False):

        """docstring"""

        if self.quad_root is None:
            self.read()

        inside = []*len(points)
        for i, point in enumerate(points):
            inside[i] = self.__point_in_obj(point, obj_nr)

        if reduced:
            return points[inside]
        return inside

    def __point_in_obj(self, point, obj_nr):

        """docstring"""

        inside = False
        x, y = point
        for cluster_coords in self.obj_cluster[obj_nr]:
            left, right, top, bottom = cluster_coords
            if left <= x <= right and top <= y <= bottom:
                inside = True
                break

        return inside

    # def rundown(self, node, point):
    #     """Find the value for a given point"""
    #     if node.lr == None:
    #         return node.value, (node.tr, node.br, node.tl, node.bl)
    #     else:
    #         x_mean = (node.bl + node.br) // 2
    #         y_mean = (node.tl + node.tr) // 2
    #         if point <= x_mean:
    #             if point <= y_mean:
    #                 return rundown(node.nw, point)
    #             else:
    #                 return rundown(node.SW, point)
    #         else:
    #             if point <= y_mean:
    #                 return rundown(node.ne, point)
    #             else:
    #                 return rundown(node.se, point)

    def extract(self, obj_nr, path):
        """docstring"""
        with h5py.File(path, "r") as f:
            gray_img = f[""] # was muss hier rein

        array = np.array([])
        for cluster_coords in self.obj_cluster[obj_nr]:
            left, right, top, bottom = cluster_coords
            gray_cluster = gray_img[left:right, top:bottom]
            array = np.append(array, gray_cluster.flatten())

        for cluster_coords in self.obj_cluster['chunks']:
            left, right, top, bottom = cluster_coords
            cluster = self.data[left:right, top:bottom] # Self.data muss in "read" erstellt werden
            mask = cluster == obj_nr
            gray_cluster = gray_img[mask]
            array = np.append(array, gray_cluster)
        unique, counts = np.unique(array, return_counts=True)
        return dict(zip(unique, counts))

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

    def __init__(self, left, right, top, bottom, NE=None, SE=None, SW=None, NW=None, value=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.NE = NE
        self.SE = SE
        self.SW = SW
        self.NW = NW

        self.value = value
