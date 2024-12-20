import PhysicsScene.PhysicsScene as phy
import PhysicsScene.component.body as body
import pygame
import sys

# CONSTANT ZONE
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED_X, PLAYER_SPEED_Y = 2, 2
FPS = 30
GRAVITY = 9.8
COLORS = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "orange": (255, 128, 0),
    "cyan": (0, 255, 255),
}

# Init Game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

body_list = []
Player = body.Mesh(
    x=400,
    y=300,
    vertices=[
        (0,-40),(90,20),(-90,20),
        (-150,60),(-15,150),
        (150,60),(15,150),
        (-80,-40),(80,-40)],
    tris=[(0,1,2),(3,2,4),(1,5,6),(0,3,7),(0,5,8)],
    color=COLORS['blue'],
    mass=40,
)

body_list.append(Player)
Scene = phy.PhysicsScene(body_list)

Scene.add_body(body.Circle(
    x=400,
    y=400,
    radius=7,
    color=COLORS['green'],
    mass=1
))

move_left = False
move_right = False
move_up = False
move_down = False
dt = 1 / FPS

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

    if move_left:
        Player.velocity[0] -= PLAYER_SPEED_X
    if move_right:
        Player.velocity[0] += PLAYER_SPEED_X
    if move_up:
        Player.velocity[1] += PLAYER_SPEED_Y
    if move_down:
        Player.velocity[1] -= PLAYER_SPEED_Y

    Scene.step(dt)
    Scene.render(screen, COLORS['white'])

    pygame.time.Clock().tick(FPS)
    