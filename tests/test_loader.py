import os

import pytest
from pike.finder import PikeFinder
from pike.loader import PikeLoader
from tests import utils


SIMPLE_CLASS = """
class Tracer(object):
    pass
"""


class TestLoader(object):
    def setup_method(self, method):
        self.temp_folder = utils.make_tmpdir()

        # Create a simple package
        pkg_location = utils.create_working_package(self.temp_folder)
        mod_location = os.path.join(pkg_location, 'app.py')
        utils.write_file(mod_location, SIMPLE_CLASS)

        self.finder = PikeFinder([self.temp_folder])
        self.loader = PikeLoader('pike_tests.app', mod_location)

    def teardown_method(self, method):
        utils.remove_dir(self.temp_folder)

    def test_load_module_raises_import_error_with_bad_fullname(self):
        with pytest.raises(ImportError):
            self.loader.load_module('bam')

    def test_is_package(self):
        loader = self.finder.find_module('pike_tests')
        assert loader.is_package()

    def test_module_isnt_package(self):
        loader = self.finder.find_module('pike_tests.app')
        assert not loader.is_package()

    def test_load_package_module(self):
        loader = self.finder.find_module('pike_tests')
        module = loader.load_module('pike_tests')
        assert module is not None

    def test_second_load_pulls_previously_loaded_module(self):
        first_load = self.loader.load_module('pike_tests.app')
        second_load = self.loader.load_module('pike_tests.app')
        assert first_load == second_load
