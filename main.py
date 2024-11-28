from pygame.locals import *
from OpenGL.GLU import *
from render_mesh import *

pygame.init()

screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Iron Golem A3')

mesh = RenderMesh("model/iron_golem.obj", GL_TRIANGLES)
mesh.load_texture("model/iron_golem_texture.png")

camera_position = [-8, -10, -70]
camera_speed = 1.0
camera_fov = 65.0
object_rotation = 180

def camera_and_model_config():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camera_fov, (screen_width / screen_height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    glTranslate(*camera_position)
    glRotatef(object_rotation, 0, 1, 0)

    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)

    process_model_lighting()

def process_inputs():
    global camera_fov
    global object_rotation
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        object_rotation += 1.0

        if object_rotation > 360.0: object_rotation = 360.0

        glRotatef(object_rotation,0, 1, 0)

    if keys[pygame.K_a]: glTranslatef(camera_speed, 0, 0)

    if keys[pygame.K_w]: glTranslatef(0, -camera_speed, 0)

    if keys[pygame.K_s]: glTranslatef(0, camera_speed, 0)

    if keys[pygame.K_d]: glTranslatef(-camera_speed, 0, 0)

    if keys[pygame.K_d]: glTranslatef(-camera_speed, 0, 0)

    if keys[pygame.K_i]:
        camera_fov -= 5.0

        if camera_fov < 20.0: camera_fov = 20.0

        process_camera_zoom()

    if keys[pygame.K_o]:
        camera_fov += 5.0

        if camera_fov > 130.0: camera_fov = 130.0

        process_camera_zoom()

def process_camera_zoom():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camera_fov, (screen_width / screen_height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def create_model():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    mesh.create_model()
    glPopMatrix()

def process_model_lighting():

    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)
    light_position = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    ambient_light = [1.0, 1.0, 1.0, 1.0]
    diffuse_light = [1.0, 1.0, 1.0, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    material_diffuse = [1.0, 1.0, 1.0, 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    shininess = 50.0
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

done = False
camera_and_model_config()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        process_inputs()

    create_model()
    pygame.display.flip()
    pygame.time.wait(5)
pygame.quit()

