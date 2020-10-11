# ABSTRACT ART GENERATOR
# By Burak U. - github.com/Burakcoli

from color_palettes import Palette
from random import randint
import pygame as pg
import pygame.gfxdraw
import pygame.freetype
import pygame_gui as pgui
from tkinter import *
from tkinter.filedialog import asksaveasfilename

pg.init()
pg.freetype.init()

SW, SH = 1280, 720
window = pg.display.set_mode((SW, SH))
ui_manager = pgui.UIManager((SW, SH))
pg.display.set_caption("Abstract Art Generator")

logo = pg.image.load("assets/logo.png")
pg.display.set_icon(logo)

background_color = pg.Color("#322f3d")

xs_font = pg.freetype.Font("Basic-Regular.ttf", 12)
small_font = pg.freetype.Font("Basic-Regular.ttf", 14)
medium_font = pg.freetype.Font("Basic-Regular.ttf", 18)
large_font = pg.freetype.Font("Basic-Regular.ttf", 24)
xl_font = pg.freetype.Font("Basic-Regular.ttf", 30)
xxl_font = pg.freetype.Font("Basic-Regular.ttf", 40)

fonts = [xs_font, small_font, medium_font, large_font, xl_font, xxl_font]
font_sizes = [12, 14, 18, 24, 30, 40]


def text_to_screen(window, text, color, pos, font_size):
    font_used = fonts[font_sizes.index(font_size)]
    font_used.render_to(window, pos, text, color)


active_overlay = 0
overlays = [
    pg.image.load("assets/overlay1.png").convert_alpha(),
    pg.image.load("assets/overlay2.png").convert_alpha(),
    pg.image.load("assets/overlay3.png").convert_alpha(),
    pg.image.load("assets/overlay4.png").convert_alpha(),
    pg.image.load("assets/overlay5.png").convert_alpha(),
    pg.image.load("assets/overlay6.png").convert_alpha()
]

art_styles_list = [
    "Chaotic",
    "Striped Horizontal",
    "Striped Vertical",
    "Mosaic",
    "Cornered",
    "Centered",
    "Empty"
]

art_shapes_list = [
    "Lines",
    "Circles",
    "Squares",
    "Hollow Polygons",
    "Filled Polygons",
    "Dots",
    "Curves",
    "Rings"
]

resolutions_list = [
    "4K: 3840x2160",
    "Full HD: 1920x1080",
    "HD: 1280x720"
]


class Canvas:
    def __init__(self, size, display_size):
        self.width = size[0]
        self.height = size[1]
        self.display_size = display_size
        self.sPos = ((SW - self.width) // 2, (SH - self.height) // 2)
        self.dsPos = ((SW - self.display_size[0])//2 + 10, (SH-self.display_size[1])//2)
        self.canvas = pg.Surface((self.width, self.height))
        self.canvas.fill((255, 255, 255))
        self.display_canvas = pg.Surface(self.display_size)

        self.bg_layer = pg.Surface((self.width, self.height))
        self.bg_layer.fill((255, 255, 255))
        self.layer_one = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.layer_two = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.fg_layer = pg.Surface((self.width, self.height), pg.SRCALPHA)

    def export_art(self):
        tkinter_window = Tk()
        tkinter_window.withdraw()

        available_formats = [("Portable Network Graphics", "*.png")]
        filename = asksaveasfilename(title="Export File", filetypes=available_formats)

        if filename:
            name = filename[:]
            return name

    def clean_all_layers(self):
        self.layer_one.fill((0, 0, 0, 0))
        self.layer_two.fill((0, 0, 0, 0))

    def clean_layer(self, layer):
        layer.fill((0, 0, 0, 0))

    def generate_lines(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity):
                posX = (randint(-200, self.width+200), randint(0, self.width))
                posY = (randint(-200, self.height+200), randint(0, self.height))
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size//4)
        elif style == art_styles_list[1]:   # Striped Horizontal
            interval = self.height // complexity
            for i in range(complexity):
                posX = 0, self.width
                posY = i * interval + randint(0, self.height//10), i * interval + randint(0, self.height//10)
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size // 4)
        elif style == art_styles_list[2]:   # Striped Vertical
            interval = self.width // complexity
            for i in range(complexity):
                posY = 0, self.height
                posX = i * interval + randint(0, self.width//10), i * interval + randint(0, self.width//10)
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size // 4)
        elif style == art_styles_list[3]:   # Mosaic
            row_line_count = complexity // 3 + 1
            row_count = complexity // 4 + 1
            x_interval = self.width // (row_line_count - 1)
            y_interval = self.height // (row_count - 1)
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_line_count):
                    current_color = color_one if (i+j) % 2 == 0 else color_two
                    size = randint(magnitude[0], magnitude[1]) // 4
                    posX = ((x_interval*j), (x_interval*(j+1)))
                    posY_u = ((y_interval*i), (y_interval*(i+1)))
                    posY_d = ((y_interval*(i+1)), (y_interval*i))
                    if randint(0,1) == 0:
                        pg.draw.line(layer, pg.Color(current_color), (posX[0], posY_u[0]), (posX[1], posY_u[1]), size)
                    else:
                        pg.draw.line(layer, pg.Color(current_color), (posX[0], posY_d[0]), (posX[1], posY_d[1]), size)

        elif style == art_styles_list[4]:   # Cornered
            for i in range(complexity*2):
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1]) // 4
                corner = randint(0, 3)
                first_x_area, second_x_area = 0, 0
                first_y_area, second_y_area = 0, 0
                if corner == 0:
                    first_x_area, second_x_area = (-50, 100), (0, self.width//2)
                    first_y_area, second_y_area = (-50, 100), (0, self.height//2)
                elif corner == 1:
                    first_x_area, second_x_area = (self.width-100, self.width+50), (self.width//2, self.width)
                    first_y_area, second_y_area = (-50, 100), (0, self.height // 2)
                elif corner == 2:
                    first_x_area, second_x_area = (self.width-100, self.width+50), (self.width//2, self.width)
                    first_y_area, second_y_area = (self.height-100, self.height+50), (self.height//2, self.height)
                elif corner == 3:
                    first_x_area, second_x_area = (-50, 100), (0, self.width // 2)
                    first_y_area, second_y_area = (self.height-100, self.height+50), (self.height//2, self.height)

                posX = (randint(first_x_area[0], first_x_area[1]), randint(second_x_area[0], second_x_area[1]))
                posY = (randint(first_y_area[0], first_y_area[1]), randint(second_y_area[0], second_y_area[1]))

                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size)
        elif style == art_styles_list[5]:   # Centered
            for i in range(complexity//2):
                current_color = cp[randint(0, len(cp)-1)]
                posX = (randint(2*self.width//5, 3*self.width//5), randint(0, self.width))
                posY = (randint(2*self.height//5, 3*self.height//5), randint(0, self.height))
                size = randint(magnitude[0], magnitude[1]) // 4
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size)
        elif style == art_styles_list[6]:   # Empty, do not draw anything.
            pass

    def generate_squares(self, complexity, cp, style, layer, magnitude):

        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity*2):
                size = randint(magnitude[0], magnitude[1])
                posX = randint(-size, self.width)
                posY = randint(-size, self.height)
                current_color = cp[randint(0, len(cp)-1)]
                pg.draw.rect(layer, pg.Color(current_color), (posX, posY, size, size))

        if style == art_styles_list[1]:     # Striped Horizontal
            row_square_count = complexity // 2 + 2
            point = self.width // (row_square_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                if i % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_square_count):
                    posX = j * point
                    posY = i * point
                    size = randint(magnitude[0], magnitude[1])
                    if i % 2 == 0:
                        pg.draw.rect(layer, pg.Color(current_color),(posX, posY, size, size))

        if style == art_styles_list[2]:     # Striped Vertical
            row_square_count = complexity // 2 + 2
            point = self.width // (row_square_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_square_count):
                    if j % 1 == 0:
                        current_color = color_one if current_color == color_two else color_two
                    posX = j * point
                    posY = i * point
                    size = randint(magnitude[0], magnitude[1])
                    if j % 2 == 0:
                        pg.draw.rect(layer, pg.Color(current_color), (posX-size//2, posY-size//2, size, size))

        if style == art_styles_list[3]:     # Mosaic
            row_square_count = complexity//2 + 2
            size = self.width // (row_square_count-2)
            row_count = self.height // size + 2
            color_one = cp[randint(0, len(cp)-1)]
            color_two = cp[randint(0, len(cp)-1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_square_count):
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    posX = j * size
                    posY = i * size
                    pg.draw.rect(layer, pg.Color(current_color), (posX+size//20, posY+size//20, size-size//10, size-size//10))

        if style == art_styles_list[4]:     # Cornered
            for corner in range(4):
                corner_color = cp[randint(0, len(cp)-1)]
                if corner == 0:
                    pg.draw.rect(layer, pg.Color(corner_color), (0, 0, magnitude[1], magnitude[1]))
                if corner == 1:
                    pg.draw.rect(layer, pg.Color(corner_color), (self.width-magnitude[1], 0, magnitude[1], magnitude[1]))
                if corner == 2:
                    pg.draw.rect(layer, pg.Color(corner_color), (self.width-magnitude[1], self.height-magnitude[1], magnitude[1], magnitude[1]))
                if corner == 3:
                    pg.draw.rect(layer, pg.Color(corner_color), (0, self.height-magnitude[1], magnitude[1], magnitude[1]))

            for i in range(complexity*3):
                current_color = cp[randint(0, len(cp)-1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (-magnitude[1]//2, self.width//3), (-magnitude[1]//2, self.height//2-magnitude[1])
                if corner == 1:
                    x_area, y_area = (2*self.width//3-magnitude[1], self.width), (-magnitude[1]//2, self.height//2-magnitude[1])
                if corner == 2:
                    x_area, y_area = (2*self.width//3-magnitude[1], self.width), (self.height//2, self.height)
                if corner == 3:
                    x_area, y_area = (-magnitude[1], self.width//3), (self.height//2, self.height)

                posX = randint(x_area[0], x_area[1])
                posY = randint(y_area[0], y_area[1])
                size = randint(magnitude[0], magnitude[1])

                pg.draw.rect(layer, pg.Color(current_color), (posX, posY, size, size))

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width // 4, 3 * self.width // 4), (self.height // 4, 3 * self.height // 4)
            out_x_area, out_y_area = (self.width // 6, 5 * self.width // 6), (self.height // 6, 5 * self.height // 6)

            for i in range(complexity):
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                size = randint(magnitude[0], magnitude[1])
                current_color = cp[randint(0, len(cp) - 1)]

                pg.draw.rect(layer, pg.Color(current_color), (center_x-size//2, center_y-size//2, size, size))
        if style == art_styles_list[6]:     # Empty
            pass

    def generate_circles(self, complexity, cp, style, layer, magnitude, fill):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity):
                rad = randint(magnitude[0], magnitude[1])
                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0
                centerX = randint(-25, self.width + 25)
                centerY = randint(-25, self.height + 25)
                current_color = cp[randint(0, len(cp) - 1)]
                alpha_surface = pg.Surface((rad*2, rad*2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (centerX-rad, centerY-rad))

        if style == art_styles_list[1]:     # Striped Horizontal
            row_circle_count = complexity // 2 + 2
            point = self.width // (row_circle_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                if i % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_circle_count):
                    posX = j * point
                    posY = i * point
                    rad = randint(magnitude[0], magnitude[1])
                    if fill == 1:
                        fill_type = randint(5, rad // 2)
                    else:
                        fill_type = 0
                    if i % 2 == 0:
                        alpha_surface = pg.Surface((rad * 2, rad * 2))
                        alpha_surface.fill((0, 0, 0))
                        pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                        alpha_surface.set_colorkey((0, 0, 0))
                        alpha_surface.set_alpha(randint(150, 255))
                        layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[2]:  # Striped Vertical
            row_circle_count = complexity // 2 + 2
            point = self.width // (row_circle_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_circle_count):
                    if (j+1) % 2 == 0:
                        current_color = color_one if current_color == color_two else color_two
                    posX = j * point
                    posY = i * point
                    rad = randint(magnitude[0], magnitude[1])
                    if fill == 1:
                        fill_type = randint(5, rad // 2)
                    else:
                        fill_type = 0
                    if j % 2 == 0:
                        alpha_surface = pg.Surface((rad * 2, rad * 2))
                        alpha_surface.fill((0, 0, 0))
                        pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                        alpha_surface.set_colorkey((0, 0, 0))
                        alpha_surface.set_alpha(randint(150, 255))
                        layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[3]:     # Mosaic
            row_circle_count = complexity
            rad = self.width // row_circle_count
            row_count = self.height // rad + 1
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_circle_count):
                    if fill == 1:
                        fill_type = rad//4
                    else:
                        fill_type = 0
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    posX = rad + j * (rad+1) * 2
                    posY = rad + i * (rad+1) * 2
                    pg.draw.circle(layer, pg.Color(current_color), (posX, posY), rad, fill_type)

        if style == art_styles_list[4]:     # Cornered
            for i in range(complexity*2):
                current_color = cp[randint(0, len(cp)-1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (-50, self.width//3), (-50, self.height//3)
                if corner == 1:
                    x_area, y_area = (self.width//1.5, self.width+50), (-50, self.height//3)
                if corner == 2:
                    x_area, y_area = (self.width//1.5, self.width+50), (self.height//1.5, self.height+50)
                if corner == 3:
                    x_area, y_area = (-50, self.width//3), (self.height//1.5, self.height+50)

                posX = randint(x_area[0], x_area[1])
                posY = randint(y_area[0], y_area[1])
                rad = randint(magnitude[0], magnitude[1])

                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0

                alpha_surface = pg.Surface((rad * 2, rad * 2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width//4, 3*self.width//4), (self.height//4, 3*self.height//4)
            out_x_area, out_y_area = (self.width//6, 5*self.width//6), (self.height//6, 5*self.height//6)

            for i in range(complexity):
                if fill == 1:
                    fill_type = randint(magnitude[0], magnitude[1])
                else:
                    fill_type = 0
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                rad = randint(magnitude[0], magnitude[1])
                current_color = cp[randint(0, len(cp)-1)]

                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0

                alpha_surface = pg.Surface((rad * 2, rad * 2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (center_x - rad, center_y - rad))

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_polygons(self, complexity, cp, style, layer, magnitude, fill):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity//2):
                current_color = cp[randint(0, len(cp)-1)]
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0]//5, magnitude[1]//5)
                points_count = randint(3, 5)
                points = []
                first_point = [randint(0, self.width), randint(0, self.height)]
                for _ in range(points_count):
                    points.append([randint(first_point[0]-magnitude[1]*2, first_point[0]+magnitude[1]*2),
                                   randint(first_point[1]-magnitude[1]*2, first_point[1]+magnitude[1]*2)])

                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[1]:     # Striped Horizontal
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            for i in range(row_count):
                if (i + 1) % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = randint(3, 5)
                    points = []
                    if (i + 1) % 2 == 0:
                        for k in range(point_count):
                            points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                        pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[2]:     # Striped Vertical
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            for i in range(row_count):
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = randint(3, 5)
                    points = []
                    if j % 2 == 0:
                        current_color = color_one if current_color == color_two else color_two
                        for k in range(point_count):
                            points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                        pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[3]:     # Mosaic
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    x_area = (x_interval*j, x_interval*(j+1))
                    y_area = (y_interval*i, y_interval*(i+1))
                    point_count = randint(3, 5)
                    points = []
                    for k in range(point_count):
                        points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                    pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[4]:     # Cornered
            x_areas = [(-100, self.width//3), (2*self.width//3, self.width+100),
                       (2*self.width//3, self.width+100), (-100, self.width//3)]

            y_areas = [(-100, self.height//2-50), (-100, self.height//2-100),
                       (self.height//2+100, self.height+100), (self.height//2+100, self.height+100)]

            point_count = randint(3, 5)
            for i in range(complexity//2):
                corner = randint(0, 3)
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)
                current_color = cp[randint(0, len(cp)-1)]
                points = []
                for j in range(point_count):
                    pos = (randint(x_areas[corner][0], x_areas[corner][1]),
                           randint(y_areas[corner][0], y_areas[corner][1]))
                    points.append(pos)

                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[5]:     # Centered
            x_inner_area = [self.width // 4, 3 * self.width // 4]
            x_outer_area = [self.width // 6, 5 * self.width // 6]
            y_area = [self.height // 4, 3 * self.height // 4]
            for i in range(complexity // 4):
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                current_color = cp[randint(0, len(cp)-1)]

                point_count = randint(3, 4)
                points = []
                for j in range(point_count):
                    if randint(0, 6) <= 4:
                        pos = (randint(x_inner_area[0], x_inner_area[1]), randint(y_area[0], y_area[1]))
                    else:
                        pos = (randint(x_outer_area[0], x_outer_area[1]), randint(y_area[0], y_area[1]))

                    points.append(pos)
                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_curves(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:
            multiples = magnitude // 5
            for i in range(complexity//5):
                current_color = cp[randint(0, len(cp)-1)]
                point_count = 5
                multiples_points = []
                for _ in range(multiples):
                    multiples_points.append([])
                for j in range(point_count):
                    x = randint(0, self.width)
                    y = randint(0, self.height)
                    for k in range(multiples):
                        multiples_points[k].append((x, y+k))

                for k in range(multiples):
                    pg.gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[1]:     # Striped Horizontal
            multiples = magnitude // 5
            point_count = 5
            row_count = complexity // 2
            interval_y = (self.height // row_count)
            interval_x = (self.width // point_count)
            row_color_one = cp[randint(0, len(cp)-1)]
            row_color_two = cp[randint(0, len(cp)-1)]

            for i in range(row_count):
                current_color = row_color_one if i % 2 == 0 else row_color_two

                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([])

                for j in range(point_count+2):
                    y_pos = randint(((i-2)*interval_y), ((i+2)*interval_y) )
                    x_pos = randint((j-1)*interval_x, (j*interval_x))
                    for k in range(multiples):
                        multiples_points[k].append((x_pos, y_pos+k))

                for k in range(multiples):
                    pg.gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[2]:     # Striped Vertical
            point_count = 5
            col_count = complexity // 2
            multiples = magnitude // 5
            interval_x = (self.height // col_count) * 2
            interval_y = (self.width // point_count)
            col_color_one = cp[randint(0, len(cp)-1)]
            col_color_two = cp[randint(0, len(cp)-1)]

            for i in range(col_count):
                current_color = col_color_one if i % 2 == 0 else col_color_two

                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([])

                for j in range(point_count+2):
                    y_pos = randint((j-1)*interval_y, j*interval_y)
                    x_pos = randint((i-1)*interval_x, (i+1)*interval_x)
                    for k in range(multiples):
                        multiples_points[k].append((x_pos+k, y_pos))

                for k in range(multiples):
                    pg.gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[3]:     # Mosaic
            row_curve_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_curve_count
            y_interval = self.height // row_count
            multiples = magnitude // 5
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_curve_count):
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = 4
                    multiples_points = []
                    for m in range(multiples):
                        multiples_points.append([])

                    for k in range(point_count):
                        x = randint(x_area[0], x_area[1])
                        y = randint(y_area[0], y_area[1])
                        for m in range(multiples):
                            multiples_points[m].append((x, y+m))

                    for m in range(multiples):
                        pg.gfxdraw.bezier(layer, multiples_points[m], 5, pg.Color(current_color))

        if style == art_styles_list[4]:     # Cornered
            corner_starts = [((0, self.width//3),(-1, 0)),
                             ((2*self.width//3, self.width),(-1, 0)),
                             ((2*self.width//3, self.width),(self.height, self.height+1)),
                             ((0, self.width//3),(self.height, self.height+1))]
            corner_ends = [((-1, 0),(0, self.height//2)),
                           ((self.width, self.width+1),(0, self.height//2)),
                           ((self.width, self.width+1),(self.height//2, self.height)),
                           ((-1, 0),(self.height//2, self.height))]
            multiples = magnitude // 5
            point_count = 2
            x_area = [0, 0]
            y_area = [0, 0]
            for i in range(complexity//2):
                corner = randint(0, 3)

                if corner == 0: x_area = [0, self.width//3]; y_area = [0, self.height//2]
                if corner == 1: x_area = [2*self.width//3, self.width]; y_area = [0, self.height//2]
                if corner == 2: x_area = [2*self.width//3, self.width]; y_area = [self.height//2, self.height]
                if corner == 3: x_area = [0, self.width//3]; y_area = [self.height//2, self.height]

                current_color = cp[randint(0, len(cp)-1)]

                multiples_points = []
                first_point = (randint(corner_starts[corner][0][0], corner_starts[corner][0][1]),
                               randint(corner_starts[corner][1][0], corner_starts[corner][1][1]))
                last_point = (randint(corner_ends[corner][0][0], corner_ends[corner][0][1]),
                              randint(corner_ends[corner][1][0], corner_ends[corner][1][1]))
                for k in range(multiples):
                    multiples_points.append([first_point])

                for j in range(point_count):
                    x = randint(x_area[0], x_area[1])
                    y = randint(y_area[0], y_area[1])

                    for k in range(multiples):
                        multiples_points[k].append((x+k, y))
                for k in range(multiples):
                    multiples_points[k].append(last_point)

                for k in range(multiples):
                    pg.gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[5]:     # Centered
            curve_count = complexity // 5
            multiples = magnitude // 5
            point_count = 5
            for i in range(curve_count):
                side = randint(0, 3)
                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([(self.width//2, self.height//2)])

                current_color = cp[randint(0, len(cp)-1)]
                x, y = 0, 0
                for j in range(point_count):
                    if side == 0:
                        x = randint(self.width//2+20*j, self.width)
                        y = randint(0, self.height)
                    elif side == 1:
                        x = randint(0, self.width)
                        y = randint(0, self.height // 2 - 20 * j)
                    elif side == 2:
                        x = randint(0, self.width//2-20*j)
                        y = randint(0, self.height)
                    elif side == 3:
                        x = randint(0, self.width)
                        y = randint(self.height // 2 + 20 * j, self.height)

                    for k in range(multiples):
                        multiples_points[k].append((x, y+k))

                for k in range(multiples):
                    pg.gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_dots(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity*20):
                centerX = randint(-25, self.width + 25)
                centerY = randint(-25, self.height + 25)
                current_color = cp[randint(0, len(cp) - 1)]
                pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[1]:     # Striped Horizontal
            row_dot_count = complexity * 2
            row_count = complexity // 2
            interval = self.height // row_count
            row_colour_one = cp[randint(0, len(cp) - 1)]
            row_colour_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count+1):
                for j in range(row_dot_count):
                    current_color = row_colour_one if i % 2 == 0 else row_colour_two
                    centerY = i * interval + 5
                    centerX = randint(0, self.width)
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[2]:     # Striped Vertical
            row_dot_count = complexity * 2
            row_count = complexity // 2
            interval = self.width // row_count
            row_colour_one = cp[randint(0, len(cp) - 1)]
            row_colour_two = cp[randint(0, len(cp) - 1)]
            while row_colour_two == row_colour_one:
                row_colour_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count+1):
                for j in range(row_dot_count):
                    current_color = row_colour_one if i % 2 == 0 else row_colour_two
                    centerX = i * interval + 5
                    centerY = randint(0, self.width)
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[3]:     # Mosaic
            row_dot_count = complexity * 5
            interval = self.width // row_dot_count * 2
            row_count = self.height // interval + 5
            color_one = cp[randint(0, len(cp)-1)]
            color_two = cp[randint(0, len(cp)-1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_dot_count):
                    current_color = color_one if (i+j) % 2 == 0 else color_two
                    centerX = 2 + j * interval
                    centerY = 2 + i * interval
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[4]:     # Cornered
            for i in range(complexity * 8):
                current_color = cp[randint(0, len(cp) - 1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (0, self.width // 3), (0, self.height // 3)
                if corner == 1:
                    x_area, y_area = (self.width // 1.5, self.width), (0, self.height // 3)
                if corner == 2:
                    x_area, y_area = (self.width // 1.5, self.width), (self.height // 1.5, self.height)
                if corner == 3:
                    x_area, y_area = (0, self.width // 3), (self.height // 1.5, self.height)

                posX = randint(x_area[0], x_area[1])
                posY = randint(y_area[0], y_area[1])

                pg.draw.circle(layer, pg.Color(current_color), (posX, posY), magnitude[1]//30 + 2)

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width // 4, 3 * self.width // 4), (self.height // 4, 3 * self.height // 4)
            out_x_area, out_y_area = (self.width // 6, 5 * self.width // 6), (self.height // 6, 5 * self.height // 6)

            for i in range(complexity * 4):
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                current_color = cp[randint(0, len(cp) - 1)]
                pg.draw.circle(layer, pg.Color(current_color), (center_x, center_y), magnitude[1]//30 + 2)

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_bg(self, color):
        self.bg_layer.fill(pg.Color(color))

    def generate_fg(self, overlay):
        self.clean_layer(self.fg_layer)
        self.fg_layer.blit(overlay, (0, 0))
        self.blit_to_canvas()

    def generate_layer_one(self, art_style, art_shape, color_palette, complexity, magnitude):
        self.generate_art(self.layer_one, art_style, art_shape, color_palette, complexity, magnitude)

    def generate_layer_two(self, art_style, art_shape, color_palette, complexity, magnitude):
        self.generate_art(self.layer_two, art_style, art_shape, color_palette, complexity, magnitude)

    def generate_art(self, layer, art_style, art_shape, color_palette, complexity, magnitude):
        self.clean_layer(layer)
        layer.set_colorkey((0, 0, 0))

        if art_shapes_list[0] == art_shape:
            self.generate_lines(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[1] == art_shape:
            self.generate_circles(complexity, color_palette, art_style, layer, magnitude, 0)

        if art_shapes_list[2] == art_shape:
            self.generate_squares(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[3] == art_shape:
            self.generate_polygons(complexity, color_palette, art_style, layer, magnitude, 1)

        if art_shapes_list[4] == art_shape:
            self.generate_polygons(complexity, color_palette, art_style, layer, magnitude, 0)

        if art_shapes_list[5] == art_shape:
            self.generate_dots(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[6] == art_shape:
            self.generate_curves(complexity, color_palette, art_style, layer, magnitude[1])

        if art_shapes_list[7] == art_shape:
            self.generate_circles(complexity, color_palette, art_style, layer, magnitude, 1)

    def blit_to_canvas(self):
        self.canvas.blit(self.bg_layer, (0, 0))
        self.canvas.blit(self.layer_one, (0, 0))
        self.canvas.blit(self.layer_two, (0, 0))
        self.canvas.blit(self.fg_layer, (0, 0))
        self.canvas.convert()
        self.display_canvas = pg.transform.smoothscale(self.canvas, self.display_size)

    def draw(self, window):
        window.blit(self.display_canvas, self.dsPos)


p1 = Palette()
c1 = Canvas((3840, 2160), (int(SW//1.8), int(SH//1.8)))

current_color_palette = p1.get_random_palette()
current_palette_name = p1.get_name_of_palette(current_color_palette)
layer_one_style = "Striped Vertical"
layer_one_shape = "Lines"
layer_two_style = "Cornered"
layer_two_shape = "Rings"
layer_one_complexity = 15
layer_two_complexity = 15
layer_one_magnitude = [50, 400]
layer_two_magnitude = [50, 400]

option_locks = [0, 0, 0, 0, 0, 0, 0, 0, 0]

help_opt = 0

export_resolution = resolutions_list[0]


def draw_menu(window, color_palette, option_locks, help_opt):
    ui_h1_color = (250, 250, 250)
    ui_color = pg.Color("#DFD6FF")

    lock_enabled = pg.transform.scale(pg.image.load("assets/lock_enabled.png"), (20, 20))
    lock_disabled = pg.transform.scale(pg.image.load("assets/lock_disabled.png"), (20, 20))

    pg.draw.rect(window, pg.Color("#2B2834"), (18, 90, 252, 95))        # Color Palette BG
    pg.draw.rect(window, pg.Color("#2B2834"), (18, 195, 252, 190))      # Layer One BG
    pg.draw.rect(window, pg.Color("#2B2834"), (18, 395, 252, 190))      # Layer Two BG

    lock_position = 35

    if option_locks[0] == 0:
        window.blit(lock_disabled, (lock_position, 125))
    else:
        window.blit(lock_enabled, (lock_position, 125))

    if option_locks[1] == 0:
        window.blit(lock_disabled, (lock_position, 225))
    else:
        window.blit(lock_enabled, (lock_position, 225))

    if option_locks[2] == 0:
        window.blit(lock_disabled, (lock_position, 255))
    else:
        window.blit(lock_enabled, (lock_position, 255))

    if option_locks[3] == 0:
        window.blit(lock_disabled, (lock_position, 305))
    else:
        window.blit(lock_enabled, (lock_position, 305))

    if option_locks[4] == 0:
        window.blit(lock_disabled, (lock_position, 355))
    else:
        window.blit(lock_enabled, (lock_position, 355))

    if option_locks[5] == 0:
        window.blit(lock_disabled, (lock_position, 425))
    else:
        window.blit(lock_enabled, (lock_position, 425))

    if option_locks[6] == 0:
        window.blit(lock_disabled, (lock_position, 455))
    else:
        window.blit(lock_enabled, (lock_position, 455))

    if option_locks[7] == 0:
        window.blit(lock_disabled, (lock_position, 505))
    else:
        window.blit(lock_enabled, (lock_position, 505))

    if option_locks[8] == 0:
        window.blit(lock_disabled, (lock_position, 555))
    else:
        window.blit(lock_enabled, (lock_position, 555))

    text_to_screen(window=window, text="ABSTRACT ART GENERATOR", color=ui_h1_color, pos=(430, 35), font_size=40)
    text_to_screen(window=window, text="OPTIONS", color=ui_h1_color, pos=(60, 65), font_size=24)
    text_to_screen(window=window, text="COLOR PALETTE", color=ui_h1_color, pos=(60, 105), font_size=18)
    for i, color in enumerate(color_palette):
        pg.draw.rect(window, (0, 0, 0), (60+(i*50), 155, 26, 26))
        pg.draw.rect(window, pg.Color(color), (63+(i*50), 158, 20, 20))
    text_to_screen(window=window, text="LAYER ONE STYLE", color=ui_h1_color, pos=(60, 205), font_size=18)
    text_to_screen(window=window, text="LAYER ONE COMPLEXITY", color=ui_color, pos=(60, 290), font_size=14)
    text_to_screen(window=window, text="LAYER ONE SHAPE SIZE", color=ui_color, pos=(60, 340), font_size=14)
    text_to_screen(window=window, text="LAYER TWO STYLE", color=ui_h1_color, pos=(60, 405), font_size=18)
    text_to_screen(window=window, text="LAYER TWO COMPLEXITY", color=ui_color, pos=(60, 490), font_size=14)
    text_to_screen(window=window, text="LAYER TWO SHAPE SIZE", color=ui_color, pos=(60, 540), font_size=14)

    text_to_screen(window=window, text="OVERLAY", color=ui_h1_color, pos=(SW-190, 160), font_size=24)

    text_to_screen(window=window, text="RESOLUTION", color=ui_color, pos=(SW-240, 560), font_size=14)

    pg.draw.rect(window, pg.Color("#2B2834"), (SW-245, 190, 210, 320))

    active_color = (90, 90, 90)
    inactive_color = (20, 20, 20)

    pg.draw.rect(window, active_color if active_overlay == 1 else inactive_color, (SW-232, 198, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 2 else inactive_color, (SW-132, 198, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 3 else inactive_color, (SW-232, 278, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 4 else inactive_color, (SW-132, 278, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 5 else inactive_color, (SW-232, 358, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 6 else inactive_color, (SW-132, 358, 84, 49), 1)
    pg.draw.rect(window, active_color if active_overlay == 0 else inactive_color, (SW-182, 438, 84, 49), 1)

    window.blit(pg.transform.scale(overlays[0], (80, 45)), (SW-230, 200))
    window.blit(pg.transform.scale(overlays[1], (80, 45)), (SW-130, 200))
    window.blit(pg.transform.scale(overlays[2], (80, 45)), (SW-230, 280))
    window.blit(pg.transform.scale(overlays[3], (80, 45)), (SW-130, 280))
    window.blit(pg.transform.scale(overlays[4], (80, 45)), (SW-230, 360))
    window.blit(pg.transform.scale(overlays[5], (80, 45)), (SW-130, 360))


def generate_ui():
    ui_manager.clear_and_reset()
    lm = 60     # Left margin

    current_palette_dropdown = pgui.elements.UIDropDownMenu(options_list=p1.get_all_names(),
                                                            starting_option=current_palette_name,
                                                            relative_rect=pg.Rect(lm, 125, 200, 22), manager=ui_manager,
                                                            object_id="current_palette_dropdown")

    layer_one_style_dropdown = pgui.elements.UIDropDownMenu(options_list=art_styles_list,
                                                            starting_option=layer_one_style,
                                                            relative_rect=pg.Rect(lm, 225, 200, 22), manager=ui_manager,
                                                            object_id="layer_one_style_dropdown")

    layer_one_shape_dropdown = pgui.elements.UIDropDownMenu(options_list=art_shapes_list,
                                                            starting_option=layer_one_shape,
                                                            relative_rect=pg.Rect(lm, 255, 200, 22), manager=ui_manager,
                                                            object_id="layer_one_shape_dropdown")

    layer_one_complexity_slider = pgui.elements.UIHorizontalSlider(relative_rect=pg.Rect(lm, 305, 200, 22),
                                                                   start_value=layer_one_complexity,
                                                                   value_range=(10, 30), manager=ui_manager,
                                                                   object_id="layer_one_complexity_slider")

    layer_one_size_slider = pgui.elements.UIHorizontalSlider(relative_rect=pg.Rect(lm, 355, 200, 22),
                                                             start_value=layer_one_magnitude[1], value_range=(50, 400),
                                                             manager=ui_manager, object_id="layer_one_size_slider")

    layer_two_style_dropdown = pgui.elements.UIDropDownMenu(options_list=art_styles_list,
                                                            starting_option=layer_two_style,
                                                            relative_rect=pg.Rect(lm, 425, 200, 22), manager=ui_manager,
                                                            object_id="layer_two_style_dropdown")

    layer_two_shape_dropdown = pgui.elements.UIDropDownMenu(options_list=art_shapes_list,
                                                            starting_option=layer_two_shape,
                                                            relative_rect=pg.Rect(lm, 455, 200, 22), manager=ui_manager,
                                                            object_id="layer_two_shape_dropdown")

    resolution_dropdown = pgui.elements.UIDropDownMenu(options_list=resolutions_list,
                                                       starting_option=export_resolution,
                                                       relative_rect=pg.Rect(SW-240, 575, 200, 22), manager=ui_manager,
                                                       object_id = "resolution_dropdown")

    layer_two_complexity_slider = pgui.elements.UIHorizontalSlider(relative_rect=pg.Rect(lm, 505, 200, 22),
                                                                   start_value=layer_two_complexity,
                                                                   value_range=(10, 30), manager=ui_manager,
                                                                   object_id="layer_two_complexity_slider")

    layer_two_size_slider = pgui.elements.UIHorizontalSlider(relative_rect=pg.Rect(lm, 555, 200, 22),
                                                             start_value=layer_two_magnitude[1], value_range=(50, 400),
                                                             manager=ui_manager, object_id="layer_two_size_slider")

    export_art_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW - 240, SH - 100, 200, 50),
                                               text="Export", manager=ui_manager, object_id="export_art_button")

    generate_button = pgui.elements.UIButton(relative_rect=pg.Rect(lm, SH - 100, 200, 50),
                                             text="Generate", manager=ui_manager, object_id="generate_button")

    random_generate_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW // 2 - 100, SH - 100, 200, 50),
                                                    text="Generate Randomly", manager=ui_manager,
                                                    object_id="random_generate_button")

    lock_button_one = pgui.elements.UIButton(relative_rect=pg.Rect(24, 132, 12, 12), text="", manager=ui_manager,
                                             object_id="lock_button_one")
    lock_button_two = pgui.elements.UIButton(relative_rect=pg.Rect(24, 232, 12, 12), text="", manager=ui_manager,
                                             object_id="lock_button_two")
    lock_button_three = pgui.elements.UIButton(relative_rect=pg.Rect(24, 262, 12, 12), text="", manager=ui_manager,
                                               object_id="lock_button_three")
    lock_button_four = pgui.elements.UIButton(relative_rect=pg.Rect(24, 312, 12, 12), text="", manager=ui_manager,
                                              object_id="lock_button_four")
    lock_button_five = pgui.elements.UIButton(relative_rect=pg.Rect(24, 362, 12, 12), text="", manager=ui_manager,
                                              object_id="lock_button_five")
    lock_button_six = pgui.elements.UIButton(relative_rect=pg.Rect(24, 432, 12, 12), text="", manager=ui_manager,
                                             object_id="lock_button_six")
    lock_button_seven = pgui.elements.UIButton(relative_rect=pg.Rect(24, 462, 12, 12), text="", manager=ui_manager,
                                               object_id="lock_button_seven")
    lock_button_eight = pgui.elements.UIButton(relative_rect=pg.Rect(24, 512, 12, 12), text="", manager=ui_manager,
                                               object_id="lock_button_eight")
    lock_button_nine = pgui.elements.UIButton(relative_rect=pg.Rect(24, 562, 12, 12), text="", manager=ui_manager,
                                              object_id="lock_button_nine")

    overlay1_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-197, 250, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay1_button")
    overlay2_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-97, 250, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay2_button")
    overlay3_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-197, 330, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay3_button")
    overlay4_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-97, 330, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay4_button")
    overlay5_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-197, 410, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay5_button")
    overlay6_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-97, 410, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay6_button")
    overlay7_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-147, 490, 14, 14), text="", manager=ui_manager,
                                             object_id="overlay7_button")
    help_opt_button = pgui.elements.UIButton(relative_rect=pg.Rect(SW-100, 60, 100, 30), text="HELP", manager=ui_manager,
                                             object_id="help_opt_button")


def draw_help():
    pg.draw.rect(window, pg.Color("#2B2834"), (SW - 610, 90, 510, 380))
    c, p, s = [255, 255, 255], [SW-600, 100], 12     # Color, Position, Font-size
    ri = 12     # Row interval
    text_to_screen(window, "Thanks for trying out my program! Let me help you with how the program works.", c, p, s)
    p = [p[0], p[1]+ri+10]
    text_to_screen(window, "Left side contains the art generation options, we have two layers that can be in different", c, p, s)
    p = [p[0], p[1]+ri]
    text_to_screen(window, "styles, different shapes, different complexities and different sizes. For example a layer", c, p, s)
    p = [p[0], p[1]+ri]
    text_to_screen(window, "with 'Cornered' 'Circles' options, will generate circles that are roughly cornered.", c, p, s)
    p = [p[0], p[1]+ri+10]
    text_to_screen(window, "Random values have a big part in my program to make the possibilities endless", c, p, s)
    p = [p[0], p[1]+ri]
    text_to_screen(window, "If you like a setting and want to keep it but randomize other settings, you can just click", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "on the small buttons right next to the options to 'Lock' them for generating randomly.", c, p, s)
    p = [p[0], p[1] + ri+10]
    c = pg.Color("#DFD6FF")
    text_to_screen(window, "Generate Button: Generates art with the options specified in the options panel.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Generate Randomly Button: Generates art by randomizing the options on the left.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Export Button: Opens a file dialog and let's you export a png of your art in 4k quality.", c, p, s)
    p = [p[0], p[1] + ri+10]
    c = [255, 255, 255]
    text_to_screen(window, "Overlay options don't change by randomizing or generating new art with adjusting the options.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "And you can try new overlays with existing art. ", c, p, s)
    p = [p[0], p[1] + ri+10]
    text_to_screen(window, "There are 20 unique color palettes, and there are seven style options with eight shape options.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Shapes are self explanatory but let's take a look at the styles:", c, p, s)
    p = [p[0], p[1] + ri+5]
    c = pg.Color("#DFD6FF")
    text_to_screen(window, "Chaotic - The most randomized option.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Striped Horizontal - Whatever the shape is, the shapes roughly line up in horizontal lines", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Striped Vertical - Same with striped horizontal but it's vertical.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Mosaic - The selected shape will cover the canvas with equal amount of spacing between them.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Cornered - Forces the randomizer to make the shapes appear roughly on the corners.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Centered - Forces the randomizer to make the shapes appear roughlt on the center.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Empty - Doesn't draw any shapes to the layer. Sometimes one shape is enough for the art.", c, p, s)
    p = [p[0], p[1] + ri+10]
    c = [255, 255, 255]
    text_to_screen(window, "Complexity adjusts how many shapes will be drawn, it's more absolute than the size option.", c, p, s)
    p = [p[0], p[1] + ri]
    text_to_screen(window, "Size option adjusts how large the shapes 'can' be. Size is still more randomized for variety.", c, p, s)
    p = [p[0], p[1] + ri+10]
    c = pg.Color("#DFD6FF")
    text_to_screen(window, "ENJOY!", c, p, s)



generate_ui()

run = True
while run:
    delta_time = pg.time.Clock().tick(60)/1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                c1.generate_fg(overlays[0])
            if event.key == pg.K_2:
                c1.generate_fg(overlays[1])
            if event.key == pg.K_3:
                c1.generate_fg(overlays[2])
            if event.key == pg.K_4:
                c1.generate_fg(overlays[3])
            if event.key == pg.K_ESCAPE:
                run = False
                break

        if event.type == pg.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "generate_button":

                    cp = current_color_palette.copy()
                    bg_color = cp[randint(0, len(cp)-1)]
                    c1.generate_bg(bg_color)
                    cp.remove(bg_color)

                    c1.generate_layer_one(art_style=layer_one_style, art_shape=layer_one_shape,
                                          color_palette=cp, complexity=layer_one_complexity,
                                          magnitude=layer_one_magnitude)
                    c1.generate_layer_two(art_style=layer_two_style, art_shape=layer_two_shape,
                                          color_palette=cp, complexity=layer_two_complexity,
                                          magnitude=layer_two_magnitude)

                    c1.blit_to_canvas()

                if event.ui_object_id == "random_generate_button":
                    if option_locks[0] == 0:
                        current_color_palette = p1.get_random_palette()
                    if option_locks[1] == 0:
                        layer_one_style = art_styles_list[randint(0, len(art_styles_list)-1)]
                    if option_locks[2] == 0:
                        layer_one_shape = art_shapes_list[randint(0, len(art_shapes_list)-1)]
                    if option_locks[3] == 0:
                        layer_one_complexity = randint(10, 30)
                    if option_locks[4] == 0:
                        layer_one_magnitude[1] = randint(51, 400)
                    if option_locks[5] == 0:
                        layer_two_style = art_styles_list[randint(0, len(art_styles_list)-1)]
                    if option_locks[6] == 0:
                        layer_two_shape = art_shapes_list[randint(0, len(art_shapes_list)-1)]
                    if option_locks[7] == 0:
                        layer_two_complexity = randint(10, 30)
                    if option_locks[8] == 0:
                        layer_two_magnitude[1] = randint(51, 400)

                    current_palette_name = p1.get_name_of_palette(current_color_palette)
                    generate_ui()

                    cp = current_color_palette.copy()
                    bg_color = cp[randint(0, len(cp) - 1)]
                    c1.generate_bg(bg_color)
                    cp.remove(bg_color)

                    c1.generate_layer_one(art_style=layer_one_style, art_shape=layer_one_shape,
                                          color_palette=cp, complexity=layer_one_complexity,
                                          magnitude=layer_one_magnitude)
                    c1.generate_layer_two(art_style=layer_two_style, art_shape=layer_two_shape,
                                          color_palette=cp, complexity=layer_two_complexity,
                                          magnitude=layer_two_magnitude)

                    c1.blit_to_canvas()

                if event.ui_object_id == "help_opt_button":
                    help_opt = 1 if help_opt == 0 else 0

                if event.ui_object_id == "export_art_button":
                    path = c1.export_art()
                    if path:
                        if export_resolution == resolutions_list[0]:
                            pg.image.save(c1.canvas, path + ".png")
                        elif export_resolution == resolutions_list[1]:
                            pg.image.save(pg.transform.smoothscale(c1.canvas, (1920, 1080)), path + ".png")
                        elif export_resolution == resolutions_list[2]:
                            pg.image.save(pg.transform.smoothscale(c1.canvas, (1280, 720)), path + ".png")
                    else:
                        pass
                    
                if event.ui_object_id == "lock_button_one":
                    option_locks[0] = 1 if option_locks[0] == 0 else 0
                if event.ui_object_id == "lock_button_two":
                    option_locks[1] = 1 if option_locks[1] == 0 else 0
                if event.ui_object_id == "lock_button_three":
                    option_locks[2] = 1 if option_locks[2] == 0 else 0
                if event.ui_object_id == "lock_button_four":
                    option_locks[3] = 1 if option_locks[3] == 0 else 0
                if event.ui_object_id == "lock_button_five":
                    option_locks[4] = 1 if option_locks[4] == 0 else 0
                if event.ui_object_id == "lock_button_six":
                    option_locks[5] = 1 if option_locks[5] == 0 else 0
                if event.ui_object_id == "lock_button_seven":
                    option_locks[6] = 1 if option_locks[6] == 0 else 0
                if event.ui_object_id == "lock_button_eight":
                    option_locks[7] = 1 if option_locks[7] == 0 else 0
                if event.ui_object_id == "lock_button_nine":
                    option_locks[8] = 1 if option_locks[8] == 0 else 0

                if event.ui_object_id == "overlay1_button":
                    active_overlay = 1
                    c1.generate_fg(overlays[0])
                if event.ui_object_id == "overlay2_button":
                    active_overlay = 2
                    c1.generate_fg(overlays[1])
                if event.ui_object_id == "overlay3_button":
                    active_overlay = 3
                    c1.generate_fg(overlays[2])
                if event.ui_object_id == "overlay4_button":
                    active_overlay = 4
                    c1.generate_fg(overlays[3])
                if event.ui_object_id == "overlay5_button":
                    active_overlay = 5
                    c1.generate_fg(overlays[4])
                if event.ui_object_id == "overlay6_button":
                    active_overlay = 6
                    c1.generate_fg(overlays[5])
                if event.ui_object_id == "overlay7_button":
                    active_overlay = 0
                    c1.clean_layer(c1.fg_layer)
                    c1.blit_to_canvas()

            if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_object_id == "resolution_dropdown":
                    export_resolution = event.text
                if event.ui_object_id == "current_palette_dropdown":
                    current_color_palette = p1.get_colors_from_palette(event.text)
                if event.ui_object_id == "layer_one_style_dropdown":
                    layer_one_style = event.text
                if event.ui_object_id == "layer_one_shape_dropdown":
                    layer_one_shape = event.text
                if event.ui_object_id == "layer_two_style_dropdown":
                    layer_two_style = event.text
                if event.ui_object_id == "layer_two_shape_dropdown":
                    layer_two_shape = event.text

            if event.user_type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_object_id == "layer_one_complexity_slider":
                    layer_one_complexity = event.value
                if event.ui_object_id == "layer_one_size_slider":
                    layer_one_magnitude[1] = event.value
                if event.ui_object_id == "layer_two_complexity_slider":
                    layer_two_complexity = event.value
                if event.ui_object_id == "layer_two_size_slider":
                    layer_two_magnitude[1] = event.value

        ui_manager.process_events(event)

    ui_manager.update(delta_time)
    window.fill(background_color)
    c1.draw(window)
    draw_menu(window, current_color_palette, option_locks, help_opt)
    ui_manager.draw_ui(window)
    if help_opt == 1:
        draw_help()
    pg.display.update()

pg.quit()
