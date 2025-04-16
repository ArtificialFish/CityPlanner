import pygame as pg


def draw_text(screen, text, size, color, pos):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


def scale_image(image, w=None, h=None):
    if (w == None) and (h == None):
        pass
    elif h == None:
        scale = w / image.get_width()
        h = scale * image.get_height()
        image = pg.transform.scale(image, (int(w), int(h)))
    elif w == None:
        scale = h / image.get_height()
        w = scale * image.get_width()
        image = pg.transform.scale(image, (int(w), int(h)))
    else:
        image = pg.transform.scale(image, (int(w), int(h)))

    return image
