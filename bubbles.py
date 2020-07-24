import simple_draw as sd
from win32api import GetSystemMetrics
import fractal_tree_draw as fd
import transform_decart_ang as tda
import random


class Screen:
    """Keeps list of all screen objects and resolution"""

    def __init__(self, x_size=800, y_size=600):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        print(f"Screen resolution = {width} x {height}")
        self.x_resolution = x_size if x_size < width else width
        self.y_resolution = y_size if y_size < height else height
        # self.mobile_objects_count = 0
        # self.static_objects_count = 0
        self.mobile_objects = []
        self.static_objects = []
        sd.resolution = (self.x_resolution, self.y_resolution)
        self.draw_screen_background()
        sd.take_background()
        return

    def draw_screen_background(self):
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.3),
                                     int(self.y_resolution * 0.9)),
                        200, 275, 40, 0.6, )
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.8),
                                     int(self.y_resolution * 0.1)),
                        150, 120, 30, 0.65, sd.COLOR_DARK_ORANGE)
        return

    def add_mobile_item(self, mov_item):
        if isinstance(mov_item, MobileObject):
            self.mobile_objects.append(mov_item)
        return None

    def add_stationary_item(self, stat_item):
        if isinstance(stat_item, ScreenObject) and not isinstance(stat_item, MobileObject):
            self.static_objects.append(stat_item)
        return None

    def move_mobile_items(self):
        for dinObj in self.mobile_objects:
            dinObj.make_movement()
        return

    def manage_mobile_items_collisions(self):
        def mobObjectChangeSpeed(item: MobileObject, normalVector):
            [speedValue, direction] = item.get_speed()
            direction = tda.reflectance_angle(normalToSurface=normalVector, angle=direction)
            item.set_contact(b=True)
            item.set_speed(value=speedValue, direction=direction)

        for statObj in self.static_objects:
            for mobObj in self.mobile_objects:
                [isContact, normalVector] = mobObj.check_contact(statObj)
                if isContact:
                    if not mobObj.was_contact():
                        mobObjectChangeSpeed(item=mobObj, normalVector=normalVector)
                        mobObj.set_contact(b=True)
                else:
                    mobObj.set_contact(b=False)
        for i in range(0, len(self.mobile_objects) - 2):
            for j in range(i + 1, len(self.mobile_objects) - 1):
                mobObj1 = self.mobile_objects[i]
                mobObj2 = self.mobile_objects[j]
                [isContact, normalVector] = mobObj1.check_contact(mobObj2)
                if isContact:
                    if not mobObj1.was_contact():
                        mobObjectChangeSpeed(item=mobObj1, normalVector=normalVector)
                        mobObj1.set_contact(b=True)
                    if not mobObj2.was_contact():
                        mobObjectChangeSpeed(item=mobObj2, normalVector=normalVector)
                        mobObj2.set_contact(b=True)
                else:
                    mobObj1.set_contact(b=False)
                    mobObj2.set_contact(b=False)
        return

    def draw_items(self):
        # sd.take_background()
        sd.start_drawing()  # removes  blinking
        for statObj in self.static_objects:
            statObj.draw_item()
        for dinObj in self.mobile_objects:
            dinObj.draw_item()
        sd.finish_drawing()  # removes  blinking
        sd.sleep(0.05)
        sd.draw_background()

    def __del__(self):
        return


class ScreenObject:
    """ Has initial point coordinates, reference of own center and dimensions
    can be drawn with defined color and width"""

    def __init__(self, reference: list, relation: list, dimensions: list):
        self.xPosition = reference[0]
        self.yPosition = reference[1]
        self.xRelation = relation[0]
        self.yRelation = relation[1]
        self.xDimension = dimensions[0]
        self.yDimension = dimensions[1]
        self.color = sd.COLOR_YELLOW
        self.width = 1
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

    def get_limits(self):
        point1 = [self.xPosition, self.yPosition]
        point2 = [self.xPosition + self.xDimension, self.yPosition + self.yDimension]
        return point1, point2

    def set_color(self, color=sd.COLOR_YELLOW):
        if color:
            self.color = color
        return

    def set_width(self, width=None):
        if width:
            self.width = width
        return


class MobileObject(ScreenObject):
    """changes its coordinates, checks collision
    draws itself"""

    def __init__(self, reference: list, relation: list, dimensions: list):
        super().__init__(reference, relation, dimensions)
        self.speedValue = 0
        self.speedDirection = 0
        self.wasContactBefore = False
        return

    def get_speed(self) -> (int, int):
        return self.speedValue, self.speedDirection

    def set_speed(self, value: int = 0, direction: int = 0):
        self.speedValue = value if value > 0 else 0
        self.speedDirection = direction if value > 0 else 0
        return

    def was_contact(self) -> bool:
        return self.wasContactBefore

    def set_contact(self, b: bool):
        self.wasContactBefore = b
        return

    def check_contact(self, opponent: ScreenObject) -> [bool, int]:
        def check_ball_block_contact(ball: Ball, block: Block) -> [bool, int]:
            def check_ball_vertex_contact(centre, vertex, radius) -> bool:
                [x, y] = tda.vectorize(point1=centre, point2=vertex)
                distance = int(tda.vector_length(x=x, y=y))
                return not (distance > radius)

            def check_ball_edge_contact(centre, radius, linePoint1, linePoint2):
                distance = tda.distance_point_line(point=centre, linePoint1=linePoint1, linePoint2=linePoint2)
                return not (distance > radius)

            contactDetected = False
            normalToSurface = 0
            [referencePoint, oppositePoint] = opponent.get_limits()
            center = ball.get_position()
            ranges = ball.get_ranges()
            ballRadius = ranges[0]
            blockVertex = [referencePoint,
                           [oppositePoint[0], referencePoint[1]],
                           oppositePoint,
                           [referencePoint[0], oppositePoint[1]]]
            if referencePoint[0] <= center[0] <= oppositePoint[0]:
                contactDetected = (check_ball_edge_contact(centre=center,
                                                           radius=ballRadius,
                                                           linePoint1=blockVertex[3],
                                                           linePoint2=blockVertex[2])
                                   or check_ball_edge_contact(centre=center,
                                                              radius=ballRadius,
                                                              linePoint1=blockVertex[0],
                                                              linePoint2=blockVertex[1]))
                if contactDetected:
                    [x, y] = tda.vectorize(point1=blockVertex[0], point2=blockVertex[1])
                    normalToSurface = tda.vector_angle(x=x, y=y)
                    return [True, normalToSurface]
            elif referencePoint[1] <= center[1] <= oppositePoint[1]:
                contactDetected = (check_ball_edge_contact(centre=center,
                                                           radius=ballRadius,
                                                           linePoint1=blockVertex[0],
                                                           linePoint2=blockVertex[3])
                                   or check_ball_edge_contact(centre=center,
                                                              radius=ballRadius,
                                                              linePoint1=blockVertex[1],
                                                              linePoint2=blockVertex[2]))
                if contactDetected:
                    [x, y] = tda.vectorize(point1=blockVertex[0], point2=blockVertex[1])
                    normalToSurface = 90 + tda.vector_angle(x=x, y=y)
                    return [True, normalToSurface]
            else:
                for point in blockVertex:
                    if check_ball_vertex_contact(centre=center, vertex=point, radius=ballRadius):
                        [x, y] = tda.vectorize(point1=center, point2=point)
                        normalToSurface = tda.vector_angle(x=x, y=y)
                        return [True, normalToSurface]
            return [contactDetected, normalToSurface]

        def check_ball_ball_contact(ball1: Ball, ball2: Ball) -> [bool, int]:
            nearDistance = ball1.xRelation + ball2.xRelation
            # farDistance = nearDistance + ball1.speedValue + ball2.speedValue
            [x, y] = tda.vectorize(point1=ball1.get_position(), point2=ball2.get_position())
            ball_distance = tda.vector_length(x, y)
            # if farDistance < ball_distance:
            #     return False
            if nearDistance >= ball_distance:
                return [True, tda.vector_angle(x, y)]
            return [False, 0]

        if isinstance(self, Ball):
            if isinstance(opponent, Block):
                return check_ball_block_contact(self, opponent)
            elif isinstance(opponent, Ball):
                return check_ball_ball_contact(self, opponent)
        return [False, 0]

    def make_movement(self):
        [x, y] = tda.angular_to_decart(distance=self.speedValue, angle=self.speedDirection)
        self.xPosition += x
        self.yPosition += y
        return

    # def draw_item(self):
    #     # super().draw_item()
    #     pass


class Block(ScreenObject):
    """ rectangular static blocks """

    def __init__(self, reference: list, dimensions: list):
        relation = [0, 0]
        super().__init__(reference, relation, dimensions)
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        self.oppositePoint = sd.get_point(x=self.xPosition + self.xDimension, y=self.yPosition + self.yDimension)
        return

    def draw_item(self):
        # super().draw_item()
        sd.rectangle(left_bottom=self.referencePoint, right_top=self.oppositePoint, color=self.color, width=self.width)
        return


class Ball(MobileObject, ScreenObject):
    """ mobile balls with radius """

    def __init__(self, reference: list, radius: int):
        relation = [radius, radius]
        dimensions = [radius * 2, radius * 2]
        super().__init__(reference, relation, dimensions)
        return

    def draw_item(self):
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        if self.wasContactBefore:
            color = sd.COLOR_RED
        else:
            color = self.color
        sd.circle(center_position=self.referencePoint, radius=self.xRelation, color=color, width=self.width)
        return


# =================================================================================
def ball_init(x_lim, y_lim):
    ''' define start position, speed and radius for bubble in window '''
    palette = [sd.COLOR_YELLOW,
               sd.COLOR_PURPLE,
               sd.COLOR_CYAN,
               sd.COLOR_GREEN]
    color_count = len(palette) - 1
    color = palette[random.randint(0, color_count)]
    speed_limit = (5, 10)
    radius_limit = (25, 50)
    speed_value = random.randint(*speed_limit)  # star before list unpacks the arguments
    speed_direction = random.randint(0, 360)
    radius = random.randint(*radius_limit)
    x = random.randint(radius + speed_limit[1], x_lim - radius - speed_limit[1])
    y = random.randint(radius + speed_limit[1], y_lim - radius - speed_limit[1])
    ball_data = ([x, y],
                 [speed_value, speed_direction],
                 radius,
                 color)
    return ball_data


def ball_creation():
    [reference, speed, radius, color] = ball_init(x_resolution, y_resolution)
    ball1 = Ball(reference=reference, radius=radius)
    ball1.set_speed(speed[0], speed[1])
    ball1.set_color(color)
    ball1.set_width(2)
    return ball1


def block_creation():
    [reference, speed, radius, color] = ball_init(x_resolution, y_resolution)
    block1 = Block(reference=reference, dimensions=[int(radius * speed[0]), int(radius * speed[1] / 36)])
    block1.set_color(color)
    block1.set_width(3)
    return block1


# =====================================================================================

x_resolution, y_resolution = 1200, 700
balls_count = 16
blocks_count = 4

window = Screen(x_size=x_resolution, y_size=y_resolution)
window.draw_screen_background()
frame = Block(reference=[1, 1], dimensions=[x_resolution - 2, y_resolution - 2])
frame.set_color(color=sd.COLOR_RED)
frame.set_width(width=2)
window.add_stationary_item(frame)

while balls_count > 0:
    window.add_mobile_item(ball_creation())
    balls_count -= 1

while blocks_count > 0:
    window.add_stationary_item(block_creation())
    blocks_count -= 1

while not sd.user_want_exit():
    window.draw_items()
    window.manage_mobile_items_collisions()
    window.move_mobile_items()

sd.quit()
