from gitcmd import GitCmd
import unittest
import os


class TestHttpsClone(unittest.TestCase):
    testDir = "./__test"

    def setUp(self):
        self.gc = GitCmd(work_dir=self.testDir, url='https://github.com/philoprove/gitcmd')
        self.gc.clone()
        assert os.path.exists(self.testDir)
        assert os.path.exists(self.testDir + '/README.rst')

    def testPull(self):
        self.gc.pull()

    def tearDown(self):
        os.popen("rm -rf " + self.testDir)



class TestSSHClone(unittest.TestCase):
    testDir = "./__test"

    def setUp(self):
        self.gc = GitCmd(work_dir=self.testDir, url='git@github.com:philoprove/gitcmd.git')
        self.gc.clone()
        assert os.path.exists(self.testDir)
        assert os.path.exists(self.testDir + '/README.rst')

    def testPull(self):
        self.gc.pull()

    def tearDown(self):
        os.popen("rm -rf " + self.testDir)

