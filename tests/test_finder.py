import os

from pike.finder import PikeFinder


class TestFinder(object):
    def setup_method(self, method):
        partial_path, _ = os.path.split(__file__)
        finder_path, _ = os.path.split(partial_path)
        self.finder = PikeFinder([finder_path])

    def test_module_name_to_filename(self):
        res = self.finder.module_name_to_filename('pike.finder')
        assert res == 'pike{0}finder'.format(os.path.sep)

    def test_get_import_filename_module(self):
        filename = self.finder.module_name_to_filename('tests.test_finder')
        module_path = self.finder.get_import_filename(filename)

        assert module_path == __file__

    def test_get_import_filename_package(self):
        filename = self.finder.module_name_to_filename('tests')
        module_path = self.finder.get_import_filename(filename)

        assert module_path.endswith('tests{0}__init__.py'.format(os.path.sep))
