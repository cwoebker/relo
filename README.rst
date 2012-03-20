Relo: Intelligent cli search for Humans
=======================================

`Relo <http://relo.cwoebker.com>`_ recursively searches documents and analyzes them.

`Build Status <http://travis-ci.org/cwoebker/relo>`_
----------------------------------------------------

Master:

.. image:: https://secure.travis-ci.org/cwoebker/relo.png?branch=master

Develop:

.. image:: https://secure.travis-ci.org/cwoebker/relo.png?branch=develop


Usage
-----

``relo config``
  Changes settings and other global variables.

``relo update``
  Updates the relo installation.

``relo index``
  Creates an index of a given directory.

``relo search``
  Either searches a filesystem or an index if available.

``relo stats``
  Analyzes a filesystem or an index if available.


Installation
------------

Installing relo is easy with pip:

    $ pip install legit

You'll then be able to call upon the ``relo`` command at any time.

Documentation
--------------

Check `the homepage <http://relo.cwoebker.com/>`_.

Additionally try running ``relo --help`` for basic usage information.


Caveats
-------

- **Warning:** This is still beta. Do not use for anything hugely important.
