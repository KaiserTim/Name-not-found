import QuadTree

if __name__ == '__main__':
    path = "./data/hdf5image/B01_0361_annotations_si_spacing1.hdf5"
    quadtree = ObjectMask(path=path, obj_count=1)
    quadtree.read()
    points = [(5,2)]
    quadtree.check(obj_nr=1, points=points)
