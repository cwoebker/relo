import os
from setuptools import setup, find_packages
from distutils.command.install import INSTALL_SCHEMES

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Relo",
    version = '0.7-beta',
    author = "Cecil Woebker",
    author_email = "cwoebker@gmail.com",
    homepage = "cwoebker.com",
    maintainer = "Cecil Woebker",
    maintainer_email = "cwoebker@gmail.com",
    description = ("Recursive Document Content Search in Python"),
    keywords = "python search document content",
    url = "http://cwoebker.com/relo",
    packages = find_packages(),
    include_package_data=True,
    long_description=read('README.rst'),
    scripts = ['relopy'],
    install_requires=['BeautifulSoup >= 3.2.0', 'pdfminer >= 20110515', 'argparse >= 1.2.1', 'redis >= 2.4.10', 'progressbar >= 2.3'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
    ],
)

