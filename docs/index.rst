.. highlight:: python
.. currentmodule:: relo

.. _Python: http://python.org/
.. _issues: https://github.com/cwoebker/relo/issues
.. _PyPi: http://pypi.python.org/pypi/relo
.. _DocType: https://github.com/cwoebker/relo/tree/master/relo/doctype
.. _tests: https://github.com/cwoebker/relo/tree/master/tests

========================================
Relo: Recursive Document Content Search!
========================================

Relo is a simple, lightweight and extensible Search tool and framework for Python_. It is distributed as a
single script ``relopy`` and a library that can be used in other python apps.

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

.. _download:

You can use easy_install or pip as usual:

::

    easy_install relo
    pip install relo

.. note::
    Still not fully tested!

.. rubric:: Dependencies

.. _dependencies:

Relo needs the argparse library for parsing arguments.
Furthermore some of the plugins need libraries that help in loading
and reading different kinds of files.
As of now these libraries are:
    * **PyPdf:** Needed for reading pages from pdf files

.. note::

    The dependencies don't install automatically when installing relo for now, some issues
    wrapping my head around setup.py. Will be fixed soon.

        easy_install pypdf

        pip install pypdf

    When argparse doesn't come with your python version installed.

        easy_install argparse
        
        pip install argparse

Usage Guide
===========
Start here:

* **Learn:** how to use the relo library or the relopy script.
* **Contribute:**  to the project.
* **Contribute (DocType)** and add additional doctypes.


.. toctree::
   :maxdepth: 2

   tutorial
   plugins/index

Information Base
================
A database for tutorials, guides and other links that relate to relo.

.. toctree::
    :maxdepth: 2

    faq
    contact

Development and Contribution
============================

These chapters are intended for developers interested in helping with the development process.

.. toctree::
    :maxdepth: 2

    changelog
    roadmap
    development
    plugindev

.. toctree::
    :hidden:

    doctypes/index

License
=======

Code and documentation are available according to the BSD License:

.. include:: ../LICENSE.txt
  :literal:

Contact
=======

Email me at cwoebker@gmail.com

or check the :doc:`contact` page

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [1] This is a test footnote cause I wanted to use one.