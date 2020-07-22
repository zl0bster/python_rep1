import simple_draw as sd
from win32api import GetSystemMetrics
import fractal_tree_draw as fd
import transform_decart_ang as da_trans


class Screen:
    """Keeps list of all screen objects and resolution"""

    def __init__(self, x_size=800, y_size=600):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        print(f"Screen resolution = {width} x {height}")
        self.x_resolution = x_size if x_size < width else width
        self.y_resolution = y_size if y_size < height else height
        self.mobile_objects_count = 0
        self.static_objects_count = 0
        self.mobile_objects = []
        self.static_objects = []
        sd.resolution = (self.x_resolution, self.y_resolution)
        self.draw_screen_background()
        sd.take_background()
        return

    def draw_screen_background(self):
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.4),
                                     int(self.y_resolution * 0.25)),
                        200, 275, 40, 0.6, )
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.6),
                                     int(self.y_resolution * 0.3)),
                        150, 120, 30, 0.65, sd.COLOR_DARK_ORANGE)
        return

    def add_mobile_item(self, mov_item):
        if isinstance(mov_item, MobileObject):
            self.mobile_objects_count += 1
            self.mobile_objects.append(mov_item)
            return self.mobile_objects_count
        return None

    def add_stationary_item(self, stat_item):
        if isinstance(stat_item, ScreenObject) and not isinstance(stat_item, MobileObject):
            self.static_objects_count += 1
            self.static_objects.append(stat_item)
            return self.static_objects_count
        return None

    def move_mobile_items(self):
        for dinObj in self.mobile_objects:
            result = dinObj.make_movement
        return

    def manage_mobile_items_collisions(self):
        # TODO check contact of all mobile items with mobile and static items
        pass

    def draw_items(self):
        sd.take_background()
        sd.start_drawing()  # removes  blinking
        for statObj in self.static_objects:
            result = statObj.draw_item
        for dinObj in self.mobile_objects:
            result = dinObj.draw_item
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

    def set_color(self, color=None):
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

    def get_speed(self):
        return self.speedValue, self.speedDirection

    def set_speed(self, value: int = 0, direction: int = 0):
        self.speedValue = value if value > 0 else 0
        self.speedDirection = direction if value > 0 else 0
        return

    def check_contact(self, opponent: ScreenObject):

        def check_ball_block_contact(ball: Ball, block: Block) -> bool:
            def check_ball_vertex_contact(center, vertex, radius) -> bool:
                distance = int(da_trans.vector_length(da_trans.vectorize(point1=center, point2=vertex)))
                if distance > radius:
                    return False
                return True

            def check_ball_edge_contact(center, radius, linePoint1, linePoint2):
                distance = da_trans.distance_point_line(point=center, linePoint1=linePoint1, linePoint2=linePoint2)
                if distance > radius:
                    return False
                return True

            contactDetected = False
            [referencePoint, oppositePoint] = opponent.get_limits()
            center = ball.get_position()
            ranges = ball.get_ranges()
            ballRadius = ranges[0]
            blockVertex = [referencePoint,
                           [oppositePoint[0], referencePoint[1]],
                           oppositePoint,
                           referencePoint[0], oppositePoint[1]]
            if referencePoint[0] <= center[0] <= oppositePoint[0]:
                contactDetected = (check_ball_edge_contact(center=center,
                                                           radius=ballRadius,
                                                           linePoint1=blockVertex[3],
                                                           linePoint2=blockVertex[2])
                                   or check_ball_edge_contact(center=center,
                                                              radius=ballRadius,
                                                              linePoint1=blockVertex[0],
                                                              linePoint2=blockVertex[1]))
                if contactDetected:
                    return True
            elif referencePoint[1] <= center[1] <= oppositePoint[1]:
                contactDetected = (check_ball_edge_contact(center=center,
                                                           radius=ballRadius,
                                                           linePoint1=blockVertex[0],
                                                           linePoint2=blockVertex[4])
                                   or check_ball_edge_contact(center=center,
                                                              radius=ballRadius,
                                                              linePoint1=blockVertex[1],
                                                              linePoint2=blockVertex[2]))
                if contactDetected:
                    return True
            else:
                for point in blockVertex:
                    if check_ball_vertex_contact(center=center, vertex=point, radius=ballRadius):
                        return True
            return contactDetected

        def check_ball_ball_contact(ball1: Ball, ball2: Ball) -> bool:
            nearDistance = ball1.xRelation + ball2.xRelation
            # farDistance = nearDistance + ball1.speedValue + ball2.speedValue
            [x, y] = da_trans.vectorize(point1=ball1.get_position(), point2=ball2.get_position())
            ball_distance = da_trans.vector_length(x, y)
            # if farDistance < ball_distance:
            #     return False
            if nearDistance >= ball_distance:
                return True
            return False

        if isinstance(self, Ball):
            if isinstance(opponent, Block):
                return check_ball_block_contact(self, opponent)
            elif isinstance(opponent, Ball):
                return check_ball_ball_contact(self, opponent)
        return False

    def make_movement(self):
        positionRelation = da_trans.angular_to_decart(distance=self.speedValue, angle=self.speedDirection)
        self.xPosition += positionRelation[0]
        self.yPosition += positionRelation[1]
        return


class Block(ScreenObject):
    """ rectangular static blocks """

    def __init__(self, reference: list, dimensions: list):
        relation = [0, 0]
        super().__init__(reference, relation, dimensions)
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        self.oppositePoint = sd.get_point(x=self.xPosition + self.xDimension, y=self.yPosition + self.yDimension)
        return

    def draw_item(self):
        sd.rectangle(left_bottom=self.referencePoint, right_top=self.oppositePoint, color=self.color, width=1)
        return


class Ball(MobileObject):
    """ mobile balls with radius """

    def __init__(self, reference: list, radius: int):
        relation = [radius, radius]
        dimensions = [radius * 2, radius * 2]
        super().__init__(reference, relation, dimensions)
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        return

    def draw_item(self):
        sd.circle(center_position=self.referencePoint, radius=self.xRelation, color=self.color, width=self.width)
        return
