import random
import time

import simple_draw as sd
from win32api import GetSystemMetrics

import fractal_tree_draw as fd
import transform_decart_ang as tda


class Screen:
    """Keeps list of all screen objects and resolution"""

    def __init__(self, x_size=800, y_size=600):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        print(f"Screen resolution = {width} x {height}")
        self.x_resolution = x_size if x_size < width else width
        self.y_resolution = y_size if y_size < height else height
        self.mobile_objects = []
        self.static_objects = []
        # self.contacting_items = {}
        sd.resolution = (self.x_resolution, self.y_resolution)
        # self.draw_screen_background()
        sd.take_background()

    def draw_screen_background(self):
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.3),
                                     int(self.y_resolution * 0.9)),
                        200, 275, 40, 0.6, )
        fd.fractal_tree(sd.get_point(int(self.x_resolution * 0.8),
                                     int(self.y_resolution * 0.1)),
                        150, 120, 30, 0.65, sd.COLOR_DARK_ORANGE)

    def add_mobile_item(self, mov_item):
        if isinstance(mov_item, MobileObject):
            self.mobile_objects.append(mov_item)

    def remove_mobile_item(self, mov_item):
        if isinstance(mov_item, MobileObject):
            itemName = id(mov_item)
            self.mobile_objects.remove(mov_item)
            print(f'Mobile item {itemName} removed')

    def add_stationary_item(self, stat_item):
        if isinstance(stat_item, ScreenObject) and not isinstance(stat_item, MobileObject):
            self.static_objects.append(stat_item)

    def move_mobile_items(self):
        for dinObj in self.mobile_objects:
            dinObj.make_movement()

    def export_mobile_items(self):
        headLine = "Xpos, Ypos, Xref, Yref, Xsize, Ysize, Speed Value, Speed Direction, Was Contact,"
        logTimeTuple = time.localtime(time.time())
        logTimeStr = f"{logTimeTuple.tm_year}-{logTimeTuple.tm_mon:}-{logTimeTuple.tm_mday} {logTimeTuple.tm_hour}-" \
                     f"{logTimeTuple.tm_min}-{logTimeTuple.tm_sec}"
        logFileName = f"balls log {logTimeStr}.csv"
        print(logFileName)
        try:
            logFile = open(logFileName, 'w')
            logFile.write(headLine + '\n')
            for dinObj in self.mobile_objects:
                data = dinObj.export_data()
                logFile.write(data + '\n')

        except OSError as errorMessage:
            print(errorMessage)
        finally:
            logFile.close()
            print(f"log file {logFileName} is closed")

    def manage_mobile_items_collisions(self):
        def mobObjectChangeSpeed(item: MobileObject, normalVector):
            [speedValue, direction] = item.get_speed()
            direction = tda.reflectance_angle(normalToSurface=normalVector, angle=direction)
            item.set_contact()
            item.set_speed(value=speedValue, direction=direction)

        def mobObjectDispersion(item: MobileObject, normalVector):
            [speedValue, direction] = item.get_speed()
            item.set_speed(value=speedValue, direction=normalVector)

        for statObj in self.static_objects:
            for mobObj in self.mobile_objects:
                [isContact, normalVector] = mobObj.check_contact(statObj)
                if isContact:
                    if mobObj.was_contact() == 0:
                        mobObjectChangeSpeed(item=mobObj, normalVector=normalVector)
                        mobObj.set_contact()
                        if mobObj.is_to_remove_now():
                            mobObj.ball_init(x_resolution, y_resolution)
                        if statObj.is_to_remove_now():
                            statObj.block_init(x_resolution, y_resolution)
                else:
                    mobObj.lost_contact()
                if mobObj.was_contact() > 2:
                    mobObjectDispersion(mobObj, normalVector)
                    # mobObjectChangeSpeed(item=mobObj, normalVector=normalVector)
                if mobObj.is_inside(statObj):
                    mobObj.ball_reset_position(x_resolution, y_resolution)
        for i in range(0, len(self.mobile_objects) - 1):
            for j in range(i + 1, len(self.mobile_objects)):
                mobObj1 = self.mobile_objects[i]
                mobObj2 = self.mobile_objects[j]
                [isContact, normalVector] = mobObj1.check_contact(mobObj2)
                if isContact:
                    if mobObj1.was_contact() == 0:
                        mobObjectChangeSpeed(item=mobObj1, normalVector=normalVector)
                        mobObj1.set_contact()
                        if mobObj1.is_to_remove_now():
                            mobObj1.ball_init(x_resolution, y_resolution)
                    if mobObj2.was_contact() == 0:
                        mobObjectChangeSpeed(item=mobObj2, normalVector=normalVector)
                        mobObj2.set_contact()
                        if mobObj2.is_to_remove_now():
                            mobObj2.ball_init(x_resolution, y_resolution)
                else:
                    mobObj1.lost_contact()
                    mobObj2.lost_contact()
                if mobObj1.was_contact() > 1:
                    mobObjectDispersion(mobObj1, normalVector + 90)
                if mobObj2.was_contact() > 1:
                    mobObjectDispersion(mobObj2, normalVector + 270)

        return

    def draw_items(self):
        sd.start_drawing()  # removes  blinking
        for statObj in self.static_objects:
            statObj.draw_item()
        for dinObj in self.mobile_objects:
            dinObj.draw_item()
        sd.finish_drawing()  # removes  blinking
        sd.sleep(0.08)
        sd.draw_background()

    # def __del__(self):
    #     pass

    def do(self):
        self.draw_items()
        self.manage_mobile_items_collisions()
        self.move_mobile_items()
        [cursorPos, mouseState] = sd.get_mouse_state()
        if mouseState[2] != 0:
            self.export_mobile_items()

    def screen_init(self, balls=3, blocks=1, wallWidth=3):
        x_resolution = self.x_resolution
        y_resolution = self.y_resolution
        wallBlocks = [[(0, 0), (wallWidth, y_resolution - 1)],
                      [(wallWidth, 0), (x_resolution - wallWidth, wallWidth)],
                      [(x_resolution - 1 - wallWidth, 0), (x_resolution - 1, y_resolution - 1)],
                      [(wallWidth, y_resolution - 1 - wallWidth), (x_resolution - wallWidth, y_resolution - 1)]]
        for wall in wallBlocks:
            self.add_stationary_item(Block(wall[0], wall[1]))
            print('wall block', id(wall), 'added')
        while blocks > 0:
            block1 = Block()
            block1.block_init(x_resolution, y_resolution)
            self.add_stationary_item(block1)
            print('block', blocks, 'added')
            blocks -= 1
        while balls > 0:
            ball1 = Ball()
            ball1.ball_init(x_resolution, y_resolution)
            self.add_mobile_item(ball1)
            print('balls', balls, 'added')
            balls -= 1

    def stat_items_issue(self, ignore=None):
        for item in self.static_objects:
            if not item is ignore:
                yield item


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
        self.isRemovable = False
        self.tillRemove = 10
        return

    def draw_item(self):
        pass

    def export_data(self):
        pass

    def import_data(self):
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
        point1 = [self.xPosition - self.xRelation, self.yPosition - self.yRelation]
        point2 = [point1[0] + self.xDimension, point1[1] + self.yDimension]
        return point1, point2

    def set_color(self, color=sd.COLOR_YELLOW):
        if color:
            self.color = color

    def set_width(self, width=None):
        if width:
            self.width = width

    def screen_object_init(self, x0=0, y0=0, x_lim=200, y_lim=200):
        palette = [sd.COLOR_YELLOW,
                   sd.COLOR_PURPLE,
                   sd.COLOR_CYAN,
                   sd.COLOR_GREEN]
        color_count = len(palette) - 1
        color = palette[random.randint(0, color_count)]
        x = random.randint(x0, x_lim)
        y = random.randint(y0, y_lim)
        self.xPosition = x
        self.yPosition = y
        self.color = color
        self.width = 2

    def is_inside(self, screenItem):
        x_own, y_own = self.get_position()
        (x1, y1), (x2, y2) = screenItem.get_limits()
        return (x1 < x_own < x2) and (y1 < y_own < y2)

    def is_removable(self):
        return self.isRemovable

    def is_to_remove_now(self):
        if self.isRemovable:
            if self.tillRemove < 10:
                self.set_color(sd.COLOR_RED)
                self.set_width(3)
                if type(self) is Ball:
                    self.set_radius(int(0.9 * self.get_radius()))
                    self.set_width(int(0.1 * self.get_radius()))
            if self.tillRemove < 1:
                return True
            else:
                self.tillRemove -= 1
                if self.tillRemove <= 1:
                    return True
        return False

    def set_lifetime(self, x=10):
        self.isRemovable = True
        self.tillRemove = x


class MobileObject(ScreenObject):
    """changes its coordinates, checks collision
    draws itself"""

    def __init__(self, reference: list, relation: list, dimensions: list):
        super().__init__(reference, relation, dimensions)
        self.speedValue = 0
        self.speedDirection = 0
        self.wasContactBefore = 0

    def get_speed(self) -> (int, int):
        return self.speedValue, self.speedDirection

    def set_speed(self, value: int = 0, direction: int = 0):
        self.speedValue = value if value > 0 else 0
        self.speedDirection = direction if value > 0 else 0

    def was_contact(self) -> int:
        return self.wasContactBefore

    def set_contact(self):
        self.wasContactBefore += 1

    def export_data(self) -> str:
        export = f" {self.xPosition}, {self.yPosition}, {self.xRelation}, {self.yRelation}," \
                 f" {self.xDimension}, {self.yDimension}, {self.speedValue}, {self.speedDirection}," \
                 f" {self.wasContactBefore}"
        return export

    def import_data(self, data: str):
        pass

    def lost_contact(self):
        if self.wasContactBefore > 0:
            self.wasContactBefore -= 1
        if self.wasContactBefore < 0:
            self.wasContactBefore = 0

    def check_contact(self, opponent: ScreenObject) -> [bool, int]:
        def check_ball_block_contact(ball: Ball, block: Block) -> [bool, int]:
            def check_ball_vertex_contact(centre, vertex, radius) -> bool:
                [x, y] = tda.vectorize(point1=centre, point2=vertex)
                distance = int(tda.vector_length(x=x, y=y))
                return not (distance > radius)

            def check_ball_edge_contact(centre, radius, linePoint1, linePoint2):
                distance = abs(tda.distance_point_line(point=centre, linePoint1=linePoint1, linePoint2=linePoint2))
                return not (distance > radius)

            contactDetected = False
            normalToSurface = 0
            [referencePoint, oppositePoint] = block.get_limits()
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
                                                              linePoint1=blockVertex[1],
                                                              linePoint2=blockVertex[0]))
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
                    [x, y] = tda.vectorize(point1=blockVertex[1], point2=blockVertex[2])
                    normalToSurface = tda.vector_angle(x=x, y=y)
                    return [True, normalToSurface]
            else:
                for point in blockVertex:
                    if check_ball_vertex_contact(centre=center, vertex=point, radius=ballRadius):
                        [x, y] = tda.vectorize(point1=center, point2=point)
                        normalToSurface = 90 + tda.vector_angle(x=x, y=y)
                        return [True, normalToSurface]
            return [contactDetected, normalToSurface]

        def check_ball_ball_contact(ball1: Ball, ball2: Ball) -> [bool, int]:
            contactDistance = ball1.xRelation + ball2.xRelation  # xRelation is radius
            [x, y] = tda.vectorize(point1=ball1.get_position(), point2=ball2.get_position())
            ballDistance = tda.vector_length(x, y)
            if not ballDistance > contactDistance:
                return [True, 90 + tda.vector_angle(x, y)]
            return [False, 0]

        if isinstance(self, Ball) and not self.wasContactBefore:
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

    def mobile_object_init(self):
        speed_limit = (int(window.x_resolution * 0.005), int(window.x_resolution * 0.008))
        speed_value = random.randint(*speed_limit)  # star before list unpacks the arguments
        speed_direction = random.randint(0, 360)
        self.speedDirection = speed_direction
        self.speedValue = speed_value
        return


class Block(ScreenObject):
    """ rectangular static blocks """

    def __init__(self, reference=[0, 0], dimensions=[1, 1]):
        relation = [0, 0]
        super().__init__(reference, relation, dimensions)
        self.init_points()
        return

    def draw_item(self):
        sd.rectangle(left_bottom=self.referencePoint, right_top=self.oppositePoint, color=self.color,
                     width=self.width)

    def init_points(self):
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        self.oppositePoint = sd.get_point(x=self.xPosition + self.xDimension, y=self.yPosition + self.yDimension)

    def block_init(self, x_lim=200, y_lim=200):
        wall_thickness = 5
        x_size = random.randint(int(x_lim * 0.05), int(x_lim * 0.3))
        y_size = random.randint(int(y_lim * 0.05), int(y_lim * 0.3))
        x0 = wall_thickness
        x_max = x_lim - x_size - wall_thickness
        y0 = x0
        y_max = y_lim - y_size - wall_thickness
        self.set_lifetime(random.randint(10, 100))
        intersected = True
        self.xDimension = x_size
        self.yDimension = y_size
        i = 0
        self.screen_object_init(x0=x0, y0=y0, x_lim=x_max, y_lim=y_max)
        # while intersected:
        #     i += 1
        #     j = 0
        #     self.screen_object_init(x0=x0, y0=y0, x_lim=x_max, y_lim=y_max)
        #
        #     for item in window.static_objects:
        #         j += 1
        #         if id(self) != id(item):
        #             print('iteration ', i, j, intersected)
        #             intersected = intersected or item.is_inside(self)
        self.init_points()


class Ball(MobileObject):
    """ mobile balls with radius """

    def __init__(self, reference=[0, 0], radius=1):
        relation = [radius, radius]
        dimensions = [radius * 2, radius * 2]
        super().__init__(reference, relation, dimensions)
        return

    def draw_item(self):
        self.referencePoint = sd.get_point(x=self.xPosition, y=self.yPosition)
        if self.wasContactBefore > 0:
            color = sd.COLOR_RED
            width = 5
        else:
            color = self.color
            width = self.width
        sd.circle(center_position=self.referencePoint, radius=self.xRelation, color=color, width=width)
        return

    def get_radius(self):
        return self.xRelation

    def ball_init(self, x_lim, y_lim):
        ''' define start position, speed and radius for bubble in window '''
        radius_limit = (16, 50)
        radius = random.randint(*radius_limit)
        self.mobile_object_init()
        self.set_radius(radius)
        self.ball_reset_position(x_lim, y_lim)
        self.set_lifetime(random.randint(20, 50))

    def set_radius(self, radius):
        self.xRelation = radius
        self.yRelation = radius
        self.xDimension = radius * 2
        self.yDimension = self.xDimension

    def ball_reset_position(self, x_lim, y_lim):
        wall_thickness = 5
        x0 = self.xRelation + self.speedValue + wall_thickness
        x_max = x_lim - self.xRelation - self.speedValue - wall_thickness
        y0 = x0
        y_max = y_lim - self.xRelation - self.speedValue - wall_thickness
        self.screen_object_init(x0=x0, y0=y0, x_lim=x_max, y_lim=y_max)
        return


# =================================================================================


# =====================================================================================

x_resolution, y_resolution = 1600, 950

window = Screen(x_size=x_resolution, y_size=y_resolution)
window.screen_init(balls=48, blocks=6, wallWidth=4)

while not sd.user_want_exit():
    window.do()

sd.quit()
