import os
from multiprocessing import Queue

import pytest

from seren.mount import BindNameSpace
from seren.mount import FilesSystemType as FS
from seren.mount import Mount
from seren.mount import MountFlags as MFLAGS
from seren.mount import OverlayFs

__author__ = "Odair M."
__copyright__ = "Odair M."
__license__ = "MIT"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("EXT4", "ext4"),
        ("TMPFS", "tmpfs"),
        ("DEVPTS", "devpts"),
        ("OVERLAYFS", "overlay"),
        pytest.param("DEV", "dev", marks=pytest.mark.xfail),
        pytest.param("fat", "", marks=pytest.mark.xfail),
    ],
)
def test_file_system_type(test_input: str, expected: str):
    """Test filesystem type
    This class map filesystem typefor constants like enumeration
    :param test_input: A string that represent test
    :param expected: expected response

    """
    assert FS[test_input].value == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("MS_RDONLY", 0),
        ("MS_BIND", 2**12),
        ("MS_PRIVATE", 18),
        pytest.param("DEV", "dev", marks=pytest.mark.xfail),
        pytest.param("fat", -1, marks=pytest.mark.xfail),
    ],
)
def test_mount_flags(test_input: str, expected: int):
    """Test if the class MountFlags returns corrects values

    :param test_input: enumarate name
    :param expected: int number

    """
    assert MFLAGS[test_input].value == expected


@pytest.fixture
def queue():
    """Return a multiprocessing queue fixture
    :returns: MultiProcessing queue

    """
    q = Queue()
    yield q
    q.close()


def test_mount_targets(tmp_path):
    """Test if the targest mounts is the same

    :param tmp_path: TODO
    :returns: TODO

    """
    source = "/dev/pts"
    target = str(tmp_path.absolute())

    devpts = Mount(source, target, FS.DEV, MFLAGS.MS_BIND)

    assert target == devpts.get_target()


def test_mount_delete(tmp_path):
    """Test umount feature for the class

    :param tmp_path: TODO
    :returns: TODO

    """
    source = "/sys"
    target = str(tmp_path.absolute())
    sysfs = Mount(source, target, FS.SYSFS, MFLAGS.MS_BIND)
    assert os.path.ismount(target)
    del sysfs
    assert os.path.ismount(target) is False


def test_mount_empty_target():
    """TODO: Docstring for test_mount_empty_target.

    :returns: TODO

    """
    with pytest.raises(OSError):
        t = Mount("/proc", "", FS.PROC, MFLAGS.MS_RDONLY)
        del t


def test_overlay(tmp_path_factory):
    """Test overlay class, mount overlayfs and check if is ok

    :param tmp_path_factory: TODO
    :returns: TODO

    """
    base_dir = str(tmp_path_factory.mktemp("base").absolute())
    work_dir = str(tmp_path_factory.mktemp("work").absolute())
    lower_dir = str(tmp_path_factory.mktemp("lower1").absolute())
    upperdir = str(tmp_path_factory.mktemp("upper").absolute())
    target = str(tmp_path_factory.mktemp("target").absolute())

    overlay = OverlayFs(base_dir, work_dir, upperdir, target, lower_dir)

    # time.sleep(60)
    assert os.path.ismount(overlay.get_target())


def test_bind(tmp_path):
    """Test bind directories

    :param tmp_path: TODO
    :returns: TODO

    """
    target = str(tmp_path.absolute())
    mounts = []
    with BindNameSpace(target) as b:
        # check is still mounted

        for i in b.get_mounts():
            print("Mount point {}!".format(i))
            mounts.append(i)
            # assert os.path.ismount(i) is True
            print("------------------------------------------------")

    # check if all filesystem are ummounted


def test_mount_proc(tmp_path):
    """Test if the mount class can bind /proc

    :param tmp_path: fixture for temporary directory

    """
    source = "/proc"
    target = str(tmp_path.absolute())

    proc = Mount(source, target, FS.PROC, MFLAGS.MS_BIND)

    assert os.path.ismount(proc.get_target())
