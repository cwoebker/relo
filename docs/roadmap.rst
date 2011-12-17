.. highlight:: python
.. currentmodule:: relo

=======
Roadmap
=======


Release 0.7
===========

.. rubric:: New Features

* **Relo Updater:** Notifies about new versions (auto download?)

* **Better Printing**: improved way of posting information

    * **Relo Colorful:** (Maybe) Colors for better information flow. **DONE**


* **Index Option** index files before search them, more efficient, nice database used for, redis?!?

.. rubric:: Improvements

* **Progress Bar:** There is now a progressbar to display how much of the search is done. **IN PROGRESS**
* **Relo Colorful:** (Maybe) Colors for better information flow. **DONE**

* **Code Restructuring** Code has been completely revamped


Release 0.8
===========

.. rubric:: New Features

* **Graphical User Interface (GUI):** A User interface in wxPython, PyQt4 or whatever fits best.

    * **Settings and Defaults:** Settings and Defaults stored in ~/.relo(py) .
    * **Plugin Manager:** Control the Plugin Manager from the GUI.
    * **MenuBar Icon:** Make relopy easily accessible through the menu bar.

* **Replace:** A replace function that can process all files and replace certain expressions with others.

.. rubric:: Improvements

* **Index DB:** Relo creates db files for faster searching, either when set or when already searched.

.. rubric:: DocType

* **Many advancements** you will see soon

Release 0.9
===========

.. rubric:: New Features

.. rubric:: Improvements

* **Total modularization** The relo library is going to be split up into its counterparts so it can be used more effectively

.. rubric:: DocType

Release 1.0
===========

.. rubric:: New Features

* **Cython** speed improvements

.. rubric:: Improvements

* **Code Check** Code is going to be checked completely. w/ pylint, pyflakes and pep8

.. rubric:: DocType

Future
======

Indexing of files for faster search
index db generation one time, then changes
performance needed code in C

More DocTypes