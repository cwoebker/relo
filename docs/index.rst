.. relo documentation master file, created by
   sphinx-quickstart on Wed Aug 10 16:31:44 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Relo: Recursive Document Content Search!
========================================

Relo is a simple, lightweight and extensible Search tool and framework for Python. It is distributed as a
single script 'relopy' and a library that can be used in other python apps.

* **Content Search:** Search files recursively search a folder, with all its containing files, for a certain string.
* **Name Search:** Search filenames recursively in a certain folder.
* **Regex:** Use Regular Expressions to extend and improve search.
* **Plugins:** Manage and use Plugins to implement support for additional doctypes.

.. note::
    The Relo library doesn't actually return any results yet it just prints them out.
    Things like this will be implemented before the final stable version.

.. rubric:: Example: simple relo library

::

  from relo import Relo

  search = Relo(debug=False, hidden=False, content=True, recursive=True, directory='./', key='example')
  search.list()
  search.start()

Run this script or paste it into a python console, then watch the results come in.

.. note::
    More control can be achieved by using the relo.core library.

.. rubric:: Download and Install

.. note::
    Still not fully tested!

Content
=======
Start here:
* if you want to learn how to use the relo library or the relopy script.
* if you want to help contribute to the project.
* if you want to help to add additional doctypes.


.. toctree::
   :maxdepth: 2

Development and Contribution
============================

These chapters are intended for developers interested in helping with the development process.

.. toctree::
    :maxdepth: 2

    changelog
    development
    plugindev

.. toctree::
    :hidden:

    plugins/index

License
=======

Code and documentation are available according to the BSD License:

.. include:: ../LICENSE.txt
  :literal:

.. rubric:: Footnotes

.. [1] This is a test footnote cause I wanted to use one.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

