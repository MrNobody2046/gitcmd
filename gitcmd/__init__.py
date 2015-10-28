import pexpect
import os
import contextlib


@contextlib.contextmanager
def working_directory(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


class GitCmd(object):
    """
    execute git commands , clone, pull , etc
    authorize with git server if necessary
    """
    debug = False
    check_auth_timeout = 1

    def __init__(self, work_dir=".", user="", pwd="", url=""):
        """
        :param work_dir: repository dir, this dir can be the
        exist dir if you want execute commands manage git repo.
        and if dir not exist , you must use .clone method first
        to create this dir
        :param user: username in case of auth
        :param pwd: password in case of auth
        :param url: git repository's url
        """
        if not work_dir and url:
            raise Exception("Must have repository ")
        self.user = user
        self.pwd = pwd
        self.work_dir = work_dir
        self.url = url

    def need_work_dir(self):
        if not os.path.exists(self.work_dir):
            raise Exception("git repo's dir not exist")

    def auth_if_need(self, ch):
        try:
            print ch.expect("[\s\S]*?Username for .*: ", timeout=self.check_auth_timeout)
            ch.sendline(self.user)
            ch.expect("[\s\S]*?Password for .*: ", timeout=self.check_auth_timeout)
            ch.sendline(self.pwd)
        except Exception, e:
            if self.debug:
                print e
        return ch

    def clone(self):
        if os.path.exists(self.work_dir):
            raise Exception("git repo's dir already exist")
        pexpect.run("mkdir -p %s" % self.work_dir)
        ch = self.execute('git clone %s .' % self.url)
        if self.transfer_finished(ch):
            ch.wait()
            return True
        else:
            ch.close()
            return False

    def pull(self):
        return self.execute(cmd="git pull")

    def execute(self, cmd="git status"):
        self.need_work_dir()
        with working_directory(self.work_dir):
            child = self.auth_if_need(pexpect.spawn(cmd))
            return child

    def checkout(self, commit_id="master"):
        return self.execute("git checkout %s" % commit_id)

    def transfer_finished(self, ch):
        try:
            ch.expect("Checking connectivity... done.", timeout=180)
            return True
        except:
            return False


