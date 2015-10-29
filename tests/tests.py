from gitcmd import GitCmd
import unittest
import os


def only_local(cls):
    if os.environ.get("USER") == 'sphy':
        return cls
    else:
        return None

class TestHttpsClone(unittest.TestCase):
    testDir = "./__testHttpsClone"

    def setUp(self):
        self.gc = GitCmd(work_dir=self.testDir, url='https://github.com/philoprove/gitcmd')
        self.gc.clone()
        assert os.path.exists(self.testDir)
        assert os.path.exists(self.testDir + '/README.rst')

    def testPull(self):
        self.gc.pull()

    def tearDown(self):
        os.popen("rm -rf " + self.testDir)

    def exists(self, filename):
        assert os.path.exists(self.testDir + filename)


@only_local
class TestSSHClone(TestHttpsClone):
    testDir = "./__testSSHClone"

    def setUp(self):
        self.gc = GitCmd(work_dir=self.testDir, url='git@github.com:philoprove/gitcmd.git')
        self.gc.clone()
        assert os.path.exists(self.testDir)
        self.exists('/README.rst')

    def testPull(self):
        self.gc.pull()

    def tearDown(self):
        os.popen("rm -rf " + self.testDir)


@only_local
class TestGitLabClone(TestHttpsClone):
    testDir = "./__testGitLabClone"

    def setUp(self):
        """
        put this file in local test dir:
                [myconfig.py]
                user, pwd = "gitlab user", "git lab password",
                url = 'gitlab url'
                commit_id = "commitid for test"
                commit_exists = '/path/somefilename'
        then pass this test
        :return:
        """
        self.cf = __import__("myconfig")
        self.gc = GitCmd(work_dir=self.testDir, user=self.cf.user, pwd=self.cf.pwd,
                         url=self.cf.url)
        self.gc.clone()

    def testCheckout(self):
        self.gc.checkout(self.cf.commit_id)
        self.exists(self.cf.commit_exists)
        self.gc.checkout()

    def testPull(self):
        self.gc.pull()
