import os


def test_module_name_to_filename(pike_finder):
    res = pike_finder.module_name_to_filename('pike.finder')
    assert res == 'pike{0}finder'.format(os.path.sep)


def test_get_import_filename_module(pike_finder):
    filename = pike_finder.module_name_to_filename('tests.test_finder')
    module_path = pike_finder.get_import_filename(filename)
    assert module_path == __file__


def test_get_import_filename_package(pike_finder):
    filename = pike_finder.module_name_to_filename('tests')
    module_path = pike_finder.get_import_filename(filename)

    assert module_path.endswith('tests{0}__init__.py'.format(os.path.sep))


def test_no_loader_returned_if_module_not_in_scope(pike_finder):
    loader = pike_finder.find_module('bam')
    assert not loader
