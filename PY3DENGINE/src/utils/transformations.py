import numpy as np
import math as m
cos = m.cos
sin = m.sin


def rad2deg(a):
    return a * ( m.pi / 180)


def rotate_x(d):
    a = rad2deg(d)
    return np.array([
    [1, 0, 0],
    [0, cos(a), -sin(a)],
    [0, sin(a),  cos(a)]
    ])


def rotate_y(d):
    a = rad2deg(d)
    return np.array([
    [cos(a), 0, sin(a)],
    [0, 1, 0],
    [-sin(a), 0, cos(a)]
    ])
    

def rotate_z(d):
    a = rad2deg(d)
    return np.array([
    [cos(a), -sin(a), 0],
    [sin(a), cos(a), 0],
    [0, 0, 1]
    ])


def scaling(sx, sy, sz):
    return np.array([
        [sx,  0,  0],
        [ 0, sy,  0],
        [ 0,  0, sz]
    ])