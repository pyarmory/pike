#
#
#

import pytest
import textwrap


# Default test dir:
PIKE_TEST_DIR = 'pike_tests'


# ------------------------------------------------------------
# Fixtures
#
# See http://pytest.org/latest/tmpdir.html

@pytest.fixture
def pike_init_py(tmpdir):
    """Fixture: Create a directory with an empty __init__.py
       inside a temporary directory

       :param tmpdir: fixture with py.path.local object
       :return: temporary directory path to __init__.py

       HINT: Usually you can find the temporary directory under
             /tmp/pytest-of-$USER/pytest-$NUMBER/$NAME_OF_TEST_FUNCTION/
    """
    pkgdir = tmpdir.mkdir(PIKE_TEST_DIR)
    (pkgdir / "__init__.py").write("")
    return pkgdir


@pytest.fixture
def pike_tmp_package(pike_init_py):
    """Fixture: Create a Python package inside a temporary directory.
       Depends on the pike_init_py fixture

       :param pike_init_py: fixture with py.path.local object pointing to
                            directory with empty __init__.py
       :return: temporary directory path to the package (containing
                __init__.py,  app.py, and more.py)

       HINT: Usually you can find the temporary directory under
             /tmp/pytest-of-$USER/pytest-$NUMBER/$NAME_OF_TEST_FUNCTION/
    """
    # First file:
    (pike_init_py / 'app.py').write(textwrap.dedent("""
        class SampleObj(object):
            pass

        class OtherObj(SampleObj):
            pass
        """))

    # Second file:
    (pike_init_py / 'more.py').write(textwrap.dedent("""
        class AnotherObj(object):
            pass
        """))
    return pike_init_py
