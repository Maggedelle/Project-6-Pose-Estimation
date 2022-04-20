import numpy as np
import math


def angle(p1, p2, p3):
    angel = math.degrees(math.atan2(
        p3[2]-p2[2], p3[1] - p2[1])-math.atan2(p1[2]-p2[2], p1[1]-p2[1]))
    if angel < 0:
        angel += 360
    return angel


def devation(x, y):
    return abs((x[1] - y[1]))