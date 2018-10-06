import os
import py_compile
import six

import pytest
from pike.finder import PikeFinder
from pike.loader import PikeLoader
from tests import utils


SIMPLE_CLASS = """
class Tracer(object):
    pass
"""


@pytest.fixture
def loader_finder():
    temp_folder = utils.make_tmpdir()

    # Create a simple package
    pkg_location = utils.create_working_package(temp_folder)
    mod_location = os.path.join(pkg_location, 'app.py')
    utils.write_file(mod_location, SIMPLE_CLASS)

    finder = PikeFinder([temp_folder])
    loader = PikeLoader('pike_tests.app', mod_location)

    yield loader, finder

    utils.remove_dir(temp_folder)


@pytest.fixture
def compiled_loader():
    temp_folder = utils.make_tmpdir()

    # Create a simple package
    pkg_location = utils.create_working_package(temp_folder, 'compile_test')
    mod_location = os.path.join(pkg_location, 'app.py')
    utils.write_file(mod_location, SIMPLE_CLASS)

    py_compile.compile(mod_location)

    yield temp_folder

    utils.remove_dir(temp_folder)


def test_load_module_raises_import_error_with_bad_fullname(loader_finder):
    loader, _ = loader_finder

    with pytest.raises(ImportError):
        loader.load_module('bam')


def test_is_package(loader_finder):
    _, finder = loader_finder

    loader = finder.find_module('pike_tests')
    assert loader.is_package()


def test_module_isnt_package(loader_finder):
    _, finder = loader_finder

    loader = finder.find_module('pike_tests.app')
    assert not loader.is_package()


def test_load_package_module(loader_finder):
    _, finder = loader_finder

    loader = finder.find_module('pike_tests')
    module = loader.load_module('pike_tests')
    assert module is not None


def test_second_load_pulls_previously_loaded_module(loader_finder):
    loader, _ = loader_finder

    first_load = loader.load_module('pike_tests.app')
    second_load = loader.load_module('pike_tests.app')
    assert first_load == second_load


def test_load_module_by_path_with_invalid_path(loader_finder):
    loader, _ = loader_finder

    module = loader.load_module_by_path('name', 'something.bam')
    assert module is None


@pytest.mark.skip('pyc loading is disabled')
def test_loading_pyc(compiled_loader):
    finder = PikeFinder([compiled_loader])

    # Loading compiled module
    loader = finder.find_module('compile_test.app')
    module = loader.load_module('compile_test.app')

    if six.PY3:
        assert type(module.__loader__).__name__ == 'SourcelessFileLoader'
        assert module.__cached__.endswith('.pyc')
    else:
        assert module.__file__.endswith('app.pyc')


def test_loading_py(compiled_loader):
    finder = PikeFinder([compiled_loader])

    # Loading module source
    loader = finder.find_module('compile_test')
    module = loader.load_module('compile_test')

    if six.PY3:
        assert type(module.__loader__).__name__ == 'SourceFileLoader'
    else:
        assert module.__file__.endswith('__init__.py')
