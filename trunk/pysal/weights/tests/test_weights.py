import unittest
import pysal
import numpy as np

NPTA3E = np.testing.assert_array_almost_equal

class TestW(unittest.TestCase):
    def setUp(self):
        from pysal import rook_from_shapefile
        self.w = rook_from_shapefile("../../examples/10740.shp")

        self.neighbors={0: [3, 1], 1: [0, 4, 2], 2: [1, 5], 3: [0, 6, 4], 4: [1, 3,
            7, 5], 5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}
        self.weights={0: [1, 1], 1: [1, 1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 1,
            1, 1], 5: [1, 1, 1], 6: [1, 1], 7: [1, 1, 1], 8: [1, 1]}

        self.w3x3 = pysal.lat2W(3,3)

    def test_W(self):
        w = pysal.W(self.neighbors, self.weights)
        self.assertEqual(w.pct_nonzero, 0.29629629629629628)


    def test___getitem__(self):
        self.assertEqual(self.w[0], {1: 1.0, 4: 1.0, 101: 1.0, 85: 1.0, 5: 1.0})


    def test___init__(self):
        w = pysal.W(self.neighbors, self.weights)
        self.assertEqual(w.pct_nonzero, 0.29629629629629628)


    def test___iter__(self):
        w = pysal.lat2W(3,3)
        res = {}
        for i,wi in enumerate(w):
            res[i] = wi
        self.assertEqual(res[0], {1: 1.0, 3: 1.0})
        self.assertEqual(res[8], {5: 1.0, 7: 1.0})

    def test_asymmetries(self):
        w = pysal.lat2W(3,3)
        w.transform = 'r'
        result = w.asymmetry()[0:2]
        NPTA3E(result[0], np.array( [1, 3, 0, 2, 4, 1,
            5, 0, 4, 6, 1, 3, 5, 7, 2, 4, 8, 3, 7, 4, 6, 8, 5, 7]))

    def test_asymmetry(self):
        w = pysal.lat2W(3,3)
        self.assertEqual(w.asymmetry(), [])
        w.transform = 'r'
        self.assertFalse(w.asymmetry() == [])

    def test_cardinalities(self):
        w = pysal.lat2W(3,3)
        self.assertEqual(w.cardinalities, {0: 2, 1: 3, 2: 2, 3: 3, 4: 4, 5: 3,
            6: 2, 7: 3, 8: 2})

    def test_diagW2(self):
        NPTA3E(self.w3x3.diagW2, np.array([ 2.,  3.,  2.,  3.,  4.,  3.,  2.,
            3.,  2.]))
    def test_diagWtW(self):
        NPTA3E(self.w3x3.diagW2, np.array([ 2.,  3.,  2.,  3.,  4.,  3.,  2.,
            3.,  2.]))

    def test_diagWtW_WW(self):
        NPTA3E(self.w3x3.diagWtW_WW, np.array([ 4.,  6.,  4.,  6.,  8.,
            6.,  4.,  6.,  4.]))

    def test_full(self):
        wf = np.array([[ 0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 1.,  0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.],
               [ 0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
               [ 1.,  0.,  0.,  0.,  1.,  0.,  1.,  0.,  0.],
               [ 0.,  1.,  0.,  1.,  0.,  1.,  0.,  1.,  0.],
               [ 0.,  0.,  1.,  0.,  1.,  0.,  0.,  0.,  1.],
               [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  0.,  1.,  0.,  1.],
               [ 0.,  0.,  0.,  0.,  0.,  1.,  0.,  1.,  0.]])
        ids = range(9)

        wf1, ids1 = self.w3x3.full()
        NPTA3E(wf1, wf)
        self.assertEqual(ids1, ids)
        

    def test_get_transform(self):
        self.assertEqual(self.w3x3.transform, 'O')
        self.w3x3.transform = 'r'
        self.assertEqual(self.w3x3.transform, 'R')
        self.w3x3.transform = 'b'

    def test_higher_order(self):
        weights = {0: [1.0, 1.0, 1.0], 1: [1.0, 1.0, 1.0], 2: [1.0, 1.0, 1.0], 3: [1.0, 1.0,
            1.0], 4: [1.0, 1.0, 1.0, 1.0], 5: [1.0, 1.0, 1.0], 6: [1.0, 1.0, 1.0], 7:
            [1.0, 1.0, 1.0], 8: [1.0, 1.0, 1.0]}
        neighbors = {0: [2, 4, 6], 1: [3, 5, 7], 2: [0, 4, 8], 3: [1, 5, 7],
                4: [0, 2, 6, 8], 5: [1, 3, 7], 6: [0, 4, 8], 7: [1, 3, 5], 8:
                [2, 4, 6]}
        w2 = self.w3x3.higher_order(2) 
        self.assertEqual(w2.neighbors, neighbors)
        self.assertEqual(w2.weights, weights)

    def test_histogram(self):
        hist = [(0, 1), (1, 1), (2, 4), (3, 20), (4, 57), (5, 44), (6, 36),
                (7, 15), (8, 7), (9, 1), (10, 6), (11, 0), (12, 2), (13, 0),
                (14, 0), (15, 1)]
        self.assertEqual(self.w.histogram, hist)

    def test_id2i(self):
        id2i = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}
        self.assertEqual(self.w3x3.id2i, id2i)

    def test_id_order_set(self):
        w = pysal.W(neighbors = {'a':['b'], 'b':['a', 'c'], 'c':['b']})
        self.assertFalse(w.id_order_set)


    def test_islands(self):
        w = pysal.W(neighbors = {'a':['b'], 'b':['a', 'c'], 'c':['b'], 'd':[]})
        self.assertEqual(w.islands, ['d'])
        self.assertEqual(self.w3x3.islands, [])

    def test_max_neighbors(self):
        w = pysal.W(neighbors = {'a':['b'], 'b':['a', 'c'], 'c':['b'], 'd':[]})
        self.assertEqual(w.max_neighbors, 2)
        self.assertEqual(self.w3x3.max_neighbors, 4)

    def test_mean_neighbors(self):
        w = pysal.lat2W()
        self.assertEqual(w.mean_neighbors, 3.2)

    def test_min_neighbors(self):
        w = pysal.lat2W()
        self.assertEqual(w.min_neighbors, 2)

    def test_n(self):
        w = pysal.lat2W()
        self.assertEqual(w.n, 25)

    def test_neighbor_offsets(self):
        d = {0: [3, 1],
              1: [0, 4, 2],
              2: [1, 5],
              3: [0, 6, 4],
              4: [1, 3, 7, 5],
              5: [2, 4, 8],
              6: [3, 7],
              7: [4, 6, 8],
              8: [5, 7]}

        self.assertEqual(self.w3x3.neighbor_offsets, d)

    """
    def test_nonzero(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.nonzero())
        assert False # TODO: implement your test here

    def test_order(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.order(kmax))
        assert False # TODO: implement your test here

    def test_pct_nonzero(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.pct_nonzero())
        assert False # TODO: implement your test here

    def test_s0(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.s0())
        assert False # TODO: implement your test here

    def test_s1(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.s1())
        assert False # TODO: implement your test here

    def test_s2(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.s2())
        assert False # TODO: implement your test here

    def test_s2array(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.s2array())
        assert False # TODO: implement your test here

    def test_sd(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.sd())
        assert False # TODO: implement your test here

    def test_set_transform(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.set_transform(value))
        assert False # TODO: implement your test here

    def test_shimbel(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.shimbel())
        assert False # TODO: implement your test here

    def test_sparse(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.sparse())
        assert False # TODO: implement your test here

    def test_trcW2(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.trcW2())
        assert False # TODO: implement your test here

    def test_trcWtW(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.trcWtW())
        assert False # TODO: implement your test here

    def test_trcWtW_WW(self):
        # w = W(neighbors, weights, id_order)
        # self.assertEqual(expected, w.trcWtW_WW())
        assert False # TODO: implement your test here
    """

if __name__ == '__main__':
    unittest.main()
