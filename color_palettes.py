from random import randint

color_palettes = [
    ["#323232", "#295f4e", "#6db193", "#f4e5c2"],
    ["#222831", "#393e46", "#00adb5", "#eeeeee"],
    ["#f9ed69", "#f08a5d", "#b83b5e", "#6a2c70"],
    ["#f85f73", "#fbe8d3", "#928a97", "#283c63"],
    ["#0f1021", "#d01257", "#fb90b7", "#ffcee4"],
    ["#34374c", "#2c2e3e", "#ee2b47", "#f6f6f6"],
    ["#f3f3f3", "#ffdd67", "#ffcd38", "#4a4a4a"],
    ["#8fcfd1", "#df5e88", "#f6ab6c", "#f6efa6"],
    ["#2f2519", "#4a3f35", "#fa7d09", "#ff4301"],
    ["#0c093c", "#df42d1", "#eea5f6", "#fad6d6"],
    ["#f0e3ff", "#d89cf6", "#916dd5", "#3e206d"],
    ["#3c4245", "#5f6769", "#719192", "#dfcdc3"],
    ["#333644", "#84577c", "#c65f63", "#f6e1b8"],
    ["#151716", "#3e432e", "#616f39", "#a7d129"],
    ["#f9f9f9", "#ffe0ac", "#ffacb7", "#6886c5"],
    ["#262626", "#595959", "#b0b0b0", "#e3e3e3"],
    ["#6f4a8e", "#221f3b", "#050505", "#ebebeb"],
    ["#1fab89", "#62d2a2", "#9df3c4", "#d7fbe8"],
    ["#73f7dd", "#2cc4cb", "#1972a4", "#2e3a87"],
    ["#fcf0c8", "#f7d098", "#911f27", "#630a10"]
]

color_palette_names = [
    "Forest",
    "Futuristic",
    "Sunset",
    "Vintage",
    "Crimson",
    "Vampire",
    "Lightning",
    "Pastel",
    "Lava",
    "Neon",
    "Lilac",
    "Soft Gray",
    "Low Saturation",
    "Poison",
    "Spring",
    "Black & White",
    "Corruption",
    "Ivy",
    "Ocean",
    "Royalty"
]


class Palette:
    def __init__(self):
        self.palettes = color_palettes
        self.palette_names = color_palette_names

    def get_random_palette(self):
        return self.palettes[randint(0, len(self.palettes)-1)]

    def get_all_names(self):
        return self.palette_names

    def get_all_palettes(self):
        return self.palettes

    def get_name_of_palette(self, palette):
        return self.palette_names[self.palettes.index(palette)]

    def get_colors_from_palette(self, palette):
        return self.palettes[self.palette_names.index(palette)]