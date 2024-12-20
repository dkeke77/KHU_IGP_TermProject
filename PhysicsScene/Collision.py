from .component.vector import Vector
from .component import body
from . import SAT

def collision(body1, body2):
    normal, depth, contact_points = None, None, None
    tri_index = -1

    if body1.shape_type == "Mesh":
        normal_lst,depth_lst,cp_lst = [],[],[]
        for tri in body1.tris:
            normal_temp, depth_temp = handle_primitive_collision(tri, body2)
            if normal_temp != None and depth_temp != None:
                tri_index = body1.tris.index(tri)
                cp = get_primitive_contact_points(body1.tris[tri_index], body2)
                normal_lst.append(normal_temp)
                depth_lst.append(depth_temp)
                cp_lst.append(sum(cp,start=Vector(0,0)) / len(cp))
                break
        
        if len(normal_lst) > 0:
            normal = sum(normal_lst) / len(normal_lst)
            depth = sum(depth_lst) / len(depth_lst)
            contact_points = sum(cp_lst) / len(cp_lst)
            response(body1, body2, normal, depth, contact_points)
        return contact_points
    
    elif body2.shape_type == "Mesh":
        normal_lst,depth_lst,cp_lst = [],[],[]
        for tri in body2.tris:
            normal_temp, depth_temp = handle_primitive_collision(body1, tri)
            if normal_temp != None and depth_temp != None:
                tri_index = body2.tris.index(tri)
                cp = get_primitive_contact_points(body1, body2.tris[tri_index])
                normal_lst.append(normal_temp)
                depth_lst.append(depth_temp)
                cp_lst.append(sum(cp,start=Vector(0,0)) / len(cp))
                break

        if len(normal_lst) > 0:
            normal = sum(normal_lst) / len(normal_lst)
            depth = sum(depth_lst) / len(depth_lst)
            contact_points = sum(cp_lst) / len(cp_lst)
            response(body1, body2, normal, depth, contact_points)
        return contact_points
    
    else:
        normal, depth = handle_primitive_collision(body1, body2)

        if normal == None or depth == None: return None
            
        contact_points = get_primitive_contact_points(body1, body2)

        if contact_points != None : 
            response(body1, body2, normal, depth, contact_points)
            return contact_points


def handle_primitive_collision(body1, body2):
    normal, depth = None, None
    if body1.shape_type == "Circle" and body2.shape_type == "Circle" :
        normal, depth = SAT.collision_cir_cir(body1, body2)
    elif body1.shape_type == "Circle" and body2.shape_type == "Triangle" :
        normal, depth = SAT.collision_cir_tri(body1, body2)
    elif body1.shape_type == "Triangle" and body2.shape_type == "Circle" :
        normal, depth = SAT.collision_cir_tri(body2, body1)
    elif body1.shape_type == "Triangle" and body2.shape_type == "Triangle" :
        normal, depth = SAT.collision_tri_tri(body1, body2)
    return normal, depth

def get_primitive_contact_points(body1, body2):
    if body1.shape_type == "Circle" and body2.shape_type == "Circle" :
        contact_points = contact_points_cir_cir(body1, body2)
    elif body1.shape_type == "Circle" and body2.shape_type == "Triangle" :
        contact_points = contact_points_cir_tri(body1, body2)
    elif body1.shape_type == "Triangle" and body2.shape_type == "Circle" :
        contact_points = contact_points_cir_tri(body2, body1)
    elif body1.shape_type == "Triangle" and body2.shape_type == "Triangle" :
        contact_points = contact_points_tri_tri(body1, body2)
    return contact_points

def contact_points_cir_cir(body1, body2):
    normal = (body2.center - body1.center).normalize()
    contact_point = body1.center + normal * body1.radius

    return [contact_point]

def contact_points_cir_tri(circle, tri):
    min_distance = float('inf')
    vertices = tri.get_world_coord()
    
    for i in range(3):
        va = Vector(vertices[i][0],vertices[i][1])
        vb = Vector(vertices[(i + 1) % 3][0],vertices[(i + 1) % 3][1])

        cp, distance = point_to_line_segment_projection(circle.center, va, vb)

        if distance < min_distance:
            min_distance = distance
            contact_point = cp
        
    return [contact_point]

def contact_points_tri_tri(body1, body2):
    epsilon = 0.0005
    min_distance = float('inf')
    contact_point_1 = None
    contact_point_2 = None

    for i in range(len(body1.get_world_coord())):
        vp = body1.get_world_coord()[i]
        for j in range(len(body2.get_world_coord())):
            va = body2.get_world_coord()[j]
            vb = body2.get_world_coord()[(j + 1) % len(body2.get_world_coord())]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.dist_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    for i in range(len(body2.get_world_coord())):
        vp = body2.get_world_coord()[i]
        for j in range(len(body1.get_world_coord())):
            va = body1.get_world_coord()[j]
            vb = body1.get_world_coord()[(j + 1) % len(body1.get_world_coord())]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.dist_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    return [cp for cp in [contact_point_1, contact_point_2] if cp is not None]

def response(body_1, body_2, normal_vector, penetration_depth, contact_point):
    if isinstance(contact_point, list):
        if len(contact_point) == 2: 
            contact_point = (contact_point[0] + contact_point[1]) / 2
        else:
            contact_point = contact_point[0]

    r_1 = contact_point - body_1.center  
    r_2 = contact_point - body_2.center

    r_1_perp = Vector(-r_1.y, r_1.x)
    r_2_perp = Vector(-r_2.y, r_2.x)

    relative_velocity = (body_2.velocity + r_2_perp * body_2.angular_velocity) - (body_1.velocity + r_1_perp * body_1.angular_velocity)  
    
    penetration_velocity = relative_velocity.dot(normal_vector)  
    
    if penetration_velocity > 0:
        return

    resolve_overlap(body_1, body_2, normal_vector, penetration_depth)

    r = min(body_1.bounce, body_2.bounce) 

    j = -(1+r)*penetration_velocity
    j /= 1/body_1.mass + 1/body_2.mass \
        + (r_1_perp.dot(normal_vector) ** 2) / body_1.inertia \
        + (r_2_perp.dot(normal_vector) ** 2) / body_2.inertia

    impulse = normal_vector * j  

    body_1.velocity -= impulse / body_1.mass
    body_1.angular_velocity -= r_1.cross(impulse) / body_1.inertia  

    body_2.velocity += impulse / body_2.mass
    body_2.angular_velocity += r_2.cross(impulse) / body_2.inertia 

    if body_1.shape_type == "Circle": body_1.angular_velocity = 0
    if body_2.shape_type == "Circle": body_2.angular_velocity = 0


def resolve_overlap(body1, body2, normal, depth):
    depth_vector = normal * depth

    if body1.is_static:
        body2.center += depth_vector
    elif body2.is_static:
        body1.center -= depth_vector
    else:
        body1.center -= depth_vector / 2
        body2.center += depth_vector / 2

def point_to_line_segment_projection(point: Vector, a: Vector, b: Vector):
    ab = b - a 
    ap = point - a 
    
    proj = ap.dot(ab)
    d = proj / ab.dot(ab) 

    if d <= 0:
        contact_point = a
    elif d >= 1:
        contact_point = b
    else: 
        contact_point = a + ab * d

    distance = Vector.dist(contact_point, point)

    return contact_point, distance