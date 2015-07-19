User Guide
==========

Get Started
-----------

The common use-case for Pike is to enable dynamic loading of Python packages
from various locations on a user's filesystem. This is usually to facilitate
the usage of plugins.

The easiest way to use Pike to load Python packages is to use it as a context
manager:

.. code-block:: python

    from pike.manager import PikeManager

    with PikeManager(['/path/containing/python/packages']) as mgr:
        classes = mgr.get_classes()


If you need to use Pike for an extended period of time (such as for testing),
you can use a normal instance of Pike. However, the downside to that is that
you'll need to manually trigger Pike to cleanup itself when you're done.

.. code-block:: python

    from pike.manager import PikeManager

    manager = PikeManager(['/path/containing/python/packages'])
    classes = manager.get_classes()
    manager.cleanup()


Discovery
----------

Pike also includes a set of discovery functions to allow for someone to find
modules or classes that have been imported or that are available on a filesystem.

* Documentation for imported module discovery: :mod:`pike.discovery.py`
* Documentation for filesystem discovery: :mod:`pike.discovery.filesystem`


Installation
------------

Install from PyPI
^^^^^^^^^^^^^^^^^

.. code-block:: shell

    pip install --upgrade pike

Install from source
^^^^^^^^^^^^^^^^^^^

You can find the source for Pike located on GitHub_. Once downloaded you can
install Pike using pip.

If you want to just do a normal source install of Pike the execute:

.. code-block:: shell

    # In the Pike source directory
    pip install .

If you want to make changes to Pike, then install execute:

.. code-block:: shell

    # In the Pike source directory
    pip install -e .


.. _GitHub: https://github.com/pyarmory/pike
