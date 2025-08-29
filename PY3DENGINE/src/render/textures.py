from PIL import Image
from OpenGL.GL import *
import os
import numpy as np
from dataclasses import dataclass


def load_texture(path):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(img, dtype=np.uint8)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    mode = GL_RGBA if img.mode == 'RGBA' else GL_RGB
    glTexImage2D(GL_TEXTURE_2D, 0, mode, img.width, img.height, 0, mode, GL_UNSIGNED_BYTE, img_data)

    return texture


def load_textures_from_folder(folder_path):
    textures = {}
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Не найдена папка текстур: {folder_path}")

    for file in os.listdir(folder_path):
        if file.lower().endswith(".png"):
            name = os.path.splitext(file)[0]
            full_path = os.path.join(folder_path, file)
            try:
                texture = load_texture(full_path)
                textures[name] = Texture(texture, getTextureSize(texture))
            except Exception as e:
                print(f"Не удалось загрузить текстуру {file}: {e}")
    return textures


def getTextureSize(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    width = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_WIDTH)
    height = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_HEIGHT)
    return width, height


class Textures:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.textures = dict()
            self.__initialized = True

    def load_textures(self, path, func=load_textures_from_folder):
        self.textures = func(path)

    def get(self, name):
        return self.textures.get(name, None)



@dataclass
class Texture:
    texture: any
    size: tuple