import dataclasses
from typing import Literal, Iterable
from enum import StrEnum, auto
import math

from muscad import E, EE, T, Cube, Volume, Cylinder, Part, Sphere, Circle, Square, Text, Polygon, Object, Union

from .helpers import DataTable

class Standard(StrEnum):
    # screws
    din933 = auto() # hex head
    din912 = auto() # internal hex
    din7984 = auto() # internal hex, flat
    din7991 = auto() # internal hex, counter bore
    iso7380 = auto() # flat head internal hex
    iso7380fl = auto() # flat head internal hex with flange

    # nuts
    din934 = auto() # hex nut, normal
    din936 = auto() # hex nut, flat

class Metric(StrEnum):
    m3 = auto()
    m4 = auto()
    m5 = auto()
    m6 = auto()
    m8 = auto()
    m10 = auto()

_din_912 = DataTable(
    ["head diameter", "head height", "wrench distance"],{
    Metric.m3 : ( 5.5,  3.0, 2.5),
    Metric.m4 : ( 7.0,  4.0, 3.0),
    Metric.m5 : ( 8.5,  5.0, 4.0),
    Metric.m6 : (10.0,  6.0, 5.0),
    Metric.m8 : (13.0,  8.0, 6.0),
    Metric.m10: (16.0, 10.0, 8.0),
})

_din_933 = DataTable(
    ["wrench distance", "head height"], {
    Metric.m3 : ( 5.5, 2.0),
    Metric.m4 : ( 7.0, 2.8),
    Metric.m5 : ( 8.0, 3.5),
    Metric.m6 : ( 10.0, 4.9),
    Metric.m8 : ( 13.0, 5.3),
    Metric.m10: ( 17.0, 6.4),
})

_din_7984 = DataTable(
    ["head diameter", "head height", "wrench distance"],{
    Metric.m3 : ( 5.5, 2.0, 2.0),
    Metric.m4 : ( 7.0, 2.8, 2.5),
    Metric.m5 : ( 8.5, 3.5, 3.0),
    Metric.m6 : (10.0, 4.0, 4.0),
    Metric.m8 : (13.0, 5.0, 5.0),
    Metric.m10: (16.0, 6.0, 7.0),
})

_din_934 = DataTable(
    ["head height", "wrench distance"], {
    Metric.m3 : ( 2.4,  5.5),
    Metric.m4 : ( 3.2,  7.0),
    Metric.m5 : ( 4.0,  8.0),
    Metric.m6 : ( 5.0, 10.0),
    Metric.m8 : ( 6.5, 13.0),
    Metric.m10: ( 8.0, 17.0),
})

_din_7991 = DataTable(
    ["head diameter", "wrench distance"],{
    Metric.m3 : ( 6.0, 2.0),
    Metric.m4 : ( 8.0, 2.5),
    Metric.m5 : (10.0, 3.0),
    Metric.m6 : (12.0, 4.0),
    Metric.m8 : (16.0, 5.0),
    Metric.m10: (20.0, 6.0),
})

""" template
--- = DataTable(
    [---], {
    Metric.m3 : ( ),
    Metric.m4 : ( ),
    Metric.m5 : ( ),
    Metric.m6 : ( ),
    Metric.m8 : ( ),
    Metric.m10: ( ),
})
"""

_diameters = DataTable(
    ["norm diameter"], {
    Metric.m3 : ( 3.0,),
    Metric.m4 : ( 4.0,),
    Metric.m5 : ( 5.0,),
    Metric.m6 : ( 6.0,),
    Metric.m8 : ( 8.0,),
    Metric.m10: (10.0,),
    }
)

class Hex(Part):
    def init(self, h: float, wrench_distance: float, tol=0.0, over_length: float|None=None):
        outer_diameter = wrench_distance / math.cos(math.pi/6)
        self.add_child(Cylinder(h=h, d=outer_diameter+tol, segments=6))
        if over_length:
            self.add_misc(Cylinder(h=over_length+E, d=outer_diameter+tol, segments=6).align(bottom=self.top-E))

class InnerHexBase(Part):
    def init(self, h: float, outer_diameter: float, tol=0.0, over_length: float|None=None):
        head = Cylinder(h=h, d=outer_diameter+tol)
        self.add_child(head)
        if over_length:
            self.add_misc(Cylinder(h=over_length+E, d=outer_diameter+tol).align(bottom=self.top-E))

class CounterBore(Part):
    def init(self, big_diameter: float, small_diameter: float, tol=0.0, over_length: float|None=None):
        head = Cylinder(d2=big_diameter+tol, d=small_diameter+tol, h=(big_diameter-small_diameter)/2)
        self.add_child(head)
        if over_length:
            self.add_misc(Cylinder(h=over_length+E, d=big_diameter+tol).align(bottom=self.top-E))


class Head933(Part):
    def init(self, metric, tol=0.0, over_length: float|None=None):
        v = _din_933[metric]
        self.add_child(Hex(h=v["head height"], wrench_distance=v["wrench distance"], tol=tol, over_length=over_length))

class Head912(Part):
    def init(self, metric, tol=0.0, over_length: float|None=None):
        v = _din_912[metric]
        self.add_child(InnerHexBase(h=v["head height"], outer_diameter=v["head diameter"], tol=tol, over_length=over_length))


class Head7984(Part):
    def init(self, metric, tol=0.0, over_length: float|None=None):
        v = _din_7984[metric]
        self.add_child(InnerHexBase(h=v["head height"], outer_diameter=v["head diameter"], tol=tol, over_length=over_length))

class Head7991(Part):
    def init(self, metric, tol=0.0, over_length: float|None=None):
        v = _din_7991[metric]
        self.add_child(CounterBore(big_diameter=v["head diameter"], small_diameter=_diameters[metric]["norm diameter"], tol=tol, over_length=over_length))



class Nut934(Part):
    def init(self, metric: Metric, tol=0.0, over_length: float|None=None):
        v = _din_934[metric]
        self.add_child(Hex(h=v["head height"], wrench_distance=v["wrench distance"], tol=tol, over_length=over_length))


class Screw(Part):
    def init(self, length: float, metric: Metric, standard: Standard, shrink_diameter: float=0.0, recessed: bool|float=False, head_tol=T, rotation=0.0, over_length: float|None=None):
        if over_length is None:
            over_length = length
        head_params = {"metric": metric, "tol": head_tol, "over_length": over_length}
        if standard == Standard.din933:
            head = Head933(**head_params)
        elif standard == Standard.din912:
            head = Head912(**head_params)
        elif standard == Standard.din7984:
            head = Head7984(**head_params)
        elif standard == Standard.din7991:
            head = Head7991(**head_params)
        else:
            raise NotImplementedError()

        if recessed == True:
            recess = head.height
        elif recessed == False:
            recess = 0.0
        else:
            recess = recessed
        self.add_child(head.align(bottom=-recess).z_rotate(rotation))
        d = _diameters[metric]["norm diameter"]
        self.add_child(Cylinder(d=d-shrink_diameter, h=length+EE).align(top=self.bottom+E))
        self.head_tol = head_tol
        self.metric = metric
        self.end = -length

    def add_nut(self, position: float|None=None, rotation: float=0.0, standard: Standard=Standard.din934, over_length: float|None=None):
        if standard == Standard.din934:
            nut = Nut934(self.metric, tol=self.head_tol, over_length=over_length).z_mirror()
        else:
            raise NotImplementedError()

        if position is None:
            nut_positioned = nut.align(bottom=self.end)
        elif position < 0.0:
            nut_positioned = nut.align(top=self.end-position)
        else:
            nut_positioned = nut.align(top=-position)
        self.add_child(nut_positioned.z_rotate(rotation).align())
        return self


def test_objects():
    result = Union()
    for i_m, metric in enumerate(Metric):
        for i_s, standard in enumerate((
            Standard.din933,
            Standard.din912,
            Standard.din7984,
        )):
            result += Screw(length=10.0, metric=metric, standard=standard, recessed=False).add_nut(3.0).align(center_x=i_m*20.0, center_y=i_s*20.0)
    return result
