import arcade
from PIL import Image
import os
import shutil

# Нарезка спрайт-листа на отдельные картинки
def load_frames(sprite_path, write_path, row, w, h, count):
    image = Image.open(sprite_path)

    frames = []

    if os.path.exists(write_path):
        shutil.rmtree(write_path) 
    os.makedirs(f"{write_path}", exist_ok=True)

    for i in range(count):
        box = (i * w, (row-1)*h, (i + 1) * w, row*h)
        frame = image.crop(box)

        filename = f"{write_path}/frame_{i}.png"
        frame.save(filename)

        tex = arcade.load_texture(filename)
        frames.append(tex)

    return frames


class Pers(arcade.Sprite):
    def __init__(self, sprite_path, write_path, x, y, row_in_picture, FRAME_COUNT, FRAME_WIDTH, FRAME_HEIGHT, scale=2, speed=0.07):
        super().__init__()

        self.sprite_path = sprite_path
        self.write_path = write_path

        self.FRAME_WIDTH = FRAME_WIDTH
        self.FRAME_HEIGHT = FRAME_HEIGHT

        self.frames = load_frames(sprite_path, write_path, row_in_picture, FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT)

        self.texture = self.frames[0]
        self.center_x = x
        self.center_y = y
        self.scale = scale

        self.speed = speed
        self.current_frame = 0
        self.timer = 0

        self.ground = self.center_y

    def change_frame(self, row_in_picture, FRAME_COUNT):
        self.frames = load_frames(self.sprite_path, self.write_path, row_in_picture, self.FRAME_WIDTH, self.FRAME_HEIGHT, FRAME_COUNT)

    def change_pos(self, x, y):
        self.center_x = x
        self.center_y = y
       
    def change_speed(self, speed):
        self.speed = speed;
    
    def move(self, x, y=0):
        self.center_x += x
        self.center_y += y
    
    def update_animation(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame]


