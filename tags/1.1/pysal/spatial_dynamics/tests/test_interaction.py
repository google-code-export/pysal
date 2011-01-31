import unittest
import pysal
from pysal.spatial_dynamics import interaction 
import numpy as np


class SpaceTimeEvents_Tester(unittest.TestCase):
    def setUp(self):
        self.path = "../../examples/burkitt"
    def test_SpaceTimeEvents(self):
        events = interaction.SpaceTimeEvents(self.path,'T')
        self.assertEquals(events.n, 188)
        self.assertEquals(list(events.space[0]), [ 300.,  302.])
        self.assertEquals(list(events.t[0]), [413])

class Knox_Tester(unittest.TestCase):
    def setUp(self):
        path = "../../examples/burkitt"
        self.events = interaction.SpaceTimeEvents(path,'T')
    def test_knox(self):
        result = interaction.knox(self.events,delta=20,tau=5,permutations=1)
        self.assertEquals(result['stat'], 13.0)

class Mantel_Tester(unittest.TestCase):
    def setUp(self):
        path = "../../examples/burkitt"
        self.events = interaction.SpaceTimeEvents(path,'T')
    def test_mantel(self):
        result = interaction.mantel(self.events,1,scon=0.0,spow=1.0,tcon=0.0,tpow=1.0)
        self.assertAlmostEquals(result['stat'], 0.014154, 6)

class Jacquez_Tester(unittest.TestCase):
    def setUp(self):
        path = "../../examples/burkitt"
        self.events = interaction.SpaceTimeEvents(path,'T')
    def test_jacquez(self):
        result = interaction.jacquez(self.events,k=3,permutations=1)
        self.assertEquals(result['stat'], 13)
        


suite = unittest.TestSuite()
test_classes = [SpaceTimeEvents_Tester, Knox_Tester, Mantel_Tester, Jacquez_Tester]
for i in test_classes:
    a = unittest.TestLoader().loadTestsFromTestCase(i)
    suite.addTest(a)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)

