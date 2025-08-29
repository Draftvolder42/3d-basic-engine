from abc import ABC, abstractmethod
from PY3DENGINE.src.render.constants import RenderConstants
from OpenGL.GL import *
import numpy as np
import pygame


class Render(ABC):
    @abstractmethod
    def draw_queue(queue):
        pass


class BuffersHolder(ABC):
    @abstractmethod
    def init_texture_buffer(self):
        pass


    @abstractmethod
    def init_vertices_buffer(self, num_vertices):
        pass


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


    @abstractmethod
    def clear(self):
        pass


class RenderManager(ABC):
    @abstractmethod
    def render_queue(self, *args):
        pass


    @abstractmethod
    def clear_queue(self, *args):
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
        return x, y, texture_obj.texture, texture_obj.size, shader


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
        return x, y, vertices_obj.vertices, vertices_obj.size, vertices_obj.color, shader
    

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
        return x, y, text_obj.text, text_obj.color, text_obj.font, shader
    

    def is_empty(self):
        return len(self.vertices_queue) == 0
    

    def size(self):
        return len(self.vertices_queue)


    def clear(self):
        self.vertices_queue.clear()


class OpenGLRenderableQueue:
    def __init__(self):
        self.texture = TextureQueue()
        self.vertices = VerticesQueue()
        self.text = TextQueue()


class OpenGLBuffersHolder:
    def __init__(self, const):
        self.vertices_buffer = dict()
        self.texture_buffer = dict()
        self.const = const


    def new_texture_buffer(self, num_vertices = 4):
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        TBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        try:
            glBindVertexArray(VAO)

            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, 8 * num_vertices, None, GL_DYNAMIC_DRAW)  # 4 вершины * 2 float

            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)

            glBindBuffer(GL_ARRAY_BUFFER, TBO)
            glBufferData(GL_ARRAY_BUFFER, self.const.DEFAULT_TEX_COORDS.nbytes, self.const.DEFAULT_TEX_COORDS, GL_STATIC_DRAW)

            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
            glEnableVertexAttribArray(1)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.const.DEFAULT_INDICES.nbytes, self.const.DEFAULT_INDICES, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glBindVertexArray(0) 

            self.texture_buffer[num_vertices] = (VAO, VBO, TBO, EBO)
            print("Создан новый текстурный буфер для ", num_vertices, " вершин")
        except Exception as e:
            glDeleteVertexArrays(1, [VAO])
            glDeleteBuffers(3, [VBO, TBO, EBO])
            raise RuntimeError(f"Ошибка создания текстурного буфера: {str(e)}")


    def new_vertices_buffer(self, num_vertices):
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        try:
            glBindVertexArray(VAO)
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, num_vertices * 2 * 4, None, GL_DYNAMIC_DRAW)  # 6 вершин * 2 float * 4 байта

            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))


            glEnableVertexAttribArray(0)
            glBindVertexArray(0)

            self.vertices_buffer[num_vertices] = (VAO, VBO)
            print("Создан новый вершинный буфер для ", num_vertices, " вершин")
        except Exception as e:
            if 'VAO' in locals() and glIsVertexArray(VAO):
                glDeleteVertexArrays(1, [VAO])
            if 'VBO' in locals() and glIsBuffer(VBO):
                glDeleteBuffers(1, [VBO])
            raise RuntimeError(f"Ошибка создания вершинного буфера: {str(e)}")


    def cleanup_vertices_buffers(self):
        for num_vertices, buffers in list(self.vertices_buffer.items()):
            self.cleanup_single_vertices_buffer(num_vertices)
        print("Все вершинные буферы очищены")


    def cleanup_texture_buffers(self):
        for num_vertices, buffers in self.texture_buffer.items():
            VAO, VBO, TBO, EBO = buffers
            
            if glIsVertexArray(VAO):
                glDeleteVertexArrays(1, [VAO])
            
            for buffer in [VBO, TBO, EBO]:
                if glIsBuffer(buffer):
                    glDeleteBuffers(1, [buffer])
        
        self.texture_buffer.clear()
        print("Все текстурные буферы очищены")


class OpenGLRender(Render):
    def __init__(self, const, screen_size):
        self.buffers_holder = OpenGLBuffersHolder(const)
        self.screen_size = screen_size
        self.const = const


    def draw_queue(self, queue):
        self.renderable_queue = queue
        while not self.renderable_queue.texture.is_empty():
            x, y, texture, texture_size, shader = self.renderable_queue.texture.dequeue()
            self.draw_texture(x, y, texture, shader, self.screen_size, 4, texture_size)
        while not self.renderable_queue.vertices.is_empty():
            x, y, vertices, size, color, shader = self.renderable_queue.vertices.dequeue()
            self.draw_vertices(x, y, vertices, shader, self.screen_size, len(vertices), size, color)
        while not self.renderable_queue.text.is_empty():
            x, y, text, color, font, shader = self.renderable_queue.text.dequeue()
            self.draw_text(x, y, text, shader, self.screen_size, font, 4, color)


    def draw_texture(self, x, y, texture, shader, screen_size, num_vertices=4, texture_size = (1, 1)):
        if num_vertices not in self.buffers_holder.texture_buffer:
            self.buffers_holder.new_texture_buffer(num_vertices)
            vao, vbo, tbo, ebo = self.buffers_holder.texture_buffer[num_vertices]
            glBindVertexArray(vao)  # ← ОБЯЗАТЕЛЬНО СНАЧАЛА VAO!

            glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        x = x / screen_size[0]
        y = y / screen_size[1]
        w = texture_size[0] / screen_size[0]
        h = texture_size[1] / screen_size[1]

        vertices = np.array([
            x,     y,
            x + w, y,
            x + w, y - h,
            x,     y - h
        ], dtype=np.float32)

        #glBindVertexArray(vao)  # ← ОБЯЗАТЕЛЬНО СНАЧАЛА VAO!

        #glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glUseProgram(shader.shader)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(shader.textTextureLocation, 0)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        #glBindVertexArray(0)


    def draw_vertices(self, x, y, vertices, shader, screen_size, num_vertices=4, size = (1, 1), color = (1, 1, 1, 1)):
        if num_vertices not in self.buffers_holder.vertices_buffer:
            self.buffers_holder.new_vertices_buffer(num_vertices)
        vao, vbo = self.buffers_holder.vertices_buffer[num_vertices]

        vertices = np.array(vertices, dtype=np.float32)


        #w = size[0] / screen_size[0]
        #h = size[1] / screen_size[1]

        #vertices = np.array(vertices, dtype=np.float32)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glUseProgram(shader.shader)
        glUniform4f(shader.uColorLocation, *color)

        glDrawArrays(GL_LINE_LOOP, 0, num_vertices)

        glBindVertexArray(0)

    
    def draw_text(self, x, y, text, shader, screen_size, font, num_vertices=4, color = (1, 1, 1, 1)):
        if num_vertices not in self.buffers_holder.texture_buffer:
            self.buffers_holder.new_texture_buffer(num_vertices)
        vao, vbo, tbo, ebo = self.buffers_holder.texture_buffer[num_vertices]
        text_surface = font.render(text, True, (255, 255, 255))

        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width, text_height = text_surface.get_size()


        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        size = text_surface.get_size()

        x = x / screen_size[0]
        y = y / screen_size[1]

        w = size[0] / screen_size[0]
        h = size[1] / screen_size[1]

        vertices = np.array([
        x,     y,
        x + w, y,
        x + w, y - h,
        x,     y - h
        ], dtype=np.float32)


        glBindVertexArray(vao)  # ← ОБЯЗАТЕЛЬНО СНАЧАЛА VAO!

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glUseProgram(shader.shader)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(shader.textTextureLocation, 0)
        glUniform4f(shader.uColorLocation, *color)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glDeleteTextures([texture])
        glBindVertexArray(0)


class OpenGLBatchRender(Render):
    def __init__(self, const, screen_size):
        self.buffers_holder = OpenGLBuffersHolder(const)
        self.screen_size = screen_size
        self.const = const


    def draw_queue(self, queue):
        self.renderable_queue = queue
        while not self.renderable_queue.texture.is_empty():
            self.draw_texture(self.renderable_queue.texture)
        while not self.renderable_queue.vertices.is_empty():
            #coming soon
            x, y, vertices, size, color, shader = self.renderable_queue.vertices.dequeue()
            self.draw_vertices(x, y, vertices, shader, self.screen_size, len(vertices), size, color)
        while not self.renderable_queue.text.is_empty():
            #coming soons
            x, y, text, color, font, shader = self.renderable_queue.text.dequeue()
            self.draw_text(x, y, text, shader, self.screen_size, font, 4, color)


    def draw_texture(self, texture_queue):
        texture_batches = {}
        while not texture_queue.is_empty():
            x, y, texture, texture_size, shader = texture_queue.dequeue()
            key = (shader.shader, texture)
            if key not in texture_batches:
                texture_batches[key] = []
            texture_batches[key].append((x, y, texture_size))

        for (shader_id, texture), batch in texture_batches.items():
            if not batch:
                continue

            num_instances = len(batch)
            num_vertices_per_instance = 4
            total_vertices = num_instances * num_vertices_per_instance
            all_vertices_data = np.empty((total_vertices * 2,), dtype=np.float32)

            if num_vertices_per_instance not in self.buffers_holder.texture_buffer:
                self.buffers_holder.new_texture_buffer(num_vertices_per_instance)
            vao, vbo, tbo, ebo = self.buffers_holder.texture_buffer[num_vertices_per_instance]
            glBindVertexArray(vao)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, all_vertices_data.nbytes, None, GL_DYNAMIC_DRAW)
            offset = 0
            for x, y, texture_size in batch:
                x_norm = x / self.screen_size[0]
                y_norm = y / self.screen_size[1]
                w_norm = texture_size[0] / self.screen_size[0]
                h_norm = texture_size[1] / self.screen_size[1]

                vertices = np.array([
                    x_norm,     y_norm,
                    x_norm + w_norm, y_norm,
                    x_norm + w_norm, y_norm - h_norm,
                    x_norm,     y_norm - h_norm
                ], dtype=np.float32)
                all_vertices_data[offset:offset + vertices.size] = vertices.flatten()
                offset += vertices.size

            glBufferSubData(GL_ARRAY_BUFFER, 0, all_vertices_data.nbytes, all_vertices_data)

            glUseProgram(shader_id)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture)
            texture_location = glGetUniformLocation(shader_id, "textTexture")
            glUniform1i(texture_location, 0)

            glDrawElementsInstanced(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None, num_instances)

            glBindVertexArray(0)


    def draw_vertices(self, x, y, vertices, shader, screen_size, num_vertices=4, size = (1, 1), color = (1, 1, 1, 1)):
        if num_vertices not in self.buffers_holder.vertices_buffer:
            self.buffers_holder.new_vertices_buffer(num_vertices)
        vao, vbo = self.buffers_holder.vertices_buffer[num_vertices]

        vertices = np.array(vertices, dtype=np.float32)


        #w = size[0] / screen_size[0]
        #h = size[1] / screen_size[1]

        #vertices = np.array(vertices, dtype=np.float32)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glUseProgram(shader.shader)
        glUniform4f(shader.uColorLocation, *color)

        glDrawArrays(GL_LINE_LOOP, 0, num_vertices)

        glBindVertexArray(0)

    
    def draw_text(self, x, y, text, shader, screen_size, font, num_vertices=4, color = (1, 1, 1, 1)):
        if num_vertices not in self.buffers_holder.texture_buffer:
            self.buffers_holder.new_texture_buffer(num_vertices)
        vao, vbo, tbo, ebo = self.buffers_holder.texture_buffer[num_vertices]
        text_surface = font.render(text, True, (255, 255, 255))

        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width, text_height = text_surface.get_size()


        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        size = text_surface.get_size()

        x = x / screen_size[0]
        y = y / screen_size[1]

        w = size[0] / screen_size[0]
        h = size[1] / screen_size[1]

        vertices = np.array([
        x,     y,
        x + w, y,
        x + w, y - h,
        x,     y - h
        ], dtype=np.float32)


        glBindVertexArray(vao)  # ← ОБЯЗАТЕЛЬНО СНАЧАЛА VAO!

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glUseProgram(shader.shader)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(shader.textTextureLocation, 0)
        glUniform4f(shader.uColorLocation, *color)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glDeleteTextures([texture])
        glBindVertexArray(0)
    

class OpenGLRenderManager(RenderManager):
    def __init__(self, screen_size, strategy: Render):
        self.const = RenderConstants()
        self.renderable_queue = OpenGLRenderableQueue()
        self.render = strategy(self.const, screen_size)
        self.screen_size = screen_size


    def set_render_strategy(self, strategy: Render):
        self.render = strategy(self.const, self.screen_size)


    def render_queue(self):
        self.render.draw_queue(self.renderable_queue)


    def clear_queue(self):
        self.renderable_queue.texture.clear()
        self.renderable_queue.vertices.clear()
        self.renderable_queue.text.clear()


    def cleanup(self):
        self.renderable_queue.texture.clear()
        self.renderable_queue.vertices.clear()
        self.renderable_queue.text.clear()
        self.render.buffers_holder.cleanup_texture_buffers()
        self.render.buffers_holder.cleanup_vertices_buffers()