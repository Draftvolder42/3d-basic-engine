from abc import ABC, abstractmethod
from PY3DENGINE.src.render.renderable_types.vertices import Vertices
from PY3DENGINE.src.render.renderable_types.faces import Faces
import numpy as np

class ObjectConverter(ABC):
    @abstractmethod
    def convert(self, obj):
        pass


class Convert3DModelToVertices(ObjectConverter):
    def __init__(self, screen_size, camera) -> None:
        self.screen_size = screen_size
        self.camera = camera


    def project_vertices(self, obj):
        camera_vec = np.array(self.camera.vector.get_vertex_data())
        vertices = np.array(obj.get_vertex_data())  
        delta_XYZ = vertices - camera_vec 
  
        z_coords = delta_XYZ[:, 2:3] 
    
        z_coords = np.clip(z_coords, 0.1, None) 

        factors = 1.0 / z_coords 
        vertices_2D = delta_XYZ[:, 0:2]
        projection_vertices = vertices_2D * factors
        aspect_ratio = self.screen_size[0] / self.screen_size[1]
        fov_factor = 1.0  
        normalized_vertices = projection_vertices / np.array([[fov_factor * aspect_ratio, fov_factor]])
        vertices_obj = Vertices()
        vertices_obj.vertices = normalized_vertices
        vertices_obj.size = obj.size
        vertices_obj.color = obj.color
        #print(vertices_obj.vertices)
        return vertices_obj
    
    """
    def convert(self, obj):
        camera_vec = np.array(self.camera.vector.get_vertex_data())
        vertices = np.array(obj.get_vertex_data())
        delta_XYZ = vertices - camera_vec
        distances_to_camera = np.linalg.norm(delta_XYZ, axis=1, keepdims=True)
        #print(vertices, '\n')
        vertices_2D = vertices[0:, 0:2]
        vertices_Z = vertices[0:, 1:3]
        vertices_Z[:, 0:] = vertices_Z[:, 1:]

        factors = 1/ (vertices_Z[:, 0:1]+distances_to_camera)

        #vertices_2D = vertices_2D/self.screen_size
        #print(vertices_2D, "vertices_2D")
        #print(factors, "factors")
        projection_vertices = vertices_2D*factors
        #print(projection_vertices, "projection_vertices")
        normalized_vertices = projection_vertices#/self.screen_size

        #normalized_vertices = projection_vertices
        #print(normalized_vertices)    
        vertices_obj = Vertices()
        vertices_obj.vertices = normalized_vertices
        vertices_obj.size = obj.size
        vertices_obj.color = obj.color
        #print(vertices_obj.vertices)
        return vertices_obj
    """
