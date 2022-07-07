"""
File: systemd-nspawn.py
Author: Odair M.
Email: odairmario45@gmail.com
Github: https://github.com/odairmario/seren
Description: Systemd-nspawn module
"""

import subprocess as sp
from os import path
import shutil

__author__ = "Odair M."
__copyright__ = "Odair M."
__license__ = "MIT"


class SystemdNspawn(object):

    """SystemdNspawn represent a wrap to call systemd-nspawn."""

    def __init__(self, target_value, **kwargs):
        """constructor of the class

        :param target: mount point

        """
        self.target = target_value
        self.systemd_nspawn = kwargs.get("nspawn_path","systemd-nspawn")
        self.nspawn_arguments = kwargs.get("nspawn_arguments",["-D"])

        # Stdout and Stderr
        self._stderr = None
        self._stdout = None

    @property
    def nspawn_arguments(self):
        """Systemd-nspawn arguments
        :returns: TODO

        """

        return self._nspawn_arguments

    @nspawn_arguments.setter
    def nspawn_arguments(self, arguments:list):
        """Setter for nspawn_arguments, must be a list

        :arguments: TODO
        :returns: TODO

        """

        if type(arguments) is list:
            self._nspawn_arguments = arguments
        else:
            raise ValueError("Arguments is not a list!")

    @property
    def target(self):
        """Target getter
        :returns: target path a string

        """

        return self._target
    @target.setter
    def target(self, target_value):
        """Setter for target atribute

        :target_value: TODO
        :returns: TODO

        """

        if path.isdir(target_value):
            self._target = target_value
        else:
            raise ValueError("Target path %s dosen't exist or not is a directory.",target_value)

    @property
    def systemd_nspawn(self):
        """systemd_nspawn getter
        :returns: TODO

        """

        return self._systemd_nspawn
    @systemd_nspawn.setter
    def systemd_nspawn(self, nspawn):
        """TODO: Docstring for systemd_nspawn.

        :nspawn: TODO
        :returns: TODO

        """

        if shutil.which(nspawn):
            self._systemd_nspawn = nspawn
        else:
            raise Exception("systemd-nspawn not found")



    def __enter__(self):
        """__enter__ method for WITH stament

        :param type: TODO
        :param value: TODO
        :param traceback: TODO
        :returns: TODO

        """

        return self

    # TODO
    def __exit__(self, type, value, traceback):
        """Exit __exit____exi____exit__
        :returns: TODO

        """

    def run(self, *commands):
        """Run a command on namespace container

        :param *commands: TODO
        :returns: TODO

        """
        command = [self.systemd_nspawn,*self.nspawn_arguments,*commands]

        self._stdout = sp.PIPE
        self._stderr = sp.PIPE
        try:
            err = sp.run(command,
                    stdout=self._stdout,
                    stderr=self._stderr,
                    shell=True,
                    check=True,
                    text=True
                    )
        except Exception as e:
            raise e("error code %s",err)
