"""
File: mount.py
Author: Odair M.
Email: odairmario45@gmail.com
Github: https://github.com/odairmario
Description: Mount module
"""
import ctypes
import ctypes.util
import logging as log
import os
from enum import Enum

from seren.settings import AUTHOR, COPYRIGHT, LICENSE

__author__ = AUTHOR
__copyright__ = COPYRIGHT
__license__ = LICENSE


class NoValue(Enum):
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class FilesSystemType(NoValue):
    """Filesystem types map.
    This class map filesystem typefor constants like enumeration
    """

    TMPFS = "tmpfs"
    EXT4 = "ext4"
    OVERLAYFS = "overlay"
    PROC = "proc"
    DEV = "devtmpfs"
    SYSFS = "sysfs"
    DEVPTS = "devpts"
    EMPTY = ""


class MountFlags(Enum):
    """Mount flags for the *mount* syscall"""

    MS_RDONLY = 0
    MS_NOSUID = 1
    MS_NODEV = 2
    MS_NOEXEC = 3
    MS_SYNCHRONOUS = 4
    MS_REMOUNT = 5
    MS_MANDLOCK = 6
    MS_DIRSYNC = 7
    MS_NOATIME = 10
    MS_NODIRATIME = 11
    MS_BIND = 4096
    MS_BIND_PRIVATE = 266240
    MS_MOVE = 13
    MS_REC = 14
    MS_SILENT = 15
    MS_POSIXACL = 16
    MS_UNBINDABLE = 17
    MS_PRIVATE = 18
    MS_SLAVE = 19
    MS_SHARED = 20
    MS_RELATIME = 21
    MS_KERNMOUNT = 22
    MS_I_VERSION = 23
    MS_STRICTATIME = 24
    MS_ACTIVE = 30
    MS_NOUSER = 31


def umount(target: str):
    """Ummount filesystem

    :param target: mount point of the file system
    :returns: TODO

    """

    if os.path.ismount(target) is False:
        log.warning("Filesystem %s is not mounted. Nothing to do!", target)

        return False

    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    # ret_code = libc.umount(ctypes.c_char_p(target.encode()))
    ret_code = libc.umount2(ctypes.c_char_p(target.encode()), ctypes.c_ulong(1))

    if ret_code < 0:
        log.error(
            "Error on umount the %s. Error code: %s %s",
            target,
            ret_code,
            ctypes.get_errno(),
        )
        # libc.umount2(ctypes.c_char_p(target.encode()),ctypes.c_ulong(0))
        raise OSError(ctypes.get_errno())

        return False

    if os.path.ismount(target) is True:
        log.error("Filesystem %s still mounted", target)
        # raise Exception("Filesystem still mounted %s",target)

        return False

    return True


class Mount(object):

    """Class to represent mount syscall.
    When instantiate the class mount is do and when is destroyed
    the mount point is umounted.
    """

    def __init__(self, source, target, fs, flag, **data):
        """Call mount syscall and mount the filesystem.
            Mount a filesystem with parameters given, raise error if could not mount
        .

            :param source: source of the filesystem
            :param target: directory that the filesystem will be mounted
            :param fs: filesystem type
            :param flags: list of mount flags
            :param **data: additional data passed for the syscall.

        """
        self._source = source
        self._target = target
        self._fs = fs.value
        self._flag = flag.value
        self._data = ",".join(["{}={}".format(k, v) for k, v in data.items()])

        self._ret_code = None  # define syscall return code to None

        # define libc calls
        self.__libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        self.__libc.mount.argtypes = (
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_ulong,
            ctypes.c_char_p,
        )
        self._ret_code = self.__libc.mount(
            self._source.encode(),
            self._target.encode(),
            self._fs.encode(),
            self._flag,
            self._data.encode(),
        )

        if self._ret_code < 0:
            self._errno = ctypes.get_errno()
            raise OSError(
                self._errno,
                "Error mounting {} ({} on {}) with options {}: {}".format(
                    self._source,
                    self._fs,
                    self._target,
                    self._data,
                    os.strerror(self._errno),
                ),
            )

    def get_target(self):
        """Return the mountpoint where the filesystem are mounted.
        :returns: string

        """

        if os.path.ismount(self._target):
            return self._target
        else:
            return ""

    def __del__(self):
        """Destroy object, umount fs
        :returns: TODO

        """
        umount(self._target)

    def __enter__(self, type, value, traceback):
        """__enter method for WiTH stament
        :returns: TODO

        """

        return self

    def __exit__(self):
        """Exit stament__exit____exit__x
        :returns: TODO

        """
        pass
        # umount(self._target)


class OverlayFs(Mount):

    """Mount overlayfs system"""

    __SOURCE = "overlay"

    def __init__(
        self, base_dir: str, work_dir: str, upperdir: str, target: str, *lowers_dir
    ):
        """Mount a overlayfs filesystem

        mount -t overlay overlay -o lowerdir=l2:l1,upperdir=upper,workdir=workdir merged
        :param base_dir: TODO
        :param work_dir: TODO
        :param upperdir: TODO
        :param target: TODO
        :param *lowers_dir: TODO

        """
        self._base_dir = base_dir
        self._work_dir = work_dir
        self._upperdir = upperdir
        self._target = target
        self._lowers = lowers_dir
        data = {
            "lowerdir": ":".join([*self._lowers, self._base_dir]),
            "workdir": self._work_dir,
            "upperdir": self._upperdir,
        }
        Mount.__init__(
            self,
            self.__SOURCE,
            self._target,
            FilesSystemType.OVERLAYFS,
            MountFlags.MS_ACTIVE,
            **data
        )
