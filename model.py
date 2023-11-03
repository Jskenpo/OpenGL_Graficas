from OpenGL.GL import *
import glm
from numpy import array, float32
import pygame

class Model(object):
    def __init__(self, data):
        self.vertbuffer = array(data, dtype = float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

    def loadTexture (self, textureName):
        self.textureSurface = pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface, 'RGB', True)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurface.get_width(), self.textureSurface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData)

        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, 0)

    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw =  glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat



    def render(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertbuffer.nbytes, self.vertbuffer, GL_STATIC_DRAW)

        # positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

       
        # UVs
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

        # normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 5))
        glEnableVertexAttribArray(2)
        
        # texture

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 
                        0, 
                        GL_RGB, 
                        self.textureSurface.get_width(), 
                        self.textureSurface.get_height(), 
                        0, 
                        GL_RGB, 
                        GL_UNSIGNED_BYTE, 
                        self.textureData)

        glGenerateTextureMipmap(self.texture)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertbuffer) / 8))

        '''
        if hasattr(self, 'texture'):
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertbuffer) / 8))
            glBindTexture(GL_TEXTURE_2D, 0)
        else:
            glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertbuffer) / 8))
        '''
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


