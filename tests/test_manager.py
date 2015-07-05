import sys

from pike.manager import PikeManager


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
