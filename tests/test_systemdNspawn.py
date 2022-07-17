import os

import pytest

from seren.systemdNspawn import SystemdNspawn

__author__ = "Odair M."
__copyright__ = "Odair M."
__license__ = "MIT"


@pytest.fixture
def target(tmp_path) -> str:
    """Return a string to a tmp dir
    :returns: TODO

    """

    return str(tmp_path.absolute())


@pytest.fixture()
def debian_bootstrap():
    """Check if debian_bootstrap is avaliable
    :returns: TODO

    """
    debian_path = os.environ.get("DEBIAN_PATH", False)
    debian_path = os.environ.get(
        "DEBIAN_PATH", "/home/odair/projects/seren/fixtures_data/debian"
    )

    if debian_path:
        return debian_path
    else:
        raise Exception("debian not found")


@pytest.fixture
def archlinux_bootstrap():
    """Check if debian_bootstrap is avaliable
    :returns: TODO

    """
    arch_path = os.environ.get("ARCHLINUX_PATH", False)

    if arch_path:
        return arch_path
    else:
        raise Exception("arch not found")


def test_SystemdNspawn_instance(target):
    """Test whether the class SystemdNspawn can be instancied
    :param tmp_path: fixture to generate a temporary path
    :returns: TODO

    """
    assert SystemdNspawn(target)


def test_SystemdNspawn_target_existence():
    """Test wheter the class SystemdNspawn check if the target exists and is a directory.
    :returns: TODO

    """
    with pytest.raises(ValueError):
        sn = SystemdNspawn("")


def test_SystemdNspawn_alternative_systemd_nspawn(target):
    """Test wheter systemdNspawn class raise value if systemd-nspawn dosent exists

    :target: TODO
    :returns: TODO

    """
    with pytest.raises(Exception):
        sn = SystemdNspawn(target, nspawn_path=target + "/nspawn")

    # test default value
    with SystemdNspawn(target) as sn:
        assert sn.systemd_nspawn == "systemd-nspawn"


def test_SystemdNspawn_WITH_stament(target):
    """Test wheter the class SystemdNspawn can be instancied with WITH stament

    :target: TODO
    :returns: TODO

    """
    with SystemdNspawn(target) as sn:
        assert target == sn.target


def test_SystemdNspawn_nspawn_arguments(target):
    """Test wheter class can be handle diferents arguments

    :target: TODO
    :returns: TODO

    """
    valid_arguments = ["--bind={}".format(target)]
    invalid_arguments = "--bind={}".format(target)
    with SystemdNspawn(target, nspawn_arguments=valid_arguments) as sn:
        assert valid_arguments == sn.nspawn_arguments

    with pytest.raises(ValueError):
        sn = SystemdNspawn(target, nspawn_arguments=invalid_arguments)


@pytest.mark.parametrize(
    "bootstrap, command, expected_return_value, expected_output",
    [
        (
            "debian_bootstrap",
            "ls -a | md5sum",
            0,
            "c4f0ad5e4284f6ec45145036561adf11  -\n",
        ),
        (
            "archlinux_bootstrap",
            "ls -a | md5sum",
            0,
            "d41d8cd98f00b204e9800998ecf8427e  -\n",
        ),
        ("debian_bootstrap", "apt install neovim -y &> /dev/null", 0, ""),
        pytest.param(
            "archlinux_bootstrap", "command_not_found", 1, "", marks=pytest.mark.xfail
        ),
    ],
)
def test_SystemdNspawn_runner(
    bootstrap, command, expected_return_value, expected_output, request
):
    """Test systemd-nspawn run command

    :bootstrap: TODO
    :command: TODO
    :expected_output: TODO
    :returns: TODO

    """
    bootstrap_fixture = request.getfixturevalue(bootstrap)

    with SystemdNspawn(bootstrap_fixture) as sn:
        assert sn.run(command) == expected_return_value
        assert sn.get_last_output() == expected_output
