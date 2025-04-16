import pygame as pg
from .settings import TILE_SIZE
from .utils import draw_text
from .utils import scale_image


class World:

    def __init__(self, hud, grid_x, grid_y, width, height):
        self.hud = hud
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width = width
        self.height = height

        self.grass_tiles = pg.Surface(
            (grid_x * TILE_SIZE * 2, (grid_y + 2) * TILE_SIZE)
        ).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()

        self.temp_tile = None
        self.examined_tile = None

    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.examined_tile = None
            self.hud.examined_tile = None

        self.temp_tile = None

        hud_select = self.hud.selected_tile

        grid_pos = self.mouse_to_grid(
            mouse_pos[0], mouse_pos[1], camera.scroll
        )
        x = grid_pos[0]
        y = grid_pos[1]

        if hud_select:
            if self.can_place_tile(grid_pos):
                img = hud_select["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[x][y]["render_pos"]
                iso_poly = self.world[x][y]["iso_poly"]
                collision = self.world[x][y]["collision"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision,
                }

                if hud_select["name"] == "delete":
                    if mouse_action[0] and collision:
                        self.world[x][y]["tile"] = ""
                        self.world[x][y]["collision"] = False
                else:
                    if mouse_action[0] and not collision:
                        self.world[x][y]["tile"] = hud_select["name"]
                        self.world[x][y]["collision"] = True
        else:
            if self.can_place_tile(grid_pos):
                collision = self.world[x][y]["collision"]

                if mouse_action[0] and collision:
                    self.examined_tile = grid_pos
                    self.hud.examined_tile = self.world[x][y]

    def draw(self, screen, camera):
        scroll_x = camera.scroll.x
        scroll_y = camera.scroll.y

        grass_width = self.grass_tiles.get_width()

        # grass tiles
        screen.blit(self.grass_tiles, (scroll_x, scroll_y))

        for x in range(self.grid_x):
            for y in range(self.grid_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                if tile != "":
                    ren_x = render_pos[0]
                    ren_y = render_pos[1]
                    tile_height = self.tiles[tile].get_height() / 2
                    screen.blit(
                        self.tiles[tile],
                        (
                            ren_x + grass_width / 2 + scroll_x,
                            ren_y - tile_height + 8 + TILE_SIZE + scroll_y,
                        ),
                    )
                    if self.examined_tile:
                        if (x == self.examined_tile[0]) and (
                            y == self.examined_tile[1]
                        ):
                            mask = pg.mask.from_surface(
                                self.tiles[tile]
                            ).outline()
                            mask_x = ren_x + grass_width / 2 + scroll_x
                            mask_y = (
                                ren_y - tile_height + 8 + TILE_SIZE + scroll_y
                            )
                            mask = [(x + mask_x, y + mask_y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)

        # draw build tile temp
        if self.temp_tile != None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [
                (x + grass_width / 2 + scroll_x, y + scroll_y)
                for x, y in iso_poly
            ]

            if self.hud.selected_tile["name"] == "delete":
                if self.temp_tile["collision"]:
                    pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
                else:
                    pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                if self.temp_tile["collision"]:
                    pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
                else:
                    pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)

            render_pos = self.temp_tile["render_pos"]

            dest_x = render_pos[0] + grass_width / 2 + scroll_x
            dest_y = (
                render_pos[1]
                - self.temp_tile["image"].get_height()
                + TILE_SIZE
                + scroll_y
            )
            screen.blit(self.temp_tile["image"], (dest_x, dest_y))

    def create_world(self):
        world = []

        for x in range(self.grid_x):
            world.append([])
            for y in range(self.grid_y):
                world_tile = self.grid_to_world(x, y)
                world[x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(
                    self.tiles["block"],
                    (
                        render_pos[0] + self.grass_tiles.get_width() / 2,
                        render_pos[1],
                    ),
                )

        return world

    def grid_to_world(self, x, y):
        rect = [
            (x * TILE_SIZE, y * TILE_SIZE),
            (x * TILE_SIZE + TILE_SIZE, y * TILE_SIZE),
            (x * TILE_SIZE + TILE_SIZE, y * TILE_SIZE + TILE_SIZE),
            (x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE),
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        min_x = min([x for x, _ in iso_poly])
        min_y = min([y for _, y in iso_poly])

        out = {
            "grid": [x, y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [min_x, min_y],
            "tile": "",
            "collision": False,
        }

        return out

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position => screen pos - scroll pos - offset
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to cartesian
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)

        return grid_x, grid_y

    def load_images(self):
        w = self.hud.build_surface.get_width() // 5

        block = pg.image.load("assets/tiles/block.png").convert_alpha()
        road = pg.image.load("assets/tiles/road_tile.png")
        residential = pg.image.load("assets/tiles/residential_tile.png")
        commercial = scale_image(pg.image.load("assets/commercial.png"), w=w)
        industrial = scale_image(pg.image.load("assets/industrial.png"), w=w)
        fire = pg.image.load("assets/tiles/fire_tile.png")
        police = pg.image.load("assets/tiles/police_tile.png")
        health = pg.image.load("assets/tiles/health_tile.png")

        images = {
            "block": block,
            "road": road,
            "residential": residential,
            "commercial": commercial,
            "industrial": industrial,
            "fire": fire,
            "police": police,
            "health": health,
        }

        return images

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2

        return iso_x, iso_y

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False

        for rect in [self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        world_bounds = (0 <= grid_pos[0] <= self.grid_x) and (
            0 <= grid_pos[1] <= self.grid_y
        )

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False
