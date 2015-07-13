Getting Started
===============

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
