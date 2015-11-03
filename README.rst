
gitcmd
===================

.. image:: https://img.shields.io/pypi/v/gitcmd.svg
   :target: https://pypi.python.org/pypi/gitcmd
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/gitcmd.svg
    :target: https://pypi.python.org/pypi/gitcmd
    :alt: PyPI Monthly downloads

.. image:: https://travis-ci.org/philoprove/gitcmd.svg?branch=master
   :target: https://travis-ci.org/philoprove/gitcmd
   :alt: Build Status

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/gitcmd
   :alt: Wheel Status

.. image:: https://img.shields.io/codecov/c/github/philoprove/gitcmd/master.svg
   :target: http://codecov.io/github/philoprove/gitcmd?branch=master
   :alt: Coverage report

Overview
===================

gitcmd is a wrapper of 'git' command , it can interact with git command where need username and password.


Installation
===================

The quick way::
	
    pip install gitcmd



Usage
===================

**Clone git respositroy**
::
	
    from gitcmd import GitCmd
    clone_to = 'mydir'
    url = "https://github.com/philoprove/gitcmd.git"
    gitcmd = GitCmd(work_dir=clone_to, url=url)

if you clone with ssh, you may need config ssh key at first.

**Clone gitlab with username,password**
::

    from gitcmd import GitCmd
    import os
    gitcmd = GitCmd(work_dir="clone_to_where", url="", user="user",pwd="pwd")
    
    # work dir should be either empty or not exists
    gitcmd.clone()
    
    
    # after repository was cloned to local , you can execute other commands
    gitcmd.checkout()
    gitcmd.pull()
    gitcmd.execute("git diff ...")