.. _guidelies:

***********************
Open Source Development
***********************

PySAL is an open source project and we invite any interested user who wants to
contribute to the project to contact one of the
`team members <http://code.google.com/p/pysal/people/list>`_. For users who
are new to open source development you may want to consult the following
documents for background information:

 * `Contributing to Open Source Projects HOWTO
   <http://www.kegel.com/academy/opensource.html>`_


**********
Guidelines
**********

PySAL is adopting many of the conventions in the larger scientific computing
in Python community and we ask that any one interested in joining the project
please review the following documents:

 * `Documentation standards <http://projects.scipy.org/numpy/wiki/CodingStyleGuidelines>`_
 * `Coding guidelines <http://www.python.org/dev/peps/pep-0008/>`_
 * :doc:`Testing guidelines </developers/testing>`


***********
Source Code
***********


PySAL uses `Google Code <http://code.google.com>`_ and subversion for our
`code repository <http://code.google.com/p/pysal/>`_.
Prospective developers can check out the current version using:

::

  svn checkout http://pysal.googlecode.com/svn/trunk/ pysal-read-only

while developers with commit rights can use:

::

  svn checkout https://pysal.googlecode.com/svn/trunk/ pysal --username username

substituting your Google username. When prompted, enter your generated
googlecode.com password.


You can setup PySAL for local development following the :doc:`installation instructions </users/installation>`.


************************
Development Mailing List
************************

Development discussions take place on `pysal-dev
<http://groups.google.com/group/pysal-dev>`_.


****************
Release Schedule
****************

PySAL development follows a six-month release schedule that is aligned with
the academic calendar.

1.0 Cycle
=========


======= ========   ================= ====================================================
Start   End        Phase             Notes
======= ========   ================= ====================================================
2/1/10  4/17/10    Module Proposals  Developers draft PEPs and prototype
4/17/10 4/30/10    Module Selection  Developers discuss candidate PEPS, BDFL calls vote
5/1/10  5/1/10     Module Approval   BDFL announces final approval
5/2/10  6/30/10    Development       Implementation and testing of approved modules
7/1/10  7/1/10     Code Freeze       APIs fixed, bug and testing changes only
7/1/10  7/30/10    Release Prep      Documentation, release build
7/31/10 7/31/10    Release           Official release of 1.0
======= ========   ================= ====================================================



1.1 Cycle
=========

========   ========   ================= ====================================================
Start      End        Phase             Notes
========   ========   ================= ====================================================
8/1/10     10/17/10   Module Proposals  Developers draft PEPs and prototype
10/17/10   10/30/10   Module Selection  Developers discuss candidate PEPS, BDFL calls vote
11/1/10    11/1/10    Module Approval   BDFL announces final approval
11/2/10    12/31/10   Development       Implementation and testing of approved modules
1/1/11       1/1/11   Code Freeze       APIs fixed, bug and testing changes only
1/1/11      1/30/11   Release Prep      Documentation, release build
1/31/11     1/31/11   Release           Official release  of 1.1
========   ========   ================= ====================================================


**********
Governance
**********

PySAL is organized around the Benevolent Dictator for Life (BDFL) model of project management.
The BDFL is responsible for overall project management and direction. Developers have a critical role in shaping that
direction. Specific roles and rights are as follows:

=========   ================        ===================================================
Title       Role                    Rights
=========   ================        ===================================================
BDFL        Project Director        Commit, Voting, Veto, Developer Approval/Management
Developer   Development             Commit, Voting
=========   ================        ===================================================

***************
Voting and PEPs
***************

During the initial phase of a release cycle, new functionality for PySAL should be described in a PySAL Enhancment
Proposal (PEP). These should follow the
`standard format  <http://www.python.org/dev/peps/pep-0009/>`_
used by the Python project. For PySAL, the PEP process is as follows

#. Developer prepares a plain text PEP following the guidelines

#. Developer sends PEP to the BDFL

#. Developer posts PEP to the PEP index

#. All developers consider the PEP and vote

#. PEPs receiving a majority approval become priorities for the release cycle



