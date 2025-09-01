from PY3DENGINE.src.render.render import OpenGLRenderManager, OpenGLBatchRender
from PY3DENGINE.src.render.renderable_types.textures import load_textures_from_folder
from PY3DENGINE.src.render.renderable_types.vertices import Vertices
from PY3DENGINE.src.render.renderable_types.text import Text
from PY3DENGINE.src.render.shaders.shaders import load_color_shader, load_texture_shader, load_text_shader, ColorShader, TextureShader, TextShader

from PY3DENGINE.src.conf.settings import WindowSettings, TextureSettings, RenderSettings, ModelSettings
from PY3DENGINE.src.utils.math_utils import hexagonCornersNormalized

from PY3DENGINE.src.engine.objects.camera import Camera3D
from PY3DENGINE.src.engine.objects.objects import Model3D, Vector3D
from PY3DENGINE.src.engine.objects.object_converter import Convert3DModelToVertices
from PY3DENGINE.src.utils.parsing import parse_obj
from PY3DENGINE.src.utils.transformations import rotate_x, rotate_y, rotate_z


import glfw
import pygame
from OpenGL.GL import *
import time


def init_window():
    if not glfw.init():
        raise Exception("GLFW не может быть инициализирован")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(WindowSettings.WIDTH, WindowSettings.HEIGHT, WindowSettings.WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW окно не может быть создано")
    glfw.make_context_current(window)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glfw.swap_interval(RenderSettings.V_SYNC)
    print("Окно инициализировано")
    return window


def init_fonts():
    pygame.font.init()
    print("Шрифты инициализированы")


def main():
    window = init_window()
    init_fonts()

    openGLRenderManager = OpenGLRenderManager((WindowSettings.WIDTH, WindowSettings.HEIGHT), OpenGLBatchRender)
    textures = load_textures_from_folder(TextureSettings.PATH)
    print("Загрузка текстур завершена, загружено: ", len(textures))
    COLOR_SHADER = ColorShader(load_color_shader())
    print("Загрузка цветового шейдеров завершена")
    TEXT_SHADER = TextShader(load_text_shader())
    print("Загрузка текстового шейдеров завершена")
    TEXTURE_SHADER = TextureShader(load_texture_shader())
    print("Загрузка текстурного шейдеров завершена")

    camera = Camera3D(Vector3D([0, 0, 0], [0, 0, 0]))
    hexogen3d = Model3D([0, 0, 3], parse_obj(ModelSettings.PATH +"\monkey.obj"))

    converter = Convert3DModelToVertices((WindowSettings.WIDTH, WindowSettings.HEIGHT), camera)


    vertices = Vertices()
    vertices.vertices = hexagonCornersNormalized(0, 0, 500, (WindowSettings.WIDTH, WindowSettings.HEIGHT))
    vertices.size = (1, 1)
    vertices.color = (1, 1, 1, 1)

    text = Text()
    text.text = "FPS"
    text.color = (1, 1, 1, 1)
    text.font = pygame.font.SysFont("Arial", 100)


    prev_time = time.time()
    frame_count = 0
    fps = 0
    cx = WindowSettings.WIDTH / 2
    cy = WindowSettings.HEIGHT / 2
    a = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        #for x in range(1):
            #for y in range(1):
                #openGLRenderManager.renderable_queue.texture.enqueue(x*25, y*25, textures["25x25rgb"], TEXTURE_SHADER)
        #for x in range(111):
            #for y in range(111):
                #openGLRenderManager.renderable_queue.vertices.enqueue(0, 0, vertices2, COLOR_SHADER)
        a = 0.01
        hexogen3d.transform(rotate_x(a)@rotate_y(a)@rotate_z(a))

        openGLRenderManager.renderable_queue.vertices.enqueue(0, 0, converter.project_vertices(hexogen3d), COLOR_SHADER)
        
        openGLRenderManager.renderable_queue.text.enqueue(0-cx, 0+cy, text, TEXT_SHADER)

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        openGLRenderManager.render_queue()

        glfw.swap_buffers(window)
        openGLRenderManager.clear_queue()


        current_time = time.time()
        delta = current_time - prev_time
        frame_count += 1
        if delta >= 1.0:
            fps = frame_count
            frame_count = 0
            prev_time = current_time
            text.text = f"FPS: {fps}"
        print(f"FPS: {fps}")
    openGLRenderManager.cleanup()
    print("Все буферы очищены")
    glfw.terminate()
    print("Работа завершена")

if __name__ == '__main__':
    main()


def run():
    main()