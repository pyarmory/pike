import sys
from pike.finder import PikeFinder


class PikeManager(object):
    def __init__(self, search_paths=None):
        """The Pike plugin manager

        The manager allows for the dynamic loading of Python packages for any
        location on a user's filesystem.

        :param list search_paths: List of path strings to include during module
            importing. These paths are only in addition to existing Python
            import search paths.


        Using PikeManager as a context manager:

        .. code-block:: python

            from pike.manager import PikeManager

            with PikeManager(['/path/containing/package']) as mgr:
                import module_in_the_package

        Using PikeManager instance:

        .. code-block:: python

            from pike.manager import PikeManager

            mgr = PikeManager(['/path/container/package'])
            import module_in_the_package
            mgr.cleanup()
        """
        self.module_finder = PikeFinder(search_paths)
        self.add_to_meta_path()

    def cleanup(self):
        """Removes Pike's import hooks

        This should be called if an implementer is not using the manager as
        a context manager.
        """
        if self.module_finder in sys.meta_path:
            sys.meta_path.remove(self.module_finder)

    def add_to_meta_path(self):
        """Adds Pike's import hooks to Python

        This should be automatically handled by Pike; however, this is method
        is accessible for very rare use-cases.
        """
        if self.module_finder in sys.meta_path:
            return

        if sys.version_info >= (3, 1, 0):
            sys.meta_path.insert(0, self.module_finder)
        else:
            sys.meta_path.append(self.module_finder)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __del__(self):
        self.cleanup()
