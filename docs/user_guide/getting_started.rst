Getting Started
===============

The common use-case for Pike is to enable dynamic loading of Python packages
from various locations on a user's filesystem. This is usually to facilitate
the usage of plugins.

The easiest way to use Pike to load Python packages is to use it as a context
manager:

.. code-block:: python

    from pike.discovery import py
    from pike.manager import PikeManager

    with PikeManager(['/path/containing/python/packages']):
        module = py.get_module_by_name('some_module.within_package')
        classes = py.classes_in_module(module)


If you need to use Pike for an extended period of time (such as for testing),
you can use a normal instance of Pike. However, the downside to that is that
you'll need to manually trigger Pike to cleanup itself when you're done.

.. code-block:: python

    from pike.discovery import py
    from pike.manager import PikeManager

    manager = PikeManager(['/path/containing/python/packages'])

    module = py.get_module_by_name('some_module.within_package')
    classes = py.classes_in_module(module)

    manager.cleanup()
