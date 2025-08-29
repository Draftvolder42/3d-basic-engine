import numpy as np

class RenderConstants:
    DEFAULT_TEX_COORDS = np.array([
        0.0, 1.0,  # верхний левый
        1.0, 1.0,  # верхний правый
        1.0, 0.0,  # нижний правый
        0.0, 0.0   # нижний левый
    ], dtype=np.float32)


    DEFAULT_INDICES = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)