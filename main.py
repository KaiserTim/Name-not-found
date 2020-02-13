import numpy as np
import QuadTree
import time


def cluster_indices(hinge, width, height):
    """
    Create a list of indices of a rectangle
    Inputs: The top-left corner of the rectangle, its width, its height
    Output: List of tuples containing the indices
    """

    x, y = hinge
    a, b = np.indices((width, height))
    return list(zip(x + a.flatten(), y + b.flatten()))


if __name__ == '__main__':
    start_time = time.time()
    print("Start")
    path = "data/hdf5_image/B01_0361_annotations_si_spacing1.hdf5"
    quadtree = QuadTree.ObjectMask(path=path)
    quadtree.read()
    print("Tree constructed after", time.time() - start_time, "s")
    # Generate a rectangle of indices
    hinge = (5449, 32290)
    # hinge = (58699, 26790)
    width, height = 1, 1
    points = cluster_indices(hinge=hinge, width=width, height=height)
    # points = np.load("points/B01_0361_annotations_si_spacing1.npz", allow_pickle=True)["arr_0"]
    # print(points)
    check_result = quadtree.check(obj_nr=1, points=points, mp=False)
    print(np.any(check_result))
    print("Points checked after", time.time()-start_time, "s")


