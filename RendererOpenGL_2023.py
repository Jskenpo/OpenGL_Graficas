
import pygame
import glm
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
from obj import Obj


width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

gl = Renderer(screen)
gl.setShader(vertex_shader, fragment_shader)

obj = Obj("objs/golem.obj")
objData = obj.objData



model = Model(objData)
model.loadTexture("textures/golem.jpeg")
model.position.z = -6
model.position.y = -2
model.scale = glm.vec3(0.7, 0.7, 0.7)
gl.scene.append(model)
gl.lightIntensity = 5.5
gl.dirLight = glm.vec3(0.0, -1.0, -1.0)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    gl.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        gl.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        gl.clearColor[0] -= deltaTime
    if keys[K_UP]:
        gl.clearColor[1] += deltaTime
    if keys[K_DOWN]:
        gl.clearColor[1] -= deltaTime
    if keys[K_SPACE]:
        gl.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        gl.clearColor[2] -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_1:
                gl.setShader(vertex_shader, fragment_shader)
            if event.key == pygame.K_2:
                gl.setShader(vertex_shader, greyscale_fragment_shader)
            if event.key == pygame.K_3:
                gl.setShader(vertex_shader, Fresnel_shader)
            if event.key == pygame.K_4:
                gl.setShader(vertex_shader, noise_shader)
            if event.key == pygame.K_5:
                gl.setShader(vertex_shader, stripes_shader)
    gl.render()
    pygame.display.flip()

pygame.quit()