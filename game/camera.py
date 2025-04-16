import pygame as pg


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.scroll = pg.Vector2(0, 0)

        self.dx = 0
        self.dy = 0

        self.speed = 25

    def update(self):
        self.dx = 0
        self.dy = 0

        key = pg.key.get_pressed()

        if key[pg.K_w] or key[pg.K_UP]:
            self.dy += self.speed
        if key[pg.K_a] or key[pg.K_LEFT]:
            self.dx += self.speed
        if key[pg.K_s] or key[pg.K_DOWN]:
            self.dy -= self.speed
        if key[pg.K_d] or key[pg.K_RIGHT]:
            self.dx -= self.speed

        # mouse_pos = pg.mouse.get_pos()

        # if mouse_pos[0] > self.width * 0.97:
        #     self.dx = -self.speed
        # elif mouse_pos[0] < self.width * 0.03:
        #     self.dx = self.speed
        # else:
        #     self.dx = 0

        # if mouse_pos[1] > self.height * 0.97:
        #     self.dy = -self.speed
        # elif mouse_pos[1] < self.height * 0.03:
        #     self.dy = self.speed
        # else:
        #     self.dy = 0

        self.scroll.x += self.dx
        self.scroll.y += self.dy
