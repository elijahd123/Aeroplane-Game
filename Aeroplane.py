import random
import time
import pygame
import math

pygame.init()

width, height = 1400, 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aeroplane")
run = True
clock = pygame.time.Clock()
fps = 30
frame = 0
missiles = []
in_game = True
start = time.time()


class Plane:
    def __init__(self, x: int = (width // 2), y: int = (height // 2), facing_d: int = 0,
                 colour: list = [242, 46, 31].copy(), min_speed: int = 10, max_speed: int = 20, speed_inc: float = 0.1):
        self.x = x
        self.y = y
        self.facing_d = facing_d
        self.colour = colour
        self.points = []
        self.set_points()
        self.speed = min_speed
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed_inc = speed_inc

    def get_point(self, point):
        x, y = point[0], point[1]

        dist = math.hypot(x, y)

        angle = math.radians(math.degrees(math.atan2(y, x)) + self.facing_d)

        return self.x + (dist * math.cos(angle)), self.y + (dist * math.sin(angle))

    def set_points(self):
        rel_points = [(40, 0), (38, 4), (35, 6), (10, 7), (0, 30), (-5, 30), (0, 7), (-15, 6), (-22, 15), (-22, -15),
                      (-15, -6), (0, -7), (-5, -30), (0, -30), (10, -7), (35, -6), (38, -4)]
        self.points = [self.get_point(p) for p in rel_points]

    def turn(self, amount_d):
        self.facing_d += amount_d
        if self.speed > self.min_speed:
            self.speed -= self.speed_inc

        if self.speed > self.min_speed:
            self.speed -= self.speed_inc

    def right(self):
        self.turn(5)

    def left(self):
        self.turn(-5)

    def move(self):
        self.x = int(self.x + (self.speed * math.cos(math.radians(self.facing_d))))
        self.y = int(self.y + (self.speed * math.sin(math.radians(self.facing_d))))

        if self.x > width:
            self.x = self.x % width
        elif self.x < 0:
            self.x += width
        if self.y > height:
            self.y = self.y % height
        elif self.y < 0:
            self.y += height

        if self.speed < self.max_speed:
            self.speed += self.speed_inc

    def update(self):
        self.move()
        self.set_points()

    def draw(self, win):
        pygame.draw.polygon(win, self.colour, self.points)
        #pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 3)


plane = Plane()


class Missile:
    def __init__(self, x: int, y: int, plane: Plane, life_time: int = 25, colour: list = [8, 64, 0].copy(), min_speed: int = 4, max_speed: int = 10, speed_inc: float = 0.1):
        self.plane = plane
        self.x = x
        self.y = y
        self.life_time = life_time
        self.facing_d = self.get_angle_to_plane()
        self.colour = colour
        self.points = []
        self.set_points()
        self.speed = min_speed
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed_inc = speed_inc

    def get_angle_to_plane(self):
        return math.degrees(math.atan2(self.plane.y - self.y, self.plane.x - self.x))

    def get_point(self, point):
        x, y = point[0], point[1]

        dist = math.hypot(x, y)

        angle = math.radians(math.degrees(math.atan2(y, x)) + self.facing_d)

        return self.x + (dist * math.cos(angle)), self.y + (dist * math.sin(angle))

    def set_points(self):
        rel_points = [(26, 0), (16, 5), (-9, 5), (-9, -5), (16, -5)]
        self.points = [self.get_point(p) for p in rel_points]

    def turn(self, amount_d):
        self.facing_d += amount_d
        if self.speed > self.min_speed:
            self.speed -= self.speed_inc

    def right(self):
        self.turn(5)

    def left(self):
        self.turn(-5)

    def check_turn(self):
        angle = self.get_angle_to_plane() - self.facing_d
        if angle > 10:
            self.right()
        elif angle < -10:
            self.left()

    def move(self):
        self.x = int(self.x + (self.speed * math.cos(math.radians(self.facing_d))))
        self.y = int(self.y + (self.speed * math.sin(math.radians(self.facing_d))))

        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height

        if self.speed < self.max_speed:
            self.speed += self.speed_inc

    def update(self):
        self.check_turn()
        self.move()
        self.set_points()

    def draw(self, win):
        pygame.draw.polygon(win, self.colour, self.points)
        #pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 3)


def generate_missile(plane):
    x, y = random.randint(50, width - 50), random.randint(50, height - 50)

    while math.hypot(abs(x - plane.x), abs(y - plane.y)) < 150:
        x, y = random.randint(50, width - 50), random.randint(50, height - 50)

    missile = Missile(x, y, plane)
    return missile


def redraw_win(win, plane, missiles):
    win.fill((135, 206, 235))

    plane.draw(win)

    for missile in missiles:
        missile.draw(win)

    pygame.display.update()


while run:
    clock.tick(fps)
    frame = (frame + 1) % fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if in_game:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            plane.left()
        if keys[pygame.K_d]:
            plane.right()

        plane.update()

        if frame == 0:
            missiles.append(generate_missile(plane))

        missiles = [missile for missile in missiles if missile.life_time > 0]

        for missile in missiles:
            if frame == 0:
                missile.life_time -= 1
            missile.update()
            if math.hypot(abs(missile.x - plane.x), abs(missile.y - plane.y)) < 30:
                in_game = False
                game_time = int(time.time() - start)
                print(game_time)

    redraw_win(win, plane, missiles)
