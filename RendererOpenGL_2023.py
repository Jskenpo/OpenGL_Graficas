
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

skyboxTextures = ['skybox/right.png', 'skybox/left.png', 'skybox/top.png', 'skybox/bottom.png', 'skybox/front.png', 'skybox/back.png']



gl = Renderer(screen)
gl.setShader(vertex_shader, fragment_shader)

gl.createSkybox(skyboxTextures, skyboxVertexShader, skyboxFragmentShader)

obj = Obj("objs/golem.obj")
objData = obj.objData



model = Model(objData)
model.loadTexture("textures/golem.jpeg")
model.position.z = -6
model.position.y = -2
model.scale = glm.vec3(0.7 , 0.7, 0.7)
gl.scene.append(model)
gl.lightIntensity = 5.5
gl.dirLight = glm.vec3(0.0, -1.0, -1.0)

#hacer que el target sea el modelo
gl.target = model.position


isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    gl.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()
 

    #mover camara con flechas y que el centro sea el modelo
    if keys[pygame.K_LEFT]:
        gl.cameraPosition.x -= 5 * deltaTime
    if keys[pygame.K_RIGHT]:
        gl.cameraPosition.x += 5 * deltaTime
    if keys[pygame.K_UP]:
        gl.cameraPosition.y += 5 * deltaTime
    if keys[pygame.K_DOWN]:
        gl.cameraPosition.y -= 5 * deltaTime



    #mover camara con mouse

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_rel()
        gl.cameraRotation.y += x * 0.5
        gl.cameraRotation.x += y * 0.5

    #hacer zoom 
    if keys[pygame.K_w]:
        gl.cameraPosition.z += 5 * deltaTime
    if keys[pygame.K_s]:
        gl.cameraPosition.z -= 5 * deltaTime


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
    
    gl.Update()
    gl.render()
    pygame.display.flip()

pygame.quit() 