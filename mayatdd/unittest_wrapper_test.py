import unittest

from mayatdd.mayatest import mayaTest


@mayaTest('mayatdd')
class RunMeInMaya(unittest.TestCase):
    def testSomething(self):
        pass