from dataclasses import dataclass

@dataclass
class Faces:
    _vertices = any
    color = tuple
    _points_num = int


    @property    
    def vertices(self):
        return self._vertices


    @vertices.setter
    def vertices(self, value):
        self._vertices = value
        self._points_num = len(value)
