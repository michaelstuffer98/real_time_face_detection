import os
from pathlib import Path

import pytest

from real_time_face_detection.profiles import Profiles, PROFILE_RET


@pytest.fixture
def test_profile_file():
    return Path('tests/test_profiles.json')


def test_profile_manipulations(test_profile_file):
    init_size = os.path.getsize(test_profile_file)
    test_name = 'test_profile'

    profiles = Profiles(test_profile_file)
    r = profiles.add_profile(test_name)
    assert r[0] == PROFILE_RET.OK and r[1] == f"Added profile '{test_name}'"

    r = profiles.add_profile("test_profile")
    assert r[0] == PROFILE_RET.DUPLICATE and r[1] == f"Profile '{test_name}' already exists"

    r = profiles.remove_profile("test_profile")
    assert r[0] is True and r[1] == f"Removed profile '{test_name}'"

    r = profiles.remove_profile("test_profile")
    assert r[0] is True and r[1] == f"Profile '{test_name}' not found"

    assert init_size == os.path.getsize(test_profile_file)


def test_profiles_not_readed(test_profile_file):
    profiles = Profiles(test_profile_file)
    profiles.profiles = None
    test_name = 'test_profile'

    r = profiles.add_profile(test_name)
    assert r == (PROFILE_RET.FAILURE, "Read in the profiles before accessing them")

    r = profiles.remove_profile(test_name)
    assert r == (False, "Read in the profiles before accessing them")
