from .vector import Vector

class Unit:
    def __init__(self, x, y, mass = 1, bounce = 0.5, name = None, is_static = False):
        self.center = Vector(x, y)
        self.angle = 0    
        self.name = name
        self.shape_type = None
        self.velocity = Vector(0, 0)
        self.angular_velocity = 0
                
        self.inertia = None
        self.mass = mass if not is_static else float("inf")
        self.bounce = bounce
        self.is_static = is_static

class Circle(Unit):
    def __init__(self, x, y, radius, mass = 1, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, bounce, name, is_static)
        self.radius = radius
        self.shape_type = "Circle"
        self.inertia = (1 / 2) * mass * radius * radius if not is_static else float("inf")


class Mesh(Unit):
    def __init__(self, x, y, vertices, tris, mass = 1, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, bounce, name, is_static)
        self.vertices = vertices
        self.tris = tris
        # Should write code that calc centroid and inertia