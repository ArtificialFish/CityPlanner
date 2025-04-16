import pygame as pg
from .utils import draw_text
from .utils import scale_image


class Hud:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hud_color = (198, 155, 93, 175)

        # building HUD
        self.build_surface = pg.Surface(
            (width * 0.15, height * 0.25), pg.SRCALPHA
        )
        self.build_rect = self.build_surface.get_rect(
            topleft=(width * 0.85, height * 0.75)
        )
        self.build_surface.fill(self.hud_color)

        # select HUD
        self.select_surface = pg.Surface(
            (width * 0.3, height * 0.2), pg.SRCALPHA
        )
        self.select_rect = self.select_surface.get_rect(
            topleft=(width * 0.85, height * 0.75)
        )
        self.select_surface.fill(self.hud_color)

        self.images = self.load_images()
        self.build_tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

    def create_build_hud(self):
        render_pos = [self.width * 0.85 + 10, self.height * 0.75 + 10]
        w = self.build_surface.get_width() // 5
        h = self.build_surface.get_height() // 5

        tiles = []

        col = row = 0

        for img_name, img in self.images.items():
            top_left = self.width * 0.85 + 10
            img = img.copy()
            img_scale = scale_image(img, w=w)

            img_w = img_scale.get_width()

            if (top_left + (col + 1) * (10 + img_w)) > self.width:
                row += 1
                col = 0

            pos = [
                top_left + col * (10 + img_w),
                (self.height * 0.75 + 10) + row * (10 + h),
            ]

            rect = img.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": img_name,
                    "icon": img_scale,
                    "image": self.images[img_name],
                    "rect": rect,
                }
            )

            render_pos[0] += img_scale.get_width() + 10

            col += 1

        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.build_tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):
        screen.blit(
            self.build_surface, (self.width * 0.85, self.height * 0.75)
        )

        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(
                self.select_surface, (self.width * 0.35, self.height * 0.80)
            )

            img = self.images[self.examined_tile["tile"]].copy()
            img_scale = scale_image(img, h=(h * 0.8))
            screen.blit(
                img_scale, (self.width * 0.35 + 10, self.height * 0.80 + 10)
            )
            draw_text(
                screen,
                self.examined_tile["tile"],
                40,
                (255, 255, 255),
                self.select_rect.center,
            )

        for tile in self.build_tiles:
            screen.blit(tile["icon"], tile["rect"].topleft)

        if self.selected_tile != None:
            tile = self.selected_tile
            pg.draw.polygon(
                screen,
                (255, 255, 255),
                [
                    tile["rect"].topleft,
                    tile["rect"].topright,
                    tile["rect"].bottomright,
                    tile["rect"].bottomleft,
                ],
                3,
            )

    def load_images(self):
        w = self.build_surface.get_width() // 5

        road = scale_image(pg.image.load("assets/road.png"), w=w)
        residential = scale_image(pg.image.load("assets/residential.png"), w=w)
        commercial = scale_image(pg.image.load("assets/commercial.png"), w=w)
        industrial = scale_image(pg.image.load("assets/industrial.png"), w=w)
        fire = scale_image(pg.image.load("assets/fire.png"), w=w)
        police = scale_image(pg.image.load("assets/police.png"), w=w)
        health = scale_image(pg.image.load("assets/health.png"), w=w)
        delete = scale_image(pg.image.load("assets/delete.png"), w=w)

        images = {
            "road": road,
            "residential": residential,
            "commercial": commercial,
            "industrial": industrial,
            "fire": fire,
            "police": police,
            "health": health,
            "delete": delete,
        }

        # for image in images:
        #     scale_image(image=image, w=w)

        return images
