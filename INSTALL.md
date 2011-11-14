Installing TJ
====================

by Phil Christensen
phil@bubblehouse.org

Once you install Python and Twisted, the rest will be taken care of by
the setup.py file. I recommend using [pip](http://pypi.python.org/pypi/pip),
but any setuptools-compatible method should work fine.

    git clone git://github.com/philchristensen/TJ.git
    cd TJ
    pip install --editable .

Next you should be able to start up the server with:

    twistd -n tjbot

The -n will keep it in the foreground. Configuration options are kept in the 
global settings file, *default.json*.