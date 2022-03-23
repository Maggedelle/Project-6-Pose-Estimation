import numpy as np
import math


def angle(p1, p2, p3):
    # vector udregning som ikke giver de rigtige tal

    #vector_ab = p1[1] - p2[1], p1[2] - p2[2]
    #vector_bc = p3[1] - p2[1], p3[2] - p2[2]
    #dot_product = (vector_ab[0] * vector_bc[1]) + (vector_ab[1] * vector_bc[0])
    #lenght_ab = np.sqrt(vector_ab[0]**2 + vector_bc[1]**2)
    #lenght_bc = np.sqrt(vector_bc[0]**2 + vector_bc[1]**2)
    # return math.degrees(np.arccos(dot_product/(lenght_ab*lenght_bc)))
    ############################################################

    angel = math.degrees(math.atan2(
        p3[2]-p2[2], p3[1] - p2[1])-math.atan2(p1[2]-p2[2], p1[1]-p2[1]))
    if angel < 0:
        angel += 360
        # if angel >= 360:
        # angel -= 360
    return angel


def devation(x, y):
    return abs((x[1] - y[1]))
