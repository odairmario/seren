"""
File: systemd-nspawn.py
Author: Odair M.
Email: odairmario45@gmail.com
Github: https://github.com/odairmario/seren
Description: Systemd-nspawn module
"""

# from subprocess import Popen

__author__ = "Odair M."
__copyright__ = "Odair M."
__license__ = "MIT"


class SystemdNspawn(object):

    """SystemdNspawn represent a wrap to call systemd-nspawn."""

    def __init__(self, target, **kwargs):
        """constructor of the class

        :param target: mount point

        """
        self._target = target

    def __enter__(self, type, value, traceback):
        """__enter__ method for WITH stament

        :param type: TODO
        :param value: TODO
        :param traceback: TODO
        :returns: TODO

        """

        return self

    # TODO
    def __exit__(self):
        """Exit __exit____exi____exit__
        :returns: TODO

        """

    def run(self, *commands):
        """Run a command on namespace container

        :param *commands: TODO
        :returns: TODO

        """
