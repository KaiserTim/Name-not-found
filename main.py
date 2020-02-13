import QuadTree

if __name__ == '__main__':
    path = "/home/steven/PycharmProjects/Name-not-found/data/json/B01_0361_annotations_si.json"
    quadtree = QuadTree.ObjectMask(path=path)
    quadtree.read()
    points = [(5,2)]
    print(quadtree.check(obj_nr=1, points=points))
