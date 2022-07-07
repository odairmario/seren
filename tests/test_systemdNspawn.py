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
        sn = SystemdNspawn(target,nspawn_path=target+"/nspawn")

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
    valid_arguments=["--bind={}".format(target)]
    invalid_arguments="--bind={}".format(target)
    with SystemdNspawn(target,nspawn_arguments=valid_arguments) as sn:
        assert valid_arguments == sn.nspawn_arguments

    with pytest.raises(ValueError):
        sn = SystemdNspawn(target,nspawn_arguments=invalid_arguments)
