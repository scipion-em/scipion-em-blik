============
BLIK plugin
============

This plugin is wrapping BLIK programs from https://github.com/brisvag/blik
Blik is python tool for visualising and interacting with cryo-ET and subtomogram averaging data.

Installation
------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-blik

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-blik.git

    * install

    .. code-block::

        scipion installp -p path_to_scipion-em-blik --devel
