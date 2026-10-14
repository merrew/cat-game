import arcade
from gray_cat import Gray_cat
from pers import *

class Enemy(Pers):
    def __init__(self, type, sprite_path, write_path, x, y, row_in_picture, FRAME_COUNT, FRAME_WIDTH, FRAME_HEIGHT, scale=2):
        super().__init__(sprite_path, write_path, x, y, row_in_picture, FRAME_COUNT, FRAME_WIDTH, FRAME_HEIGHT, scale)

        self.type = type

       
    def check_collisions(cat: Gray_cat):
        if type == "jump":
            if (cat.c)

