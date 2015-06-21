import os
import sys
import imp


class PikeLoader(object):
    def __init__(self, fullname, module_path):
        self.target_module_name = fullname
        self.module_path = module_path

    def is_package(self):
        filename = os.path.basename(self.module_path)
        return filename.startswith('__init__')

    def load_module(self, fullname):
        if self.target_module_name != fullname:
            raise ImportError('Cannot import module with this loader')

        if fullname in sys.modules:
            return sys.modules[fullname]

        module = self.load_module_by_path(fullname, self.module_path)
        package, _, _ = fullname.rpartition('.')

        if self.is_package():
            module.__path__ = [self.module_path]
            module.__package__ = fullname
        else:
            module.__package__ = package

        sys.modules[fullname] = module
        return module

    def load_module_by_path(self, module_name, path):
        _, ext = os.path.splitext(path)
        module = None
        if ext.lower() == '.py':
            module = imp.load_source(module_name, path)
        elif ext.lower() == '.pyc':
            module = imp.load_compiled(module_name, path)

        return module
