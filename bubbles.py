import simple_draw as sd
from win32api import GetSystemMetrics
import fractal_tree_draw as fd


class Screen:
    """Keeps list of all screen objects and resolution"""

    def __init__(self, x_size=800, y_size=600):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        print(f"Screen resolution = {width} x {height}")
        self.x_resolution = x_size if x_size < width else width
        self.y_resolution = y_size if y_size < height else height
        self.mobile_objects_count = 0
        self.stationary_object_count = 0
        self.mobile_objects = []
        self.stationary_objects = []
        sd.resolution = (self.x_resolution, self.y_resolution)
        # TODO change tree roots coordinates
        fd.fractal_tree(sd.get_point(800, 500), 200, 275, 40, 0.6, )
        fd.fractal_tree(sd.get_point(500, 200), 150, 120, 30, 0.65, sd.COLOR_DARK_ORANGE)
        #
        sd.take_background()
        return self.x_resolution, self.y_resolution

    def draw_screen_background(self):
        # TODO draw all fractals here
        pass

    def add_mobile_item(self, mov_item):
        # TODO add item to list

        return

    def add_stationary_item(self, stat_item):
        # TODO add item to list

        return

    def draw_items(self):
        sd.take_background()
        sd.start_drawing()  # removes  blinking
        # TODO draw both lists - stationary and mobile items
        sd.finish_drawing()  # removes  blinking
        sd.sleep(0.05)
        sd.draw_background()

    def __del__(self):
        return


class ScreenObject:
    """ Has initial point coordinates
    can be drawn"""

    def __init__(self, reference: list, relation: list, dimensions: list):
        self.xPosition = reference[0]
        self.yPosition = reference[1]
        self.xRelation = relation[0]
        self.yRelation = relation[1]
        self.xDimension = dimensions[0]
        self.yDimension = dimensions[1]
        return

    def draw_item(self):
        pass

    def get_position(self):
        return self.xPosition, self.yPosition

    def get_ranges(self):
        r000degrees = self.xDimension - self.xRelation
        r090degrees = self.yDimension - self.yRelation
        r180degrees = self.xRelation
        r270degrees = self.yRelation
        return r000degrees, r090degrees, r180degrees, r270degrees


class MobileObject(ScreenObject):
    """changes its coordinates, checks collision
    draws itself"""

    def __init__(self, reference: list, relation: list, dimensions: list):
        super().__init__(reference, relation, dimensions)
        self.speedValue = 0
        self.speedDirection = 0
        self.wasContactBefore = False
        return

    def get_speed(self):
        return self.speedValue, self.speedDirection

    def set_speed(self, value=0, direction=0):
        self.speedValue = value if value > 0 else 0
        self.speedDirection = direction if value > 0 else 0
        return

    def check_contact(self, opponent: ScreenObject):
        pass


class Block(ScreenObject):
    #TODO finalize Block class definition, pprovide sides preparation and drawing
    def __init__(self, reference: list,  dimensions: list):
        relation = [0, 0]
        super().__init__(reference, relation, dimensions)


    def draw_item(self):
        referencePoint = sd.get_point(x=self.xPosition, y=yPosition)
        if self.xDimension>0:
        branch = sd.get_vector(start_point=referencePoint, angle=angle, length=length, )
