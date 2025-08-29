import math
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def sign(n):
    if n == 0:
        return 1
    return n/abs(n)


def hexagonCornersNormalized(center_x, center_y, size, screen_size):
    corners = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = (center_x + (size * math.cos(angle_rad))) / screen_size[0]
        y = (center_y + (size * math.sin(angle_rad))) / screen_size[1]
        corners.append((x, y))
    return corners