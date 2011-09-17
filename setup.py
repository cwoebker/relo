import os
from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
relo_dir = 'relo'

for dirpath, dirnames, filenames in os.walk(relo_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    reloList=[]
    for file in filenames:
        if '.relo' in file:
            reloList.append(file)
    if reloList == []:
        continue
    data_files.append((dirpath, reloList))

#[os.path.join(dirpath, f) for f in filenames]

version = __import__('relo').get_version()
setup(
    name = "Relo",
    version = version.replace(' ', '-'),
    author = "Cecil Woebker",
    author_email = "cwoebker@gmail.com",
    maintainer = "Cecil Woebker",
    maintainer_email = "cwoebker@gmail.com",
    description = ("Recursive Document Content Search in Python"),
    keywords = "python search document content",
    url = "http://cwoebker.github.com/relo",
    packages = packages,
    package_data={'relo': ['*.relo', 'doctype/*.relo']},
    #data_files = data_files,
    long_description=read('README.rst'),
    scripts = ['relopy'],
    install_requires=['pypdf >= 1.13', 'argparse >= 1.2.1'],
    #requires=['pypdf >= 1.13'],
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

