import json
import h5py
import numpy as np
from shapely.geometry import Polygon
import rasterio.features
import shapely.affinity


class ObjectMask:
    root = None
    data = None
    obj_cluster = {'chunks': []}

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


        self.json_to_hdf5()
        self.path = self.path[:-5] + '_hdf5fromjson.hdf5'
        self.__read_hdf5()

    def __read_hdf5(self):
        f = h5py.File(self.path, 'r')
        self.data = f["data"]
        n, m = self.data.shape
        grid = [(0, 0)] + self.__make_grid(n, m) + [(n, m)]
        trees = []
        for i in range(len(grid) - 1):
            tmp = []
            for j in range(len(grid) - 1):
                tmp.append(self.__create_tree(self.data[grid[i][0]:grid[i + 1][0], grid[j][1]:grid[j + 1][1]], (grid[i][0], grid[j][1])))
            trees.append(tmp)
        self.root = self.__merge_trees(np.array(trees))

    def __make_grid(self, n, m, hinge=(0, 0), max_size=1000):
        hn, hm = hinge

        if n <= max_size and m <= max_size:
            return []

        return self.__make_grid(n // 2, m // 2, (hn, hm)) + \
               [(hn + n // 2, hm + m // 2)] + \
               self.__make_grid(n // 2, m // 2, (hn + n // 2, hm + m // 2))

    def __create_tree(self, data, hinge, depth=5):
        left, top = hinge
        right = left + data.shape[0] - 1
        bottom = top + data.shape[1] - 1
        node = QuadNode(left, right, top, bottom)

        n, m = data.shape
        if n <= 2 or m <= 2:
            self.obj_cluster['chunks'].append(((left, right, top, bottom), data[left:right+1, top:bottom+1]))
            return node

        if np.all(data == data[0, 0]):
            node.value = data[0, 0]
            if node.value in self.obj_cluster.keys():
                self.obj_cluster[node.value].append((left, right, top, bottom))
            else:
                self.obj_cluster[node.value] = [(left, right, top, bottom)]
            return node

        if depth == 0:
            self.obj_cluster['chunks'].append(((left, right, top, bottom), data[left:right+1, top:bottom+1]))
            return node

        node.NW = self.__create_tree(data[:n // 2, :m // 2], (left, top), depth - 1)
        node.NE = self.__create_tree(data[:n // 2, m // 2:], (left, top + m // 2), depth - 1)
        node.SW = self.__create_tree(data[n // 2:, :m // 2], (left + n // 2, top), depth - 1)
        node.SE = self.__create_tree(data[n // 2:, m // 2:], (left + n // 2, top + m // 2), depth - 1)

        return node

    def __merge_trees(self, trees):
        left = trees[0, 0].left
        top = trees[0, 0].top
        right = trees[-1, -1].right
        bottom = trees[-1, -1].bottom
        node = QuadNode(left, right, top, bottom)

        if trees.shape == (4, 4):
            node.NW = trees[0, 0]
            node.NE = trees[0, 1]
            node.SW = trees[1, 0]
            node.SE = trees[1, 1]

            return node

        n, m = trees.shape
        node.NW = self.__merge_trees(trees[:n // 2, :m // 2])
        node.NE = self.__merge_trees(trees[:n // 2, m // 2:])
        node.SW = self.__merge_trees(trees[n // 2:, :m // 2])
        node.SE = self.__merge_trees(trees[n // 2:, m // 2:])

        return node

    def check(self, obj_nr, points, reduced=False):
        """
        Check if a list of points is in a given object individually
        Inputs: Number of object, list of points to check, output-parameter
        Output: If reduced=False: Boolean list of answers
                If reduced=True: List with the points which are inside of the object
        """

        if self.root is None:
            self.read()

        inside = [None] * len(points)
        for i, point in enumerate(points):
            value = self.__rundown(self.root, point)
            inside[i] = value == obj_nr

        if reduced:
            return points[inside]
        return inside

    def __rundown(self, node, point):
        """
        Find the value for a given point (fast version of point_in_object)
        Inputs: Current node to propagate, point to check
        Output:
        """
        left, right, top, bottom = node.left, node.right, node.top, node.bottom
        x, y = point
        if node.NW is None:
            if node.value is None:
                return chunk[x-left, y-top]
            else:
                return node.value
        else:
            x_mean = (left + right) // 2
            y_mean = (top + bottom) // 2
            if x <= x_mean:
                if y <= y_mean:
                    return self.__rundown(node.NW, point)
                else:
                    return self.__rundown(node.SW, point)
            else:
                if y <= y_mean:
                    return self.__rundown(node.NE, point)
                else:
                    return self.__rundown(node.SE, point)

    def __point_in_obj(self, obj_nr, point):
        """
        Check if a single point is inside a given object (very slow!)
        Inputs: Number of object, point to check
        Output: Boolean parameter
        """

        x, y = point
        for cluster_coords in self.obj_cluster[obj_nr]:
            left, right, top, bottom = cluster_coords
            if left <= x <= right and top <= y <= bottom:
                return True

        for chunk_coords, chunk in self.obj_cluster['chunks']:
            left, right, top, bottom = chunk_coords
            if left <= x <= right and top <= y <= bottom:
                if chunk[x-left, y-top] == obj_nr:
                    return True

        return False

    def extract(self, obj_nr, path):
        """
        Extract all values belonging to obj_nr from the grayvalue image
        Inputs: Number of object, path of grayvalue image
        Output: Dictionary containing (key,value) pairs of (grayvalue, count)
        """

        with h5py.File(path, "r") as f:
            gray_img = f["data"]

        array = np.array([])
        for cluster_coords in self.obj_cluster[obj_nr]:
            left, right, top, bottom = cluster_coords
            gray_cluster = gray_img[left:right+1, top:bottom+1]
            array = np.append(array, gray_cluster.flatten())

        for cluster_coords in self.obj_cluster['chunks']:
            left, right, top, bottom = cluster_coords
            cluster = self.data[left:right+1, top:bottom+1]
            mask = cluster == obj_nr
            gray_cluster = gray_img[mask]
            array = np.append(array, gray_cluster)

        unique, counts = np.unique(array, return_counts=True)
        return dict(zip(unique, counts))

    def output_json(self, obj):
        pass

    def output_hdf5(self):
        return self.data

    def json_to_hdf5(self, size=None, step_size=100):
        """
        can be called to create a hdf5 file from a json file
        the resulting pixel map will be of dimension of size*size or will fit all polygons if no size is given
        very inefficient, takes forever
        """
        path = self.path
        output_path = path[:-5] + '_hdf5fromjson.hdf5'

        with open(self.path) as json_file:
            polygon_dict = json.load(json_file)
        if size is None:
            lyst = [polygon_dict[i]['polygon'] for i in range(len(polygon_dict))]
            size = int(np.max(np.array(np.max(lyst)))*1.2)
        if step_size > size:
            step_size = size
        f = h5py.File(output_path, "w")
        mask = f.create_dataset("data", (size, size))
        for j in range(len(polygon_dict)):
            polygon = Polygon(polygon_dict[j]['polygon'])
            for i in range(size//step_size):
                sub_polygon = shapely.affinity.translate(polygon, xoff=-step_size*i)
                sub_grid = rasterio.features.rasterize([(sub_polygon, 1)], out_shape=(size, step_size))
                mask[:, step_size*i:step_size*(i+1)] = sub_grid

        f.close()

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
