.. OpenPD documentation master file, created by
   sphinx-quickstart on Sun Jan 17 23:36:15 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
OpenPD Documentation
===================================

OpenPD, standing for **Open** **P**\ eptide **D**\ ynamics, is a toolkit based on Python, distributed freely under the terms of
**MIT** License, for peptide dynamics simulation. It was designed to simulate the folding dynamics of protein efficiently with the assistance of **P**\ eptide **D**\ ynamics **F**\ orce **F**\ ield (PDFF), which is a solvent considered, high-level coarse-grained force field focusing on the peptide interaction. 

This document is part of the OpenPD distribution, which can be found in our `GitHub site <https://github.com/zhenyuwei99/openpd>`_. Users can also build the document manually in PDF format by following steps in :doc:`quick_start/build_doc` or click the ``version`` button at the right-bottom of browser.


OpenPD is developed and maintained by Zhenyu Wei (zhenyuwei99@gmail.com), from Yunfei Chen's group in Southeast University. As a newly developed program, we always welcome developers to contact us or discuss in our `GitHub site <https://github.com/zhenyuwei99/openpd>`_

The document is organized in four parts:

(1) The :ref:`Quick Start <quickstart>` part contains our program's introduction and the installation suggestions.
(#) The :ref:`Tutorials <tutorials>` part shows several primary example codes to giving users a directive intuition of workflow and features of OpenPD
(#) The :ref:`Peptide Dynamics Force Field <pdff>` part describes the component of PDFF and their developing procedure.
(#) The :ref:`Module indices <module>` part giving a detailed description of all packages and classes in OpenPD.  

.. tip:: Once you are familiar with OpenPD, The :ref:`Module indices <module>` part will be very useful for a quick code check.

=============
Contents
=============

.. toctree::
   :maxdepth: 1
   :numbered: 3
   :caption: Quick start
   :name: quickstart
   :includehidden:

   quick_start/intro
   quick_start/install
   quick_start/build
   quick_start/build_doc 

.. toctree::
   :maxdepth: 1
   :numbered: 3
   :caption: Peptide Dynamics Force Field
   :name: pdff
   :includehidden:

   pdff/overview 
   pdff/nonBonded
   pdff/torsion

.. toctree::
   :maxdepth: 1
   :numbered: 3
   :caption: Tutorials
   :name: tutorials
   :includehidden:

   tutorials/howto_useunit/main
   tutorials/howto_createSystem/main
   tutorials/howto_createEnsemble/main
   tutorials/howto_runSimulation/main

.. toctree::
   :maxdepth: 1
   :numbered: 3
   :caption: Module indices
   :name: module
   :includehidden:

   modules/unit/main
   modules/core/main
   modules/loader/main
   modules/force/main
   modules/dumper/main
   modules/integrator/main
   modules/visualizer/main
   modules/ensemble
   modules/forceEncoder
   modules/simulation

