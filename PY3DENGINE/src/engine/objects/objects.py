from abc import ABC, abstractmethod
import numpy as np

class Object3D(ABC):
    
    @abstractmethod
    def get_vertex_data(self):
        pass

    def transform(self, matrix: list):
        pass


class Vector3D(Object3D):
    def __init__(self, base_coord: list[float], coords: list[float]):
        self.base_vertex = np.array(base_coord)
        self.vertex = np.array(coords)


    def get_vertex_data(self):
        return self.base_vertex+self.vertex


    def transform(self, matrix):
        self.vertex @ matrix


class Model3D(Object3D):
    def __init__(self, base_coord: list[float], triangles: list[list[float]], color: list[float] = [1, 1, 1, 1], size: float = 1):
        self.base_vertex = np.array(base_coord)
        self.triangles = np.array(triangles)
        self.size = size
        self.color = color


    def get_vertex_data(self):
        return self.triangles+self.base_vertex


    def transform(self, matrix):
        self.triangles = self.triangles @ matrix

