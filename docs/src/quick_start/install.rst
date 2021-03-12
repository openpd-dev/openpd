==============
Install OpenPD
==============

1. OpenPD is distributed by PyPI (https://pypi.org/project/openpd). The user can install it through:

.. code-block:: console
    :linenos:

    pip install openpd

2. After that, run the tests by following:

.. code-block:: console
    :linenos:

    python -m openpd.runTest

If no error message is popped out, the installation is completed.

.. important:: 

    As OpenPD is only tests for python version >= 3.7, so make sure the python version matches the requirement.

For testing with multiprocessors, user can run tests by:

.. code-block:: console
    :linenos:

    python -m openpd.runTest -n <number of processes>

For example:

.. code-block:: console
    :linenos:

    python -m openpd.runTest -n 4

will executes the tests with 4 processors.

============
Build OpenPD
============

The user can also build OpenPD locally by following steps below:

1. Download the tarball from github:

.. code-block:: console
    :linenos:

    git clone https://github.com/zhenyuwei99/openpd.git

2. Build OpenPD:
   
.. code-block:: console
    :linenos:

    cd <openpd source dir>
    python setup.py install --record files.txt

.. note::

    .. code-block:: console
        :linenos:

        python setup.py install

    also works, but ``--record files.txt`` will be useful if the user need to remove or rebuild OpenPD.

3. Test OpenPD:

.. code-block:: console
    :linenos:

    cd ..
    python -m openpd.runTest

4. Remove OpenPD:

.. code-block:: console
    :linenos:

    cd <openpd source dir>
    xargs rm -rf < files.txt
    
.. tip::

    We suggest user to build OpenPD instead of install it through ``pip`` to get the tutorials contained in the tarball.

.. _build-doc:

====================
Build Documentation
====================

If the tarball of OpenPD has been downloaded, the user can also build the documentation locally. 


1. The document of OpenPD is compiled by Sphinx. Install Sphinx for the first:

.. code-block::
    :linenos:

    pip install sphinx

2. Build html:

.. code-block::
    :linenos:

    cd <openpd source dir>
    cd docs
    make html # file will stored in <openpd source dir>/docs/build/html

3. Build epub:

.. code-block::
    :linenos:

    cd <openpd source dir>
    cd docs
    make epub # file will stored in <openpd source dir>/docs/build/epub
