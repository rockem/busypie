.. BusyPie documentation master file, created by
   sphinx-quickstart on Wed Jan 13 23:35:59 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to busypie!
===================================
busypie is an easy and expressive utility to do busy-waiting in Python

|busypie_logo|

Although, most of the time, you wouldn't want to do much busy waiting in your production code,
testing is a different matter. When testing asynchronous systems,
it's very helpful to wait for some scenario to finish its course.

:pypi:`busypie` helps you perform busy waiting easily and expressively.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   install
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Usage

   basic
   exception
   polling
   timeout
   async
   duration






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |busypie_logo| image:: _static/busypie_logo2.png