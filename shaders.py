# En OpenGl los shaders se escriben en un nuevo lenguaje de programacion llamado GLSL
# (OpenGL Shading Language). Los shaders son programas que corren en la GPU y son
# los encargados de procesar los vertices y los px de la escena. Los shaders

vertex_shader = '''
#version 450 core 
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 textCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


out vec2 Uvs;

void main(){


    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    
    Uvs = textCoords;
}

'''

fragment_shader = '''
#version 450 core
in vec2 Uvs;

uniform sampler2D basicTexture;

out vec4 FragColor;

void main(){
    FragColor = texture(basicTexture, Uvs);
}



'''
