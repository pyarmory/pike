import os

from pike.discovery import filesystem
from tests import utils


class TestFilesystemDiscovery(object):
    def setup_method(self, method):
        self.temp_folder = utils.make_tmpdir()

    def teardown_method(self, method):
        utils.remove_dir(self.temp_folder)

    def test_find_modules(self):
        pkg_location = utils.create_working_package(self.temp_folder)
        mod_location = os.path.join(pkg_location, 'app.py')
        utils.write_file(mod_location)

        assert len(list(filesystem.find_modules(pkg_location))) == 1

    def test_find_modules_in_empty_package(self):
        pkg_location = utils.create_working_package(self.temp_folder)
        assert len(list(filesystem.find_modules(pkg_location))) == 0

    def test_find_packages(self):
        utils.create_working_package(self.temp_folder)
        assert len(list(filesystem.find_packages(self.temp_folder))) == 1

    def test_find_packages_in_empty_folder(self):
        assert len(list(filesystem.find_packages(self.temp_folder))) == 0

    def test_recursive_find_packages(self):
        pkg_location = utils.create_working_package(self.temp_folder)
        utils.create_working_package(pkg_location, 'bam')

        pkgs = filesystem.recursive_find_packages(self.temp_folder)

        assert len(list(pkgs)) == 2

    def test_recursive_find_modules(self):
        pkg_location = utils.create_working_package(self.temp_folder)
        subpkg_location = utils.create_working_package(pkg_location, 'bam')

        mod_location = os.path.join(pkg_location, 'app.py')
        utils.write_file(mod_location)
        mod_location = os.path.join(subpkg_location, 'other.py')
        utils.write_file(mod_location)

        pkgs = filesystem.recursive_find_modules(pkg_location)

        assert len(list(pkgs)) == 2
