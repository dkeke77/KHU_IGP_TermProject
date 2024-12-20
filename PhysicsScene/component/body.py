from .vector import Vector
import pygame.draw

class Body:
    def __init__(self, x, y, color, mass = 1, bounce = 0.5, is_static = False):
        self.center = Vector(x, y)
        self.angle = 0    
        self.shape_type = None
        self.velocity = Vector(0, 0)
        self.angular_velocity = 0
                
        self.inertia = None
        self.mass = mass if not is_static else float("inf")
        self.bounce = bounce
        self.is_static = is_static

        self.color = color
    
    def rotate(self, angle):
        self.angle += angle

    def draw(self, screen):
        pass


class Circle(Body):
    def __init__(self, x, y, radius, color, mass = 1, bounce = 0.5, is_static = False):
        super().__init__(x, y, color, mass, bounce, is_static)
        self.radius = radius
        self.shape_type = "Circle"
        self.inertia = (1 / 2) * mass * radius * radius if not is_static else float("inf")

    def rotate(self, angle):
        self.angle = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.center.x ,screen.get_height() - self.center.y), self.radius)


class Triangle(Body):
    def __init__(self, x, y, vertices, color, mass=1, bounce=0.5, is_static=False):
        super().__init__(x, y, color, mass, bounce, is_static)
        self.shape_type = "Triangle"
        self.vertices = vertices
        centroid = Vector(sum(vertex[0] for vertex in vertices) / 3,
                    sum(vertex[1] for vertex in vertices) / 3)
        self.translate_center(centroid)
        self.inertia = self.calc_inertia()

    def translate_center(self, v):
        self.center += v
        self.vertices = [(vtx - v) for vtx in self.vertices]
    
    def calc_inertia(self):
        v_a = self.vertices[1] - self.vertices[0]
        v_b = self.vertices[2] - self.vertices[0]
        return (v_a.dot(v_a) + v_a.dot(v_b) + v_b.dot(v_b)) / 6 * self.mass

    def draw(self, screen):
        coord = [(x, screen.get_height() - y) for (x, y) in self.get_world_coord()]
        pygame.draw.polygon(screen, self.color, coord, width=2)

    def get_world_coord(self):
        return [(vertex.rotate(self.angle) + self.center) for vertex in self.vertices]


class Mesh(Body):
    def __init__(self, x, y, vertices, tris, color, mass = 1, bounce = 0.5, is_static = False):
        super().__init__(x, y, color, mass, bounce, is_static)
        self.shape_type = "Mesh"
        self.area = []
        self.tris = []

        centroid = Vector(0,0)
        for tri in tris:
            for vtx in tri:
                centroid += Vector(x,y) + vertices[vtx]
        self.center = centroid / (len(tris)*3)

        for tri in tris:
            v1 = Vector(vertices[tri[1]][0],vertices[tri[1]][1]) - Vector(vertices[tri[0]][0],vertices[tri[0]][1])
            v2 = Vector(vertices[tri[2]][0],vertices[tri[2]][1]) - Vector(vertices[tri[0]][0],vertices[tri[0]][1])
            self.area.append(abs(v1.cross(v2)/2))
        self.area_all = sum(self.area)
        
        
        for tri in tris:
            tri_mass = mass * self.area[tris.index(tri)] / self.area_all
            new_tri = Triangle(x, y, (vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]),
                         self.color, tri_mass, bounce, is_static)
            #new_tri.translate_center(self.center - new_tri.center)
            self.tris.append(new_tri)
            
        self.inertia = self.calc_inertia()

    def calc_inertia(self):
        inertia = 0
        for tri in self.tris:
            d = Vector.dist(tri.center, self.center)
            inertia += tri.inertia + tri.mass * (d ** 2)
        return inertia
    
    def update(self, dt):
        # ANG_BOUND = 0.5
        # if self.angular_velocity > ANG_BOUND:
        #     self.angular_velocity = ANG_BOUND
        # elif self.angular_velocity < -ANG_BOUND:
        #     self.angular_velocity = -ANG_BOUND

        self.center += self.velocity * dt
        self.angle += self.angular_velocity * dt

        # Update Triangle Position
        for tri in self.tris:
            tri.center += self.velocity * dt

        # Update Triangle Rotation
        for tri in self.tris: 
            tri.center = tri.center.rotate_with(tri.center,self.center,self.angular_velocity)
            for i in range(3):
                world_coord = tri.vertices[i] + self.center
                world_coord = Vector.rotate_with(world_coord, self.center, self.angular_velocity)
                tri.vertices[i] = world_coord - self.center

            

    def draw(self, screen):
        for tri in self.tris:
            tri.draw(screen)
            pygame.draw.circle(screen, (128, 128, 0), (tri.center[0], screen.get_height() - tri.center[1]), 3)
        pygame.draw.circle(screen, (255, 0, 0), (self.center[0], screen.get_height() - self.center[1]), 3)