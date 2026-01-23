.. BusyPie documentation master file, created by
   sphinx-quickstart on Wed Jan 13 23:35:59 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to busypie!
===================================
busypie is an easy and expressive busy-waiting library for Python.

|busypie_logo|

Although you typically wouldn't want to do much busy-waiting in production code,
testing is a different matter. When testing asynchronous systems,
it's very helpful to wait for a scenario to complete.

:pypi:`busypie` helps you perform busy waiting easily and expressively.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   install
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Usage

   exception
   polling
   timeout
   duration
   assert


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |busypie_logo| image:: _static/busypie_logo2.png
