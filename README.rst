.. inclusion-marker-do-not-remove

Lovely Rita: Insights from Oakland Citation Data
================================================

Lovely Rita is set of tools for reading, cleaning, and saving parking parking citation datasets. The project is a part of Oakland's Code for America brigade `OpenOakland <http://openoakland.org/>`_. You can read more about the project in this `presentation <https://goo.gl/XiUvkB>`_.

With Lovely Rita, you can load historical parking citation data, clean the data (addresses and dates), geocode (turn addresses into geospatial coordinates), and save cleaned data to shapefiles for GIS analyses.

Check out our `documentation <https://openoakland.github.io/lovely-rita/>`_ for more detail.


Installation
============

It is good practice to use a `virtual environment <https://virtualenv.pypa.io/en/stable/>`_.

.. code-block:: bash

    git clone https://github.com/r-b-g-b/lovely-rita.git
    cd lovely-rita
    pip install -r requirements.txt
    pip install . --user


Raw data format
===============

Raw data should be provided in a `.csv` with the column names (in any order):

+------------------------+
|ticket_number           |
+------------------------+
|ticket_issue_date       |
+------------------------+
|ticket_issue_time       |
+------------------------+
|street_name             |
+------------------------+
|street_name             |
+------------------------+
|street_no               |
+------------------------+
|street_suffix           |
+------------------------+
|violation_external_code |
+------------------------+
|violation_desc_long     |
+------------------------+
|state                   |
+------------------------+
|city                    |
+------------------------+
|badge__                 |
+------------------------+
|fine_amount             |
+------------------------+


Command line interface
======================

Several useful workflows can be run from the command line. Learn about the available workflows using ``lovelyrita --help``. Learn about a specific workflow using ``lovelyrita <workflow> --help``.


Python interface
================

There is also a python inferface if you want to dive deeper into the data. There are more involved examples in the `notebooks <https://github.com/openoakland/lovely-rita/tree/master/notebooks>`_ folder.

Read in the data
----------------

.. code-block:: python

    from lovelyrita.data import read_data
    citations = read_data(data_path)


Clean the data
--------------
Lovely Rita can also clean and parse addresses and dates.

.. code-block:: python

    from lovelyrita.data import read_data
    from lovelyrita.clean import clean
    citations = read_data(data_path)
    citations = clean(citations)


Analyze the data
----------------

1. Number of citations per zip code
2. Time-series, number of citations
3. Type of violation by zip code


Save the data
-------------
There is also support for storing the data to shapefiles

.. code-block:: python

    from lovelyrita.data import write_shapefile
    write_shapefile(citations, 'my-shapefile.shp')


Documentation
=============

.. code-block:: bash

    git clone -b gh-pages http://github.com/openoakland/lovely-rita.git lovely-rita-docs


Tests
=====

There will be tests.


Contributing
============

Please read `CONTRIBUTING.md <https://gist.github.com/PurpleBooth/b24679402957c63ec426>`_ for details on our code of conduct, and the process for submitting pull requests to us.


Authors
=======

See our `list of contributors <https://github.com/r-b-g-b/lovely-rita/blob/master/CONTRIBUTORS.md>`_ to learn about the many wonderful people who helped design and build Lovely Rita.


License
=======

This project is licensed under the MIT License - see the `license file <https://github.com/r-b-g-b/lovely-rita/blob/master/LICENSE.txt>`_ for details.

Acknowledgments
===============

We would like to acknowledge the help of Danielle Dai and the Oakland Department of Transportation for providing the data and invaluable guidance for this project.
