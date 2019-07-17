.. Raven documentation master file, created by
   sphinx-quickstart on Wed Jun 26 12:10:20 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Raven
=====

Overview
--------
The purpose of RAVEN is to act as an intermediary interface between a client and the telemetry archive. In this context a client can be either
an individual who desires structured telemetry or a higher-level application. Raven is a DRF-Based RESTful (https://www.django-rest-framework.org/)
service. The API was built using the lower-level jSka.jeta_ module of the jSka_ package.
jSka.jeta_ is derived from the eng_archive of the Ska_ package provided by the Chandra Spacecraft team
and includes similar capabilities for JWST. If lower level data analysis is required then users may use the command-line
tools provided in the jSka_ environment.

.. _Ska: http://cxc.cfa.harvard.edu/mta/ASPECT/tool_doc/pydocs/
.. _jSka: https://pljwkadi.stsci.edu/
.. _jSka.jeta: https://pljwkadi.stsci.edu/

Example Call
------------

.. code-block:: bash

    $ curl https://localhost:1234/api/v1/fetch?mnemonic=MNEMONIC


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   fetch



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
