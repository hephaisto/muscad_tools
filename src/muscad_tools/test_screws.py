from pytest import approx

from .screws import Screw, Standard, Metric

def test_screw():
    screw = Screw(length=10, metric=Metric.m8, standard=Standard.din933, head_tol=0)
    assert max(screw.width, screw.depth) == approx(15.011, rel=1e-3)
