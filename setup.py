import os
from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "relo",
    version = "0.5.0",
    author = "Cecil Woebker",
    author_email = "cwoebker@gmail.com",
    desciption = ("Recursive Document Content Search in python"),
    license = "",
    keywords = "python search document content",
    url = "http://cwoebker.github.com/relo",
    packages=['', ''],
    long_desciption=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
    ],
)

