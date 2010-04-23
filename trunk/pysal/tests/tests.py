"""
Package-wide tests for PySAL

Currently allows for testing of docstring examples from individual modules.
Prior to commiting any changes to the trunk, said changes should be checked
against the rest of the local copy of the trunk by running::

    python tests.py

If all tests pass, changes have not broken the current trunk and can be
committed. Commits that introduce breakage should only be done in cases where
other developers are notified and the breakage raises important issues for
discussion.


Notes
-----
New modules need to be included in the `#module imports` section below, as
well as in the truncated module list where `mods` is first defined.

To deal with relative paths in the doctests a symlink must first be made from
within the `tests` directory as follows::

     ln -s ../examples .

"""

__author__ = "Sergio J. Rey <srey@asu.edu>"

import unittest
import doctest

# module imports
import pysal.esda.moran, pysal.esda.geary, pysal.esda.join_counts
import pysal.esda.mapclassify
import pysal.inequality.theil
import pysal.econometrics.classic
import pysal.region.maxp
import pysal.region.randomregion
import pysal.mobility.rank
import pysal.weights.spatial_lag, pysal.weights.util
import pysal.weights.Contiguity, pysal.weights.Distance, pysal.weights.user
import pysal.weights.Wsets
import pysal.esda.smoothing

#add modules to include in tests
mods='esda.moran','esda.geary', 'esda.mapclassify', \
        'esda.join_counts', \
        'econometrics.classic', \
        'inequality.theil','mobility.rank', \
        'region.maxp', 'region.randomregion', \
        'weights', \
        'weights.spatial_lag', 'weights.util', \
        'weights.Contiguity', 'weights.Distance', 'weights.user', \
        'weights.Wsets', 'esda.smoothing'

mods = [ "pysal."+ mod for mod in mods]
suite = unittest.TestSuite()
for mod in mods:
    suite.addTest(doctest.DocTestSuite(mod))

# Test imports
try:
    import rtree
    import test_cont_weights
    suite.addTest(test_cont_weights.suite)
except ImportError:
    print "Cannot test rtree contiguity weights, rtree not installed"
import test_fileIO
suite.addTest(test_fileIO.suite)
import test_cg_shapes
suite.addTest(test_cg_shapes.suite)
import test_smoothing
suite.addTest(test_smoothing.suite)
import test_dist_weights
suite.addTest(test_dist_weights.suite)
import test_weights
suite.addTest(test_weights.suite)

runner = unittest.TextTestRunner()
runner.run(suite)
