# -*- coding: utf-8 -*-
#
# draws bubble in the middle of screen
# and redraws it jumping
#
# pip install simple_draw
#
import random

import math

import simple_draw as sd


def draw_bubble(bub_center, bub_radius=20, bub_color=sd.COLOR_YELLOW):
    ''' draws the bubble '''
    for _ in range(2):
        sd.circle(center_position=bub_center, radius=bub_radius, width=2, color=bub_color)
        bub_radius *= 0.85


def show_bubble(bub_center, bub_radius=20):
    ''' draws the bubble then removes it by background color'''
    draw_bubble(bub_center=bub_center, bub_radius=bub_radius)
    sd.sleep(0.05)
    draw_bubble(bub_center=bub_center, bub_radius=bub_radius, bub_color=sd.background_color)


def show_bubbles_cloud(b_cloud=[]):
    ''' draws all bubbles in list then removes them'''
    if not b_cloud:
        return
    sd.take_background()
    sd.start_drawing()  # removes  blinking
    for bubble in b_cloud:
        point = sd.get_point(bubble['x'], bubble['y'])
        draw_bubble(point, bubble['r'], bub_color=bubble['col'])
    sd.finish_drawing()  # removes  blinking
    sd.sleep(0.05)
    sd.draw_background()
    return


def collision_detected1(bubble=[], range=[]):
    ''' checks the collision of bubble with window ranges '''
    x_result, y_result = True, True
    x_distance = (bubble['r'] + abs(bubble['x_speed']))
    y_distance = (bubble['r'] + abs(bubble['y_speed']))
    if x_distance <= bubble['x'] <= (range[0] - x_distance):
        x_result = False
    if y_distance <= bubble['y'] <= (range[1] - y_distance):
        y_result = False
    return (x_result, y_result)


def collision_detected_angular(bubble=[], range=[]):
    ''' checks the collision of bubble with window ranges '''
    x_result, y_result = True, True
    [x_speed, y_speed] = angular_to_decart(bubble['speed_val'], bubble['speed_dir'])
    x_distance = (bubble['r'] + abs(x_speed))
    y_distance = (bubble['r'] + abs(y_speed))
    if x_distance <= bubble['x'] <= (range[0] - x_distance):
        x_result = False
    if y_distance <= bubble['y'] <= (range[1] - y_distance):
        y_result = False
    return (x_result, y_result)


def bubble_init(x_lim, y_lim):
    ''' define start position, speed and radius for bubble in window'''
    palette = [sd.COLOR_YELLOW,
               sd.COLOR_RED,
               sd.COLOR_CYAN,
               sd.COLOR_GREEN]
    color_count = len(palette) - 1
    color = random.randint(0, color_count)
    speed_limit = (5, 20)
    radius_limit = (10, 60)
    x_speed = random.randint(*speed_limit)  # star before list unpacks the arguments
    y_speed = random.randint(*speed_limit)
    radius = random.randint(*radius_limit)
    x = random.randint(radius + speed_limit[1], x_lim - radius - speed_limit[1])
    y = random.randint(radius + speed_limit[1], y_lim - radius - speed_limit[1])
    bub_data = {'x': x,
                'y': y,
                'x_speed': x_speed,
                'y_speed': y_speed,
                'r': radius,
                'col': palette[color]}
    return bub_data


def bubble_init_angular(x_lim, y_lim):
    ''' define start position, speed and radius for bubble in window'''
    palette = [sd.COLOR_YELLOW,
               sd.COLOR_RED,
               sd.COLOR_CYAN,
               sd.COLOR_GREEN]
    color_count = len(palette) - 1
    color = random.randint(0, color_count)
    speed_limit = (5, 20)
    radius_limit = (10, 60)
    speed_value = random.randint(*speed_limit)  # star before list unpacks the arguments
    speed_direction = random.randint(0, 360)
    radius = random.randint(*radius_limit)
    x = random.randint(radius + speed_limit[1], x_lim - radius - speed_limit[1])
    y = random.randint(radius + speed_limit[1], y_lim - radius - speed_limit[1])
    bub_data = {'x': x,
                'y': y,
                'speed_val': speed_value,
                'speed_dir': speed_direction,
                'r': radius,
                'col': palette[color]}
    return bub_data


''' here is the fractal tree module text'''
'''-----------------------------------------'''


#
# pip install simple_draw
#

def draw_branch(point,
                angle,
                length,
                color):
    branch = sd.get_vector(start_point=point, angle=angle, length=length, )
    branch.draw(color=color)
    return branch.end_point


def draw_fork(point,
              angle,
              tilt,
              length,
              color):
    angle1 = angle + tilt
    angle2 = angle - tilt
    vertex1 = draw_branch(point, angle1, length, color)
    vertex2 = draw_branch(point, angle2, length, color)
    return ([vertex1, angle1], [vertex2, angle2])


def fractal_tree(point,
                 length=100,
                 direction=90,
                 tilt=30,
                 scale=0.6,
                 color=sd.COLOR_DARK_GREEN):
    vertexes = draw_fork(point, direction, tilt, length, color)
    while length > 10:
        length *= scale
        for points in vertexes:
            fractal_tree(points[0], length, points[1], tilt, scale, color)
    return


''' here is the angular module text'''
'''-----------------------------------------'''


def angular_to_decart(distance, angle):
    x = distance * sd.cos(angle)
    y = distance * sd.sin(angle)
    return (x, y)


def decart_to_angular(x, y):
    distance = (x * x + y * y) ** 0.5
    angle = math.degrees(math.atan(x / y))
    return (distance, angle)


def vectorize(point1=[], point2=[]):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    return (x, y)


def bounce_angle(normal, angle):
    return (normal + (normal - angle))


''' initialize screen and bubbles 
    start the main program'''
x_resolution, y_resolution = 1200, 700
sd.resolution = (x_resolution, y_resolution)
angular_type = 1

# bubble_data = {'x': 0,
#                'y': 0,
#                'x_speed': 0,
#                'y_speed': 0,
#                'r': 0}
bubbles_cloud = []
bubbles_count = 30
# tree_root = sd.get_point(x_resolution / 2, 100)

fractal_tree(sd.get_point(800, 500), 200, 275, 40, 0.6, )
fractal_tree(sd.get_point(500, 200), 150, 120, 30, 0.65, sd.COLOR_DARK_ORANGE)

# bubbles data creation
if not angular_type:
    for i in range(0, bubbles_count):
        bubbles_cloud.append(bubble_init(x_resolution, y_resolution))
else:
    for i in range(0, bubbles_count):
        bubbles_cloud.append(bubble_init_angular(x_resolution, y_resolution))

collision_direction = [False, False]
if not angular_type:
    while 1:
        show_bubbles_cloud(bubbles_cloud)
        for bubble in bubbles_cloud:
            bubble['x'] += bubble['x_speed']
            bubble['y'] += bubble['y_speed']
            collision_direction = collision_detected1(bubble, (x_resolution, y_resolution))
            if collision_direction[0]:
                bubble['x_speed'] *= -1
            if collision_direction[1]:
                bubble['y_speed'] *= -1
            if sd.user_want_exit():
                sd.quit()
                break
else:
    while 1:
        show_bubbles_cloud(bubbles_cloud)
        for bubble in bubbles_cloud:
            # 'speed_val': speed_value,
            # 'speed_dir': speed_direction,

            [x_speed, y_speed] = angular_to_decart(bubble['speed_val'], bubble['speed_dir'])
            bubble['x'] += x_speed
            bubble['y'] += y_speed
            collision_direction = collision_detected_angular(bubble, (x_resolution, y_resolution))
            if collision_direction[0]:
                bubble['speed_dir'] = bounce_angle(90, bubble['speed_dir'])
            if collision_direction[1]:
                bubble['speed_dir'] = bounce_angle(0, bubble['speed_dir'])
            if sd.user_want_exit():
                sd.quit()
                break
