# Package Admin
Some notes on package maintenance, take from the official docs [here](https://packaging.python.org/tutorials/packaging-projects/).

## Generate Distribution
Ensure latest builds tools.
```
% python3 -m pip install --upgrade setuptools wheel
Collecting setuptools
  Downloading setuptools-46.1.3-py3-none-any.whl (582 kB)
     |████████████████████████████████| 582 kB 966 kB/s
Requirement already up-to-date: wheel in /usr/local/lib/python3.8/site-packages (0.34.2)
Installing collected packages: setuptools
  Attempting uninstall: setuptools
    Found existing installation: setuptools 46.0.0
    Uninstalling setuptools-46.0.0:
      Successfully uninstalled setuptools-46.0.0
Successfully installed setuptools-46.1.3
```
Build the distribution archive.
```
% python3 setup.py sdist bdist_wheel
running sdist
running egg_info
creating typetastic.egg-info
writing typetastic.egg-info/PKG-INFO
writing dependency_links to typetastic.egg-info/dependency_links.txt
writing top-level names to typetastic.egg-info/top_level.txt
writing manifest file 'typetastic.egg-info/SOURCES.txt'
<< SNIPPED >>
adding 'typetastic-0.0.1.dist-info/WHEEL'
adding 'typetastic-0.0.1.dist-info/top_level.txt'
adding 'typetastic-0.0.1.dist-info/RECORD'
removing build/bdist.macosx-10.15-x86_64/wheel
```
We should now have:
```
% ls -l dist
total 40
-rw-r--r--  1 dougb  staff  14697 17 Apr 17:18 typetastic-0.0.1-py3-none-any.whl
-rw-r--r--  1 dougb  staff   2569 17 Apr 17:18 typetastic-0.0.1.tar.gz
```

## Install Locally
We can install the new package locally, for testing.
```
% pip3 install dist/typetastic-0.0.1.tar.gz
Processing ./dist/typetastic-0.0.1.tar.gz
Building wheels for collected packages: typetastic
  Building wheel for typetastic (setup.py) ... done
  Created wheel for typetastic: filename=typetastic-0.0.1-py3-none-any.whl size=2396 sha256=d6b7950b4b8e31b1ed760348af6d36e4330b228d059537f2605ec3f98ae7749f
  Stored in directory: /Users/dougb/Library/Caches/pip/wheels/c5/a8/dd/d5ba1e1e6852785ece29b60606dbda4ec54420e967f7fc5c5b
Successfully built typetastic
Installing collected packages: typetastic
Successfully installed typetastic-0.0.1
```
And check the installed package.
```
% pip3 show typetastic
Name: typetastic
Version: 0.0.1
Summary: Python utility to make recording screencasts easier.
Home-page: https://github.com/thisdougb/typetastic
Author: Doug Bridgens
Author-email: typetastic@far-oeuf.com
License: UNKNOWN
Location: /usr/local/lib/python3.8/site-packages
Requires:
Required-by:
```
