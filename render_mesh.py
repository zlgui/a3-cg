from OpenGL.GL import *
import pygame

class RenderMesh:
    def __init__(self, file_path, draw_type):
        self.file_path = file_path
        self.draw_type = draw_type
        self.vertices = []
        self.faces = []
        self.tex_cords = []
        self.texture_id = None
        self.load_drawing()

    def load_drawing(self):

        with open(self.file_path, 'r') as file:

            for line in file:
                if line.startswith('v '): RenderMesh.load_vertex(self, line)
                if line.startswith('vt '): RenderMesh.load_vertex_texture(self, line)
                if line.startswith('f '): RenderMesh.load_faces(self, line)

    def load_texture(self, image_path):
        texture_surface = pygame.image.load(image_path)
        texture_data = pygame.image.tostring(texture_surface, "RGB", True)
        width, height = texture_surface.get_rect().size

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def create_model(self):

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(self.draw_type)
        RenderMesh.setup_model(self)
        glEnd()

    def load_vertex(self, line):
        vertex = [float(value) for value in line[2:].split()]
        self.vertices.append(vertex)

    def load_vertex_texture(self, line):
        text_cord = [float(value) for value in line[3:].split()]
        self.tex_cords.append(text_cord)

    def load_faces(self, line):
        face = []
        text_cord_index = []

        for value in line[2:].split():
            indexes = value.split('/')
            face.append(int(indexes[0]) - 1)

            if len(indexes) > 1 and indexes[1]:
                text_cord_index.append(int(indexes[1]) - 1)

        self.faces.append((face, text_cord_index))

    def setup_model(self):
        for face, text_cord_index in self.faces:
            for i, vertex_index in enumerate(face):
                if text_cord_index:
                    tex_cord_index = text_cord_index[i]
                    glTexCoord2fv(self.tex_cords[tex_cord_index])
                glVertex3fv(self.vertices[vertex_index])