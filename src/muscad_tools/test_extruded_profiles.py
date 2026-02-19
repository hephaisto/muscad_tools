from pytest import approx

from .extruded_profiles import Profile, ProfileType

def test_profile():
    profile = Profile(profile=ProfileType.b20n6, count_x=2, count_z=3, length=230.0)
    assert profile.width == approx(40.0)
    assert profile.height == approx(60.0)
    assert profile.depth == approx(230.0)
