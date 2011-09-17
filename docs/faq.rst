.. module:: relo

==========================
Frequently Asked Questions
==========================

About Relo
==========

Is Relo efficient and fast enough to use in my own app
------------------------------------------------------

Relo is still being developed so it is not fully stable.
Most importantly the speed always depends on what you are searching:

    * Are you doing a Name or Content Search?
    * How many files are there?
    * How big are those files?

Common Problems
===============

Relo doesn't find anything in my PDF file
-----------------------------------------

Relo uses the PyPdf library. As of now its using a function that help extract
text out of a pdf, unfortunately this function doesn't always work.
For some PDFs it returns an empty string and therefore relo itself can't find anything.
