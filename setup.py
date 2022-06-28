"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['tools_ui.py']
DATA_FILES = ['--iconfile']
OPTIONS = {'iconfile': '/Users/andreykrivoshey/Work/Repositories/processing_tools/Assets/icon.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)