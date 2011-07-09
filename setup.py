#!/usr/bin/python

from distutils.core import setup
from glob import glob
import sys

import platform
if platform.system() == "Windows":
    # modulefinder can't handle runtime changes to __path__ but win32com uses them
    try:
        try:
            import py2exe.mf as modulefinder
        except ImportError:
            import modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]:
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        #no worries
        pass

    import py2exe

    sys.path.append("C:\\Microsoft.VC90.CRT")

    data_files = [("Microsoft.VC90.CRT", glob(r'C:\\Microsoft.VC90.CRT\*.*'))]
    setup(console=['photoflow.py'], windows=['gui.py'], data_files=data_files)

