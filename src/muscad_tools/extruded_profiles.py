from enum import StrEnum, auto

from muscad import E, EE, T, Cube, Volume, Cylinder, Part, Sphere, Circle, Square, Text, Polygon, Object, Union

from .helpers import DataTable

class ProfileType(StrEnum):
    b20n6 = auto()

_profile_data = DataTable(
    ["width", "slot width"],{
    ProfileType.b20n6: (20.0, 5.5),
    }
)

def slot_position(i: int, count: int, width: float):
    return (-count/2 + 0.5 + i)*width

class Profile(Part):
    def init(self, profile: ProfileType, length: float, count_x: int|None=None, count_y: int|None=None, count_z: int|None=None):
        v = _profile_data[profile]
        w = v["width"]
        s = v["slot width"]


        if count_x and count_y and not count_z:
            cx = count_x
            cy = count_y
            rotate = None
        elif count_x and not count_y and count_z:
            cx = count_x
            cy = count_z
            rotate = {"x": 90.0}
        elif not count_x and count_y and count_z:
            cx = count_z
            cy = count_y
            rotate = {"y": 90}
        else:
            raise TypeError("exactly 2 of the three count_* must be supplied")


        internal = self.make_internal(w, s, length, cx, cy)
        if rotate:
            internal = internal.rotate(**rotate)
        self.add_child(internal)


    def make_internal(self, w, s, length, count_x, count_y):
        profile = Cube(w*count_x, w*count_y, length)
        slot = Cube(s, s, length+EE)
        slots = Union()
        for y_s in (-1, 1):
            for i_x in range(count_x):
                slots += slot.align(center_x=slot_position(i_x, count_x, w), center_y=count_y*w/2*y_s)
        for x_s in (-1, 1):
            for i_y in range(count_y):
                slots += slot.align(center_y=slot_position(i_y, count_y, w), center_x=count_x*w/2*x_s)
        profile -= slots
        return profile.color("grey")
