import numpy as np

import QuadTree
import time

if __name__ == '__main__':
    start_time = time.time()
    print("Start")
    path = "data/hdf5_image/B01_0361_annotations_si_spacing1.hdf5"
    quadtree = QuadTree.ObjectMask(path=path)
    quadtree.read()
    print("Tree constructed", time.time() - start_time)
    n, m = 10, 10
    x_offset = 1000
    y_offset = 1000
    a = []
    for i in range(x_offset, x_offset + m):
        for j in range(y_offset, y_offset + n):
            a.append(i)
    b = list(range(x_offset, x_offset + n))*m
    #points = list(zip(b,a))
    points = np.load("B01_0361_annotations_si_spacing1.npz", allow_pickle=True)["arr_0"]
    print(points[:10])


    print(quadtree.check(obj_nr=1, points=points))
    print("Points checked", time.time()-start_time)

