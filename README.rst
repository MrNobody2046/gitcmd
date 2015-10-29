
gitcmd
===================


.. image:: https://travis-ci.org/philoprove/gitcmd.svg?branch=master
   :target: https://travis-ci.org/philoprove/gitcmd
   :alt: Build Status

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
    ge = GitCmd(work_dir=clone_to, url=url)

if you clone with ssh, you may need config ssh key at first.

**Clone gitlab with username,password**
::

    from gitcmd import GitCmd
    import os
    ge = GitCmd(work_dir="clone_to_where", url="", user="user",pwd="pwd")
    
    # work dir should be either empty or not exists
    ge.clone()
    
    
    # after repository was cloned to local , you can execute other commands
    ge.checkout()
    ge.pull()
    ge.execute("git diff ...")