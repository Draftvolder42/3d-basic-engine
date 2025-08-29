from abc import ABC, abstractmethod
import numpy as np

class Object3D(ABC):
    
    @abstractmethod
    def get_draw_data(self):
        pass

    def transform(self, matrix: list):
        pass


class Vector3D(Object3D):
    def __init__(self, base_coord: list[float], coords: list[float]):
        self.base_vertex = np.ndarray(base_coord)
        self.vertex = np.ndarray(coords)


    def get_draw_data(self):
        return self.base_vertex+self.vertex


    def transform(self, matrix):
        self.vertex @ matrix
