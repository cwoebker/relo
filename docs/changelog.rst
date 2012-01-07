.. highlight:: python
.. currentmodule:: relo

===========================
Release Notes and Changelog
===========================

Release 0.7 (2012 Jan 7)
========================

* **Relo Updater:** Notifies about new versions (auto download?) **EXPERIMENTAL**

* **Better Printing**: improved way of posting information **DONE**

    * **Relo Colorful:** Colors for better information flow. **DONE**
    * **Progress Bar:** There is now a progressbar to display how much of the search is done. **DONE (but not part of the actual printing module)**

* **Index Option** index files before search them, more efficient **DONE**

* **Settings** config file plus a way to change settings **DONE**


Release 0.6 (2011 Sep 16)
=========================

.. rubric:: New Features

* **Documentation:** As part of this release the documentation will be implemented.
* **All option:** Search files even without a DocType plugin file.
* **Hidden option:** What used to be called --all will now be a real hidden option to search hidden files.
* **Specific File Search:** Search specific file types as long as there is a DocType.
* **Dynamic DocType loading:** DocType plugins are loaded only if needed.

.. rubric:: Improvements

* **Website improvement:** Website renewed.

.. rubric:: DocType

* some minor improvements

Release 0.5 (2011 Aug 10)
=========================

.. rubric:: New Features

* First release to be published on `PyPi <http://pypi.python.org/pypi/relo>`_.
* Renamed project from pysearch to relo.
* Completely updated project structure for better support as a library.
* relo.py script was renamed to relopy (without an ending).

.. rubric:: Improvements

* Nothing major here since Relo is still in early development although its already beta.

.. rubric:: DocType

* No new DocTypes were implemented.
* Pdf DocType was improved significantly.
* Some minor changes to all DocTypes.

Earlier Releases (PySearch)
===========================

.. rubric:: 0.4 beta (2011 Aug 9):

* implement doctypes for pdf (and chm if easily possible)
* fork own plugin framework based on yapsy and fit it to pysearches needs
* recursive search option, disabled by default

.. rubric:: 0.3 alpha (2011 Aug 3):

* Regular Expression Search
* Changed to Yapsy


.. rubric:: 0.2 alpha (2011 Aug 1):

* Implement different types of searches:

    * File name search
    * Content search

* Implement option to search hidden files


.. rubric:: 0.1 alpha (2011 Jul 31)

* Initial Public Release

* Implemented Basic Plugin System for different document types.

* Supported DocTypes:

	* (.txt) Normal Text Files
	* (.log) Logging Files