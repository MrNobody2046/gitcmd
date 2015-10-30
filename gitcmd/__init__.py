import os
import sys
import contextlib
import time

import pexpect


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
    debug = 0
    check_auth_timeout = 10

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
            ch.expect("[\s\S]*?Username for .*: ", timeout=self.check_auth_timeout)
            ch.sendline(self.user)
            ch.expect("[\s\S]*?Password for .*: ", timeout=self.check_auth_timeout)
            ch.sendline(self.pwd)
        except Exception, e:
            if self.debug:
                print e
        return ch

    def clone(self, timeout=60):
        if os.path.exists(self.work_dir):
            raise Exception("git repo's dir already exist")
        pexpect.run("mkdir -p %s" % self.work_dir)
        return self.wait_transfer_end(self.execute('git clone %s .' % self.url, wait=False), timeout)

    def pull(self, timeout=60):
        return self.wait_transfer_end(self.execute(cmd="git pull", wait=False), timeout)

    def fetch(self, timeout=60):
        ch = self.execute(cmd="git fetch")
        if ch.exitstatus == 0:
            return True
        else:
            return False

    def execute(self, cmd="git status", wait=True, timeout=60):
        self.need_work_dir()
        with working_directory(self.work_dir):
            child = self.auth_if_need(pexpect.spawn(cmd))
            if self.debug:
                child.logfile = sys.stdout
                sys.stdout.write("\t\t>>>>Execute: %s, wait=%s,timeout=%s\n" % (cmd, wait, timeout))
            if wait:
                self.wait(child, timeout)
            return child

    def checkout(self, commit_id="master", timeout=60, force=False):
        """
        :param commit_id:
        :return: Fasle checkout failed
                 True checkout not specified or success
        """
        _c = "git checkout %s " % commit_id
        if force:
            _c += ' -f'
        ch = self.execute(_c, timeout=timeout)
        cc = self.current_commit()
        if cc and commit_id in ['master', cc]:
            return True
        else:
            return False

    def reset(self, commit_id="", timeout=10):
        ch = self.execute("git reset --hard %s" % commit_id, wait=False)
        if ch.expect(['HEAD is now .*', 'fatal: [\S\s]*', pexpect.EOF], timeout=timeout) != 1:
            return True
        return False

    def wait(self, ch, timeout):
        _t = time.time()
        while ch.isalive():
            try:
                self.expect_eof(ch, 1)
                ch.close()
            except:
                pass
            if time.time() - _t > timeout:
                ch.close()
                raise TimeoutError(timeout)
            time.sleep(0.1)

    def expect_eof(self, ch, timeout):
        ch.expect(pexpect.EOF, timeout=timeout)

    def current_commit(self):
        return os.popen('cd %s && git rev-parse HEAD' % self.work_dir).read().strip()

    def wait_transfer_end(self, ch, timeout):
        flag = ch.expect(['Checking connectivity... done.', 'Already up-to-date.\r\n', 'fatal: [\S\s]*', pexpect.EOF, ],
                         timeout=timeout)
        if flag in (0, 1):
            self.wait(ch, timeout)
            return ch
        else:
            return False


class TimeoutError(Exception):
    def __init__(self, timeout):
        super(TimeoutError, self).__init__("TimeoutError(%ds)" % timeout)


class CmdExecuteError(Exception):
    def __init__(self, ch):
        msg = 'Args:%s,Closed:%s,ExitCode:%s' % (ch.args, ch.closed, ch.exitstatus)
        super(CmdExecuteError, self).__init__(msg)
