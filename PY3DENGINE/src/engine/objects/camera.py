from abc import ABC, abstractmethod


class Camera(ABC):
    @abstractmethod
    def get_vector(self):
        pass

    def set_vector(self, vector):
        self.vector = vector


class Camera3D(Camera):
    def __init__(self, vector: list[float]) -> None:
        self.vector = vector

    def get_vector(self):
        return self.vector
    
    def set_vector(self, vector):
        self.vector = vector