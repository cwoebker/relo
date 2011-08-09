import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
version = __import__('relo.core').get_version()
setup(
    name = "Relo",
    version = version.replace(' ', '-'),
    author = "Cecil Woebker",
    author_email = "cwoebker@gmail.com",
    desciption = ("Recursive Document Content Search in python"),
    license = "BSD",
    keywords = "python search document content",
    url = "http://cwoebker.github.com/relo",
    packages=['relo', 'test'],
    long_desciption=read('README.rst'),
    scripts = ['relo/relo.py'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
    ],
)

