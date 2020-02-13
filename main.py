import numpy as np

import QuadTree

if __name__ == '__main__':
    path = "./data/hdf5_image/B01_0361_annotations_si_spacing1.hdf5"
    quadtree = QuadTree.ObjectMask(path=path)
    quadtree.read()
    points = np.load("B01_0361_annotations_si_spacing1.npz", allow_pickle=True)["arr_0"]
    print(quadtree.check(obj_nr=1, points=points))
