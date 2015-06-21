import sys
from pike.finder import PikeFinder


class PikeManager(object):
    def __init__(self, search_paths=None):
        self.module_finder = PikeFinder(search_paths)
        self.add_to_meta_path()

    def cleanup(self):
        if self.module_finder in sys.meta_path:
            sys.meta_path.remove(self.module_finder)

    def add_to_meta_path(self):
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
