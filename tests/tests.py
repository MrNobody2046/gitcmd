from git-cmd.gitcmd import GitExec
import unittest






class TestAll(unittest.TestCase):
    pass



if __name__ == "__main__":
    ge = GitExec('./wddt', "pipeline", "vrBfv2vhLbA6DzLF",
             'http://gitlab.breadtrip.com:1280/zhangyu/PipelineDemoServer.git')
    ge.checkout("7085cae918f45eec6470cffc966d1a884ebbcda1")
    ge.checkout()
    ge.pull()
