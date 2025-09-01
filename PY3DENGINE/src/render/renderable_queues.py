from abc import ABC, abstractmethod

class RenderableQueue(ABC):
    @abstractmethod
    def enqueue(self, item):
        pass


    @abstractmethod
    def dequeue(self):
        pass


    @abstractmethod
    def is_empty(self):
        pass


    @abstractmethod
    def size(self):
        pass


class TextureQueue(RenderableQueue):
    def __init__(self):
        self.texture_queue = dict()

    
    def enqueue(self, x, y, texture_obj, shader):
        self.texture_queue[(x, y)] = (texture_obj, shader)


    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        coords, data = self.texture_queue.popitem()
        x, y = coords
        texture_obj, shader = data
        return x, y, texture_obj, shader


    def is_empty(self):
        return len(self.texture_queue) == 0
    

    def size(self):
        return len(self.texture_queue)


    def clear(self):
        self.texture_queue.clear()


class VerticesQueue(RenderableQueue):
    def __init__(self):
        self.vertices_queue = dict()

    
    def enqueue(self, x, y, vertices_obj, shader):
        self.vertices_queue[(x, y)] = (vertices_obj, shader)


    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        coords, data = self.vertices_queue.popitem()
        x, y = coords
        vertices_obj, shader = data
        return x, y, vertices_obj, shader
    

    def is_empty(self):
        return len(self.vertices_queue) == 0
    

    def size(self):
        return len(self.vertices_queue)


    def clear(self):
        self.vertices_queue.clear()


class TextQueue(RenderableQueue):
    def __init__(self):
        self.vertices_queue = dict()

    
    def enqueue(self, x, y, text_obj, shader):
        self.vertices_queue[(x, y)] = (text_obj, shader)


    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        coords, data = self.vertices_queue.popitem()
        x, y = coords
        text_obj, shader = data
        return x, y, text_obj, shader
    

    def is_empty(self):
        return len(self.vertices_queue) == 0
    

    def size(self):
        return len(self.vertices_queue)


    def clear(self):
        self.vertices_queue.clear()


class FacesQueue(RenderableQueue):
    def __init__(self):
        self.faces_queue = dict()

    
    def enqueue(self, x, y, faces_obj, shader):
        self.faces_queue[(x, y)] = (faces_obj, shader)


    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        coords, data = self.faces_queue.popitem()
        x, y = coords
        faces_obj, shader = data
        return x, y, faces_obj, shader
    
    
    def is_empty(self):
        return len(self.faces_queue) == 0
    

    def size(self):
        return len(self.faces_queue)


    def clear(self):
        self.faces_queue.clear()


class OpenGLRenderableQueue:
    def __init__(self):
        self.texture = TextureQueue()
        self.vertices = VerticesQueue()
        self.faces = FacesQueue()
        self.text = TextQueue()