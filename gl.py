

import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from numpy import array, float32
import pygame

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        self.scene = []
        self.clearColor = [0.0, 0.0, 0.0, 1.0]
        _, _, self.width, self.height = screen.get_rect()
        self.activeShader = None
        self.skyboxShader = None
        #View Matrix
        self.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
        self.cameraRotation = glm.vec3(0.0, 0.0, 0.0)
        self.viewMatrix = self.getViewMatrix()
        
        #Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60.0),  #FOV
            self.width / self.height,  #Aspect Ratio
            0.1,  #Near Plane
            1000.0  #Far Plane
        )
        self.elapsedTime = 0.0

        self.dirLight = glm.vec3(1, 0, 0)
        self.lightIntensity = 1.0

        self.target = glm.vec3(0.0, 0.0, 0.0)

        

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)


    def createSkybox(self, textureList, vertex_shader, fragment_shader):
        skyboxBuffer = [
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,

            1.0, -1.0, -1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0, -1.0,
            1.0, -1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,

            -1.0,  1.0, -1.0,
            1.0,  1.0, -1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0
        ]

        self.skyboxVertBuffer = array(skyboxBuffer, dtype=float32)
        self.skyboxVBO = glGenBuffers(1)
        self.skyboxVAO = glGenVertexArrays(1)

        self.skyboxShader = compileProgram( compileShader(vertex_shader, GL_VERTEX_SHADER),
                                            compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        self.skyboxTextures = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.skyboxTextures)

        for i in range(6):
            texture = pygame.image.load(textureList[i])
            textureData = pygame.image.tostring(texture, "RGB", False)
            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                0,
                GL_RGB,
                texture.get_width(),
                texture.get_height(),
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                textureData
            )
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)


    def renderSkybox(self):

        skiboxVM = glm.mat4(glm.mat3(self.viewMatrix))

        if self.skyboxShader is not None:
            glUseProgram(self.skyboxShader)
            glUniformMatrix4fv(
                glGetUniformLocation(self.skyboxShader, "viewMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(skiboxVM)
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.skyboxShader, "projectionMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.projectionMatrix)
            )

        glDepthMask(GL_FALSE)

        glBindBuffer(GL_ARRAY_BUFFER, self.skyboxVBO)
        glBindVertexArray(self.skyboxVAO)

        glBufferData(GL_ARRAY_BUFFER,
                     self.skyboxVertBuffer.nbytes,
                     self.skyboxVertBuffer,
                     GL_STATIC_DRAW)

        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 3,
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.skyboxTextures)

        glDrawArrays(GL_TRIANGLES, 0, 36)

        glDepthMask(GL_TRUE)

    def Update(self):
        #self.viewMatrix = self.getViewMatrix()
        self.viewMatrix = glm.lookAt(self.cameraPosition, self.target, glm.vec3(0.0, 1.0, 0.0)) 

    def getViewMatrix(self):
        pitch = glm.radians(self.cameraRotation.x)
        yaw = glm.radians(self.cameraRotation.y)
        front = glm.vec3(
            glm.cos(pitch) * glm.cos(yaw),
            glm.sin(pitch),
            glm.cos(pitch) * glm.sin(yaw)
        )
        return glm.lookAt(self.cameraPosition, self.cameraPosition + front, glm.vec3(0.0, 1.0, 0.0))

    def setShader(self, vertex_shader=None, fragment_shader=None):

        #Si no se especifica un shader, se desactiva el shader
        if vertex_shader is None and fragment_shader is None:
            self.activeShader = None
        else:
            self.activeShader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            )

    def render(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.renderSkybox()

        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            #Envia la matriz de transformación a la tarjeta de video
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "viewMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.getViewMatrix())
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "projectionMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.projectionMatrix)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "time"),
                self.elapsedTime
            )
            glUniform3fv(
                glGetUniformLocation(self.activeShader, "dirLight"),
                1,
                glm.value_ptr(self.dirLight)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "lightIntensity"),
                self.lightIntensity
            )

        for obj in self.scene:

            #Envia la matriz de transformación a la tarjeta de video
            if self.activeShader is not None:
                glUniformMatrix4fv(
                    glGetUniformLocation(self.activeShader, "modelMatrix"),
                    1,
                    GL_FALSE,
                    glm.value_ptr(obj.getModelMatrix())
                )
            obj.render()
            