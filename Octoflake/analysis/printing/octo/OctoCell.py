from enum import Enum



def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls



@auto_str
class Foo(object):
    def __init__(self, value_1, value_2):
        self.attribute_1 = value_1
        self.attribute_2 = value_2



@auto_str
class OctoCell:

    def __init__(self,
                 is_pyramid=False,
                 crops = None,
                 is_solid=False,
                 trims=None,
                 weld_up=False,
                 weld_down=False,
                 point_up=False,
                 point_down=False
                 ):
        self.is_pyramid = is_pyramid
        self.crops = crops if crops is not None else set()
        self.is_solid = is_solid
        self.trims = trims if trims is not None else set()
        self.weld_up = weld_up
        self.weld_down = weld_down
        self.point_up = point_up
        self.point_down = point_down

    # def __str__(self):
    #     return f"Octahedron({self.trims})"
    #
    # def __repr__(self):
    #     return self.__str__()

class Crop(Enum):
    UP = 1
    DOWN = 2
    SW = 3
    SE = 4
    NE = 5
    NW = 6
    NONE = 7

class Trim(Enum):
    TOP = 1  # Unused
    BOTTOM = 2
    FRONT = 3
    BACK = 4
    LEFT = 5
    RIGHT = 6

    FRONT_LEFT = 7
    FRONT_RIGHT = 8
    BACK_LEFT = 9
    BACK_RIGHT = 10
