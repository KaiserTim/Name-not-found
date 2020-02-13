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
            self.data = f["data"]
            n, m = self.data.shape
            grid = [(0, 0)] + self.__make_grid(n, m) + [(n, m)]
            trees = []
            for i in range(len(grid) - 1):
                tmp = []
                for j in range(len(grid) - 1):
                    tmp.append(self.__create_tree(self.data[grid[i]:grid[i + 1], grid[j]:grid[j + 1]], (grid[i], grid[j])))
                trees.append(tmp)

            # TODO: merge trees

    def __make_grid(self, n, m, hinge=(0, 0), max_size=1000):
        hn, hm = hinge

        if n <= max_size and m <= max_size:
            return []

        return self.__make_grid(n // 2, m // 2, (hn, hm)) + \
               [(hn + n // 2, hm + m // 2)] + \
               self.__make_grid(n // 2, m // 2, (hn + n // 2, hm + m // 2))

    def __create_tree(self, data, hinge, depth=20):

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

        n, m = data.shape
        node.NW = self.__create_tree(data[:n // 2, :m // 2], (left, top), depth - 1)
        node.NE = self.__create_tree(data[:n // 2, m // 2:], (left, top + m // 2), depth - 1)
        node.SW = self.__create_tree(data[n // 2:, :m // 2], (left + n // 2, top), depth - 1)
        node.SE = self.__create_tree(data[n // 2:, m // 2:], (left + n // 2, top + m // 2), depth - 1)

        return node

    def check(self, obj_nr, points, reduced=False):

        """docstring"""

        if self.quad_root is None:
            self.read(self.path)

        inside = [] * len(points)
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
