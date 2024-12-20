from .component.vector import Vector
from .component import body as b

def collision_cir_cir(body1 : b.Circle, body2 : b.Circle):
    dist = Vector.dist(body1.center, body2.center)

    if dist >= body1.radius + body2.radius:
        return None, None
    
    normal = (body2.center - body1.center).normalize()
    depth  = body1.radius + body2.radius - dist

    return normal, depth

def collision_cir_tri(circle : b.Circle, tri : b.Triangle):
    normal = Vector(0, 0)
    penetration_depth = float('inf')

    vertices = tri.get_world_coord()

    for i in range(3):
        edge = vertices[(i + 1) % 3] - vertices[i]

        axis = Vector(-edge.y, edge.x).normalize()
       
        # project circle onto axis
        min_a, max_a = project_vertices(vertices, axis)
        min_b, max_b = project_circle(circle.center, circle.radius, axis)
        
        if max_a <= min_b or max_b <= min_a:
            return None, None
        
        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < penetration_depth:
            penetration_depth = axis_depth
            normal = axis

    cp_index = find_closest_point_on_polygon(circle.center, vertices)
    
    cp = vertices[cp_index]
    
    axis = (cp - circle.center).normalize()

    min_a, max_a = project_circle(circle.center, circle.radius, axis)
    min_b, max_b = project_vertices(vertices, axis)

    if max_a <= min_b or max_b <= min_a:
        return None, None
    
    axis_depth = min(max_b - min_a, max_a - min_b)

    if axis_depth < penetration_depth:
        penetration_depth = axis_depth
        normal = axis


    direction = (tri.center - circle.center).normalize()
   
    if direction.dot(normal) > 0:
        normal *= -1
        
    return normal, penetration_depth

def collision_tri_tri(body1 : b.Triangle, body2 : b.Triangle):
    normal = Vector(0, 0)
    depth = float('inf')
    
    vertices1 = body1.get_world_coord()
    vertices2 = body2.get_world_coord()
    
    for i in range(len(vertices1)):
        va = vertices1[i]
        vb = vertices1[(i + 1) % len(vertices1)]
        edge = vb - va
        axis = Vector(-edge.y, edge.x).normalize()
        min_a, max_a = project_vertices(body1.get_world_coord(), axis)
        min_b, max_b = project_vertices(body2.get_world_coord(), axis)

        if min_a >= max_b or min_b >= max_a:
            return None, None

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    # Add axes from polygon_2
    for i in range(len(vertices2)):
        va = vertices2[i]
        vb = vertices2[(i + 1) % len(vertices2)]
        edge = vb - va
        axis = Vector(-edge.y, edge.x).normalize()
        min_a, max_a = project_vertices(body1.get_world_coord(), axis)
        min_b, max_b = project_vertices(body2.get_world_coord(), axis)

        if min_a >= max_b or min_b >= max_a:
            return None, None

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    direction = (body1.center - body2.center).normalize()

    if direction.dot(normal) < 0:
        normal *= -1


    return normal, depth


def project_vertices(vertices: list[Vector], axis: Vector):
    min_proj = float('inf')
    max_proj = float('-inf')

    for v in vertices:
        proj = Vector(v[0],v[1]).dot(axis)

        if proj < min_proj:
            min_proj = proj
        if proj > max_proj:
            max_proj = proj

    return min_proj, max_proj

def project_circle(center, radius: float, axis: Vector):
    direction = axis.normalize()
    direction_and_radius = direction * radius

    p1 = center + direction_and_radius
    p2 = center - direction_and_radius

    min_proj = p1.dot(axis)
    max_proj = p2.dot(axis)

    if min_proj > max_proj:
        min_proj, max_proj = max_proj, min_proj

    return min_proj, max_proj

def find_closest_point_on_polygon(circle_center: Vector, vertices: list[Vector]):
    result = -1
    min_distance = float('inf')

    for i, v in enumerate(vertices):
        dist = Vector.dist(Vector(v[0],v[1]), circle_center)

        if dist < min_distance:
            min_distance = dist
            result = i

    return result
