import QuadTree

if __name__ == '__main__':
    path = "./data/hdf5_image/B01_0361_annotations_si_spacing1.hdf5"
    quadtree = QuadTree.ObjectMask(path=path)
    quadtree.read()
    n, m = 100, 100
    x_offset = 1000
    y_offset = 1000
    a = []
    for i in range(x_offset, x_offset + m):
        for j in range(y_offset, y_offset + n):
            a.append(i)
    b = list(range(x_offset, x_offset + n))*m
    points = list(zip(b,a))
    print(points[:10])
    print(quadtree.check(obj_nr=1, points=points))
