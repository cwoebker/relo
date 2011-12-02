.. highlight:: python
.. currentmodule:: relo

=======
Roadmap
=======


Release 0.7
===========

.. rubric:: New Features

* **Relo Updater:** You can update the relo library from within relopy itself.
    * **Relo Extensions:** add extensions - thrid party - with updater
    * **DocType Managing:** Install, remove, update and find DocTypes.
    * **Missing DocType:** Notify user when a plugin is needed but available.
* **Symbolic Links:** Search through directories/files that are being linked symbolically. **IN PROGRESS (Python link support problem), postponed**

* **Better Printing**: improved way of posting information

* **Index Option** index files before search them, more efficient, nice database used for, redis?!?

.. rubric:: Improvements

* **Progress Bar:** There is now a progressbar to display how much of the search is done. **IN PROGRESS**
* **Relo Colorful:** (Maybe) Colors for better information flow. **DONE**


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

.. rubric:: DocType

Release 1.0
===========

.. rubric:: New Features

.. rubric:: Improvements

.. rubric:: DocType

Future
======

Indexing of files for faster search
index db generation one time, then changes
performance needed code in C

More DocTypes