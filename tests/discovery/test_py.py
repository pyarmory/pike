import os
import textwrap
from pretend import stub

from pike.discovery import py
from pike.manager import PikeManager
from tests import utils


class BaseTestCase(object):
    def setup_method(self, method):
        self.temp_folder = utils.make_tmpdir()
        self.manager = PikeManager([self.temp_folder])
        self.pkg_name = 'pike_{}'.format(method.__name__)
        self.pkg_location = utils.create_working_package(
            self.temp_folder,
            self.pkg_name
        )

    def teardown_method(self, method):
        self.manager.cleanup()
        utils.remove_dir(self.temp_folder)


class TestPyDiscovery(BaseTestCase):
    def test_get_module_by_name(self):
        assert py.get_module_by_name(self.pkg_name) is not None

    def test_is_child_of_module(self):
        child = stub(__name__='sample.child')
        parent = stub(__name__='sample')

        assert py.is_child_of_module(child, parent)

    def test_import_from_path(self):
        mod_location = os.path.join(self.pkg_location, 'app.py')
        utils.write_file(mod_location)

        assert py._import_from_path(mod_location, self.pkg_name) is not None

    def test_child_modules_without_sub_packages(self):
        mod_location = os.path.join(self.pkg_location, 'app.py')
        utils.write_file(mod_location)

        parent_module = py.get_module_by_name(self.pkg_name)
        child_modules = list(py._child_modules(parent_module))

        assert len(child_modules) == 1

    def test_child_modules_with_sub_packages(self):
        subpkg_location = utils.create_working_package(
            self.pkg_location,
            'submod'
        )

        mod_location = os.path.join(self.pkg_location, 'app.py')
        utils.write_file(mod_location)
        submod_location = os.path.join(subpkg_location, 'other.py')
        utils.write_file(submod_location)

        parent_module = py.get_module_by_name(self.pkg_name)
        child_modules = list(py._child_modules(parent_module))

        assert len(child_modules) == 2


class TestDiscoverClasses(BaseTestCase):
    def setup_method(self, method):
        super(TestDiscoverClasses, self).setup_method(method)
        self.test_file_content = textwrap.dedent("""
        class SampleObj(object):
            pass

        class OtherObj(SampleObj):
            pass
        """)

        mod_location = os.path.join(self.pkg_location, 'app.py')
        utils.write_file(mod_location, self.test_file_content)

    def test_classes_in_module(self):
        module = py.get_module_by_name('{}.app'.format(self.pkg_name))
        assert len(list(py.classes_in_module(module))) == 2

    def test_get_all_classes(self):
        module = py.get_module_by_name(self.pkg_name)
        assert len(list(py.get_all_classes(module))) == 2

    def test_get_child_modules(self):
        subpkg_location = utils.create_working_package(
            self.pkg_location,
            'sub_mod'
        )
        mod_location = os.path.join(subpkg_location, 'something.py')
        utils.write_file(mod_location)

        module = py.get_module_by_name(self.pkg_name)
        # Recursive
        assert len(list(py.get_child_modules(module))) == 3

        # Non-Recursive
        assert len(list(py.get_child_modules(module, False))) == 2
