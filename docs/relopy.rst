.. highlight:: bash
.. module:: relo

======
ReloPy
======

This tutorial intorduces you to the relopy script which
makes it easy to search your computer for anything you like.

.. rubric:: A quick overview:

* blablabla

.. _installation:

Installation
============

You need argparse and PyPdf installed for relopy to work correctly.
ReloPy is available with the Relo library on PyPi

.. code-block:: bash

    $ sudo pip install relo         # the recommended way
    $ sudo easy_install relo        # the alternative that works most of the time

You will need Python 2 installed, I recommend Python 2.7 but you should be fine with anything from 2.3 up.

Furthermore I recommend on always using `virtualenv <http://pypi.python.org/pypi/virtualenv>`_

.. _simple:

A simple start
==============

After everything is `set up <#installation>`_ you can do a quick search to
verify everything works.

.. note::

    These are all non-recursive examples for recursive ones look `here <#complex>`_.

.. rubric:: Simple filename search

In your home directory:

.. code-block:: bash

    $ relopy test

or

.. code-block:: bash

    $ relopy -n test

.. note::

    You can use both here since filename search is the standard search.

After a short amount of time it will print out all the matching files.

.. rubric:: Simple file content search

In some other directory then your home directory...

.. code-block:: bash

    $ relopy -c test

This will look through the files that are in your home directory and print out any results.

.. note::

    As of now only files that are supported are being searched, this will be changed in the future.

.. _complex:

A more complex approach
=======================

.. rubric:: The possibilities

For a quick check on what you can do and what options are available run:

.. code-block:: bash

    $ relopy -h         # short
    $ relopy --help     # long

.. rubric:: The arguments

* **Recursive (-r):** search directories recursively
* **Hidden (-a):** search even hidden files
* **Debug (--debug/--verbose):** Print out debug/verbose information (not implemented yet)
* **Directory (-d):** Select directory to search in


