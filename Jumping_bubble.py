# -*- coding: utf-8 -*-
#
# draws bubble in the middle of screen
# and redraws it jumping
#
# pip install simple_draw
#
import random
import simple_draw as sd


def draw_bubble(bub_center, bub_radius=20):
    for _ in range(2):
        sd.circle(center_position=bub_center, radius=bub_radius, width=2)
        bub_radius -= 5
    sd.sleep(0.05)
    sd.clear_screen()


def collision_detected(position, range, speed, radius):
    x_result, y_result = True, True
    x_distance = (radius + abs(speed[0]))
    y_distance = (radius + abs(speed[1]))
    if x_distance <= position[0] <= (range[0] - x_distance):
        x_result = False
    if y_distance <= position[1] <= (range[1] - y_distance):
        y_result = False
    return (x_result, y_result)


speed_limit = (5, 20)
bubble_radius = 30
x_resolution, y_resolution = 1200, 700
sd.resolution = (x_resolution, y_resolution)

x_speed = random.randint(speed_limit[0], speed_limit[1])
y_speed = random.randint(speed_limit[0], speed_limit[1])
x = x_resolution // 2
y = y_resolution // 2
collision_direction = [False, False]
while 1:
    point = sd.get_point(x, y)
    draw_bubble(point, bubble_radius)
    x += x_speed
    y += y_speed
    collision_direction = collision_detected((x, y), (x_resolution, y_resolution), (x_speed, y_speed), bubble_radius)
    if collision_direction[0]:
        x_speed *= -1
    if collision_direction[1]:
        y_speed *= -1
    if sd.user_want_exit():
        sd.quit()
        break

# sd.pause()
