import os
import shutil
import tempfile


def make_tmpdir():
    return tempfile.mkdtemp()


def remove_dir(filename):
    if os.path.exists(filename):
        shutil.rmtree(filename)
