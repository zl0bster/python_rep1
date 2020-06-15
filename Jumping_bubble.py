# -*- coding: utf-8 -*-
#
# draws bubble in the middle of screen
# and redraws it jumping
#
# pip install simple_draw
#
import random

import simple_draw as sd


def draw_bubble(bub_center, bub_radius=20, bub_color=sd.COLOR_YELLOW):
    ''' draws the bubble '''
    for _ in range(2):
        sd.circle(center_position=bub_center, radius=bub_radius, width=2, color=bub_color)
        bub_radius -= 5


def show_bubble(bub_center, bub_radius=20):
    ''' draws the bubble then removes it by background color'''
    draw_bubble(bub_center=bub_center, bub_radius=bub_radius)
    sd.sleep(0.05)
    draw_bubble(bub_center=bub_center, bub_radius=bub_radius, bub_color=sd.background_color)


def show_bubbles_cloud(b_cloud=[]):
    if not b_cloud:
        return
    for bubble in b_cloud:
        point = sd.get_point(bubble['x'], bubble['y'])
        draw_bubble(point, bubble['r'])
    sd.sleep(0.05)
    # sd.clear_screen()
    for bubble in b_cloud:
        point = sd.get_point(bubble['x'], bubble['y'])
        draw_bubble(point, bubble['r'], bub_color=sd.background_color)
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


def bubble_init(x_lim, y_lim):
    ''' define start position, speed and radius for bubble in window'''
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
                'r': radius}
    return bub_data


''' initialize screen and bubbles 
    start the main program'''
x_resolution, y_resolution = 1200, 700
sd.resolution = (x_resolution, y_resolution)

bubble_data = {'x': 0,
               'y': 0,
               'x_speed': 0,
               'y_speed': 0,
               'r': 0}
bubbles_cloud = []
bubbles_count = 30

# bubbles data creation
for i in range(0, bubbles_count):
    bubbles_cloud.append(bubble_init(x_resolution, y_resolution))

collision_direction = [False, False]
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

# sd.pause()
