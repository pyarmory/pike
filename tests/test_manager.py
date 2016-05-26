import os
import sys
import textwrap

from pike.manager import PikeManager
from pike.discovery import py
from tests import utils


def finders_in_meta_path():
    return [finder for finder in sys.meta_path
            if type(finder).__name__ == 'PikeFinder']


class TestManager(object):
    def test_manager_with_normal_instantiation(self):
        mgr = PikeManager(['./'])
        assert mgr.module_finder in sys.meta_path

        mgr.cleanup()
        assert mgr.module_finder not in sys.meta_path

    def test_manager_as_context_manager(self):
        mgr = PikeManager(['./'])
        with mgr:
            assert mgr.module_finder in sys.meta_path
        assert mgr.module_finder not in sys.meta_path

    def test_double_add_meta_path(self):
        with PikeManager(['./']) as mgr:
            mgr.add_to_meta_path()
            assert len(finders_in_meta_path()) == 1

    def test_del_removes_from_meta_path(self):
        mgr = PikeManager(['./'])
        assert mgr.module_finder in sys.meta_path

        mgr.__del__()
        assert len(finders_in_meta_path()) == 0

    def test_double_cleanup_shouldnt_fail(self):
        """Making sure multiple cleanups don't cause problems

        This case happens when Python's GC calls the destructor on the manager
        """
        mgr = PikeManager(['./'])
        mgr.cleanup()
        mgr.cleanup()
        assert mgr.module_finder not in sys.meta_path

    def test_get_classes(self):
        temp_folder = utils.make_tmpdir()
        pkg_name = 'pike_mgr_classes'
        pkg_location = utils.create_working_package(temp_folder, pkg_name)

        test_file_content = textwrap.dedent("""
        class SampleObj(object):
            pass

        class OtherObj(SampleObj):
            pass
        """)

        mod_location = os.path.join(pkg_location, 'app.py')
        utils.write_file(mod_location, test_file_content)

        # Include module directly on the search path
        second_file = textwrap.dedent("""
        class AnotherObj(object):
            pass
        """)
        mod_location = os.path.join(temp_folder, 'more.py')
        utils.write_file(mod_location, second_file)

        classes = []
        with PikeManager([temp_folder]) as mgr:
            classes = mgr.get_classes()

        assert len(classes) == 3

    def test_get_classes_with_fixtures(self, pike_tmp_package):
        """Structurally the same than test_get_classes, but with fixtures
           (see conftest.py)
        """
        classes = []
        with PikeManager([str(pike_tmp_package)]) as mgr:
            classes = mgr.get_classes()

        assert len(classes) == 3

    def test_get_inherited_classes(self):
        temp_folder = utils.make_tmpdir()
        pkg_name = 'pike_mgr_inherited_classes'
        pkg_location = utils.create_working_package(temp_folder, pkg_name)

        test_file_content = textwrap.dedent("""
        class SampleObj(object):
            pass

        class OtherObj(SampleObj):
            pass
        """)

        mod_location = os.path.join(pkg_location, 'app.py')
        utils.write_file(mod_location, test_file_content)

        # Include module directly on the search path
        second_file = textwrap.dedent("""
        class AnotherObj(object):
            pass
        """)
        mod_location = os.path.join(temp_folder, 'more.py')
        utils.write_file(mod_location, second_file)

        classes = []
        with PikeManager([temp_folder]) as mgr:
            app = py.get_module_by_name('{}.app'.format(pkg_name))
            classes = mgr.get_all_inherited_classes(app.SampleObj)

        assert len(classes) == 1

    def test_get_inherited_classes_with_fixtures(self, pike_tmp_package):
        """Structurally the same than test_get_inherited_classes, but with fixtures
           (see conftest.py)
        """
        # Actually, this is not really needed.
        pkg_name = 'pike_mgr_inherited_classes'
        pike_tmp_package.rename(pike_tmp_package.dirpath() / pkg_name)
        classes = []
        with PikeManager([pike_tmp_package.dirname]) as mgr:
            app = py.get_module_by_name('{}.app'.format(pkg_name))
            classes = mgr.get_all_inherited_classes(app.SampleObj)

        assert len(classes) == 1
