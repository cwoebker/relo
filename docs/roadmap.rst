.. highlight:: python
.. currentmodule:: relo

=======
Roadmap
=======

Release 0.6
===========

.. rubric:: New Features

* **Documentation:** As part of this release the documentation will be finished. **IN PROGRESS**
* **Symbolic Links:** Search through directories/files that are being linked symbolically. **IN PROGRESS (Python link support problem)**
* **All option:** Search files even without a DocType plugin file. **DONE**
* **Hidden option:** What used to be called --all will now be a real hidden option to search hidden files. **DONE**
* **Specific File Search:** Search specific file types as long as there is a DocType. **DONE**
* **Dynamic DocType loading:** DocType plugins are loaded only if needed. **IN PROGRESS**

.. rubric:: Improvements

* **Website improvement:** Website renewed.

.. rubric:: DocType

* **Microsoft Html Help (.chm):** implemented since some ebooks are distributed in this format.

Release 0.7
===========

.. rubric:: New Features

* **Logging:** A logging class to implement debugging mode and other features.
* **DocType Managing:** Install, remove, update and find DocTypes.
* **Missing DocType:** Notify user when a plugin is needed but available.

.. rubric:: Improvements

* **Progress Bar:** There is now a progressbar to display how much of the search is done.
* **Relo Colorful:** (Maybe) Colors for better information flow:

    * **Error:** Red
    * **INFO:** White
    * **DEBUG:** Yellow

.. rubric:: DocType

Release 0.8
===========

.. rubric:: New Features

* **Graphical User Interface (GUI):** A User interface in wxPython, PyQt4 or whatever fits best.

    * **Settings and Defaults:** Settings and Defaults stored in ~/.relo(py) .
    * **Plugin Manager:** Control the Plugin Manager from the GUI.
    * **MenuBar Icon:** Make relopy easily accessible through the menubar.


.. rubric:: Improvements

* **Index DB:** relo created db files for faster searching, either when set or when already searched.

.. rubric:: DocType

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