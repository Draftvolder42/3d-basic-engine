from OpenGL.GL.shaders import compileProgram, compileShader, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glGetUniformLocation
from dataclasses import dataclass


def load_color_shader():
    vertex_shader = """
    #version 330 core
    layout (location = 0) in vec2 aPos;
    uniform vec4 uColor;
    out vec4 vertexColor;
    void main() {
        gl_Position = vec4(aPos, 0.0, 1.0);
        vertexColor = uColor;
    }
    """
    fragment_shader = """
    #version 330 core
    in vec4 vertexColor;
    out vec4 FragColor;
    void main() {
        FragColor = vertexColor;
    }
    """
    return compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )


def load_text_shader():
    vertex_src = """
    #version 330 core

    layout (location = 0) in vec2 aPos;
    layout (location = 1) in vec2 aTexCoord;

    out vec2 TexCoord;

    void main()
    {
        gl_Position = vec4(aPos, 0.0, 1.0);
        TexCoord = aTexCoord;
    }
    """
    fragment_src = """
    #version 330 core

    in vec2 TexCoord;
    out vec4 FragColor;

    uniform sampler2D textTexture;   
    uniform vec4 uColor;             

    void main()
    {
        vec4 texColor = texture(textTexture, TexCoord);
        FragColor = texColor * uColor;
    }
    """
    return compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )


def load_texture_shader():
    vertex_shader = """
    #version 330 core
    layout (location = 0) in vec2 aPos;
    layout (location = 1) in vec2 aTexCoord;
    out vec2 TexCoord;
    void main() {
        gl_Position = vec4(aPos, 0.0, 1.0);
        TexCoord = aTexCoord;
    }
    """
    fragment_shader = """
    #version 330 core
    in vec2 TexCoord;
    out vec4 FragColor;
    uniform sampler2D textTexture;
    void main() {
        FragColor = texture(textTexture, TexCoord);
    }
    """
    return compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )


class TextureShader:
    def __init__(self, shader: any):
        self.shader = shader
        self._textTextureLocation = glGetUniformLocation(self.shader, "textTexture")

    @property
    def textTextureLocation(self):
        return self._textTextureLocation


class TextShader:
    def __init__(self, shader: any):
        self.shader = shader
        self._textTextureLocation = glGetUniformLocation(self.shader, "textTexture")
        self._uColorLocation = glGetUniformLocation(self.shader, "uColor")
    
    @property
    def textTextureLocation(self):
        return self._textTextureLocation
    
    @property
    def uColorLocation(self):
        return self._uColorLocation


class ColorShader:
    def __init__(self, shader: any):
        self.shader = shader
        self._uColorLocation = glGetUniformLocation(self.shader, "uColor")

    @property
    def uColorLocation(self):
        return self._uColorLocation