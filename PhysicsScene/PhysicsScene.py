from .component import body
from . import Collision as Col
import pygame

class PhysicsScene:
    def __init__(self, body_lst : list):
        self.body_lst = body_lst
        self.cp = []

    def add_body(self, body):
        self.body_lst.append(body)

    def update_position(self, dt):
        for body in self.body_lst:
            if body.is_static == False:
                if body.shape_type == "Mesh" :
                    body.update(dt)
                else:
                    body.center += body.velocity * dt
                    body.angle += body.angular_velocity * dt

    def handle_collisions(self):
        self.cp = []
        for i in range(len(self.body_lst) - 1):
            for j in range(i + 1, len(self.body_lst)):
                if self.body_lst[i] == self.body_lst[j]:
                    continue

                pp = Col.collision(self.body_lst[i], self.body_lst[j])
                if pp: self.cp.append(pp)



    def step(self, dt):
        self.update_position(dt)
        self.handle_collisions()

    def render(self, screen, background):
        screen.fill(background)
        for bdy in self.body_lst:
            bdy.draw(screen)

        for pp in self.cp:
            if isinstance(pp,list):
                for p in pp:
                    pygame.draw.circle(screen, (0,0,0),(p.x,screen.get_height() - p.y),3)
            else:
                pygame.draw.circle(screen, (0,0,0),(pp.x,screen.get_height() - pp.y),3)

        pygame.display.flip()