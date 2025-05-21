import os
import importlib.util
import importlib.abc

from pike.loader import PikeLoader


class PikeFinder(importlib.abc.MetaPathFinder):
    def __init__(self, paths=None):
        self.paths = paths or []

    def module_name_to_filename(self, fullname):
        separated_name = fullname.split('.')
        return os.path.join(*separated_name)

    def get_import_filename(self, module_path):
        for base_path in self.paths:
            target_path = os.path.join(base_path, module_path)
            is_pkg = os.path.isdir(target_path)

            if is_pkg:
                filename = os.path.join(target_path, '__init__.py')
            else:
                filename = '{}.py'.format(target_path)

            if os.path.exists(filename):
                return filename

    def find_module(self, fullname, path=None):
        converted_name = self.module_name_to_filename(fullname)
        module_path = self.get_import_filename(converted_name)

        if module_path:
            return PikeLoader(fullname, module_path)

    def find_spec(self, fullname, path, target=None):
        mod_name = fullname.rsplit('.', 1)[-1]
        for base_path in self.paths:
            # Try package: <base_path>/<mod_name>/__init__.py
            package_dir = os.path.join(base_path, mod_name)
            init_file = os.path.join(package_dir, '__init__.py')
            if os.path.isdir(package_dir) and os.path.isfile(init_file):
                loader = PikeLoader(fullname, init_file)
                spec = importlib.util.spec_from_file_location(
                    fullname,
                    init_file,
                    loader=loader,
                    submodule_search_locations=[package_dir]
                )
                return spec
            # Try module: <base_path>/<mod_name>.py
            module_file = os.path.join(base_path, mod_name + '.py')
            if os.path.isfile(module_file):
                loader = PikeLoader(fullname, module_file)
                spec = importlib.util.spec_from_file_location(
                    fullname,
                    module_file,
                    loader=loader
                )
                return spec
        return None
