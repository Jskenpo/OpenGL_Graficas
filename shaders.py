

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

greyscale_fragment_shader = """

    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {

        vec4 color = texture(tex, UVs);
        float grey = (color.r + color.g + color.b) / 3.0;
        fragColor = vec4(grey, grey, grey, 1.0);
    }
"""

Fresnel_shader = """

    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {

        vec4 color = texture(tex, UVs);
        float fresnel = pow(1.0 - dot(normal, vec3(0.0, 0.0, -1.0)), 2.0);
        fragColor = vec4(color.rgb * fresnel, 1.0);
    }
"""

noise_shader = """  
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
            
            vec4 color = texture(tex, UVs);
            float noise = fract(sin(dot(UVs, vec2(12.9898,78.233))) * 43758.5453);
            fragColor = vec4(color.rgb * noise, 1.0);
        }
"""

stripes_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
                
                vec4 color = texture(tex, UVs);
                float stripes = step(0.2, fract(UVs.x * 5.0));
                fragColor = vec4(color.rgb * stripes, 1.0);
            }

"""   

