Colour Science Meta-Repository
==============================

.. start-badges

|gitter| |twitter|

.. |gitter| image:: https://img.shields.io/gitter/room/colour-science/colour
    :target: https://gitter.im/colour-science/colour/
    :alt: Gitter
.. |twitter| image:: https://img.shields.io/twitter/follow/colour_science.svg?label=Follow&style=social
    :target: https://twitter.com/colour_science

.. end-badges

Introduction
------------

This meta-repository contains all the `Colour Science <https://www.colour-science.org/>`__
projects as Git submodules, providing a convenient way to work with the entire
ecosystem.

Included Repositories
---------------------

- `colour <https://github.com/colour-science/colour>`__: Colour Science for Python
- `colour-checker-detection <https://github.com/colour-science/colour-checker-detection>`__: Colour checker detection library
- `colour-clf-io <https://github.com/colour-science/colour-clf-io>`__: Common LUT Format (CLF) I/O library
- `colour-dash <https://github.com/colour-science/colour-dash>`__: Dash-based web application for colour science
- `colour-datasets <https://github.com/colour-science/colour-datasets>`__: Colour science datasets
- `colour-demosaicing <https://github.com/colour-science/colour-demosaicing>`__: CFA demosaicing algorithms
- `colour-hdri <https://github.com/colour-science/colour-hdri>`__: HDRI processing algorithms
- `colour-specio <https://github.com/colour-science/colour-specio>`__: Spectral I/O library
- `colour-visuals <https://github.com/colour-science/colour-visuals>`__: Colour science visuals

Getting Started
---------------

Clone with Submodules
~~~~~~~~~~~~~~~~~~~~~

To clone this repository with all submodules::

    git clone --recursive https://github.com/colour-science/colour-science.meta.git
    cd colour-science.meta

Update Submodules
~~~~~~~~~~~~~~~~~

To update all submodules to their latest versions::

    git submodule update --remote --merge

Working with Individual Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each submodule is a fully functional Git repository. For contributing to individual
projects, please refer to the `Contributing Guide <https://www.colour-science.org/contributing/>`__.

Common Operations
-----------------

Initialize Submodules
~~~~~~~~~~~~~~~~~~~~~

If you cloned without ``--recursive``::

    git submodule update --init --recursive

Pull Latest Changes
~~~~~~~~~~~~~~~~~~~

To pull latest changes for all submodules::

    git submodule foreach git pull origin master

Check Status
~~~~~~~~~~~~

To check the status of all submodules::

    git submodule foreach git status

Development Environment
-----------------------

Each repository has its own development requirements. Please refer to the
individual repository documentation for specific setup instructions.

Common Setup
~~~~~~~~~~~~

Most repositories use ``uv`` for dependency management::

    cd colour
    uv sync --all-extras

Code of Conduct
---------------

The *Code of Conduct*, adapted from the `Contributor Covenant 1.4 <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`__,
is available on the `Code of Conduct <https://www.colour-science.org/code-of-conduct/>`__ page.

Contact & Social
----------------

The *Colour* developers can be reached via different means:

- `Email <mailto:colour-developers@colour-science.org>`__
- `Facebook <https://www.facebook.com/python.colour.science>`__
- `Github Discussions <https://github.com/colour-science/colour/discussions>`__
- `Gitter <https://gitter.im/colour-science/colour>`__
- `Twitter <https://twitter.com/colour_science>`__

About
-----

| **Colour Science** by Colour Developers
| Copyright 2025 Colour Developers – `colour-developers@colour-science.org <colour-developers@colour-science.org>`__
| This software is released under terms of BSD-3-Clause: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/colour-science/colour-science.meta <https://github.com/colour-science/colour-science.meta>`__