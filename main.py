import arcade
import random

from pers import Pers
from gray_cat import Gray_cat

SCREEN_WIDTH = 740
SCREEN_HEIGHT = 313


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Cat game")
        self.game_over = False

        self.background = arcade.SpriteList()
        for i in range(2):
            background = arcade.Sprite("background.jpg")
            background.center_x = SCREEN_WIDTH // 2 + i * SCREEN_WIDTH
            background.center_y = SCREEN_HEIGHT // 2
            background.width = SCREEN_WIDTH
            background.height = SCREEN_HEIGHT

            self.background.append(background)


        #Sprites
        self.gray_cat = Gray_cat("Cat_85_Animations/Cat_85_Animations/Cat_Grey_White.png",
                                 "Cat_85_Animations/Cat_85_Animations/run",
                                 x=32, y=70,
                                 row_in_picture=7,
                                 FRAME_COUNT=8, FRAME_WIDTH=32, FRAME_HEIGHT=32, scale=2)

        self.cat = arcade.SpriteList()
        self.cat.append(self.gray_cat)

        self.enemies = arcade.SpriteList()

        self.timer = 0
        self.keys_held = set()

        self.enemy_time_gen = [3, 5]
        self.min_enemy_time_gen = [0.3, 0.6]
        self.now_time_enemy_gen = 3
        self.enemy_gen_bag = []

        self.now_enemy_speed = 0.5
        self.max_enemy_speed = 8

        self.enemy_templates = [
            {
                "sprite_path": "Traps/Bear_Trap.png",
                "write_path": "Traps/bear_trap",
                "row_in_picture": 1,
                "FRAME_COUNT": 4,
                "FRAME_WIDTH": 32,
                "FRAME_HEIGHT": 32,
                "y": 50,
                "speed": 0.4,
                "scale": 2
            },
            {
                "sprite_path": "Traps/Bird.png",
                "write_path": "Traps/bird_trap",
                "row_in_picture": 2,
                "FRAME_COUNT": 6,
                "FRAME_WIDTH": 128,
                "FRAME_HEIGHT": 128,
                "y": 65,
                "speed": 0.2,
                "scale": 2
            },
            {
                "sprite_path": "Traps/Grackle.png",
                "write_path": "Traps/grackle_trap",
                "row_in_picture": 2,
                "FRAME_COUNT": 6,
                "FRAME_WIDTH": 128,
                "FRAME_HEIGHT": 128,
                "y": 120,
                "speed": 0.2,
                "scale": 2
            },
            {
                "sprite_path": "Traps/stone.png",
                "write_path": "Traps/stone_trap",
                "row_in_picture": 1,
                "FRAME_COUNT": 1,
                "FRAME_WIDTH": 64,
                "FRAME_HEIGHT": 50,
                "y": 60,
                "speed": 0.4,
                "scale": 1
            },
            {
                "sprite_path": "Traps/tree (1).png",
                "write_path": "Traps/tree_trap",
                "row_in_picture": 1,
                "FRAME_COUNT": 4,
                "FRAME_WIDTH": 64,
                "FRAME_HEIGHT": 64,
                "y": 47,
                "speed": 0.4,
                "scale": 0.8
            }
        ]


    def on_draw(self):
        self.clear()

        self.background.draw()
        self.cat.draw()
        self.enemies.draw()

    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)

        if not self.game_over:
            if key == arcade.key.UP:
                if not self.cat[0].now_jumping:
                    self.cat[0].start_jump()
            if key == arcade.key.DOWN:
                if not self.cat[0].crouch_down and not self.cat[0].crouch_up:
                    self.cat[0].start_crouch_down()
        if self.game_over and key == arcade.key.ENTER:
            self.game_over = False 
            self.enemies.clear() 
           
            self.timer = 0
            self.keys_held = set()

            self.enemy_time_gen = [4, 7]
            self.min_enemy_time_gen = [1, 2]
            self.now_time_enemy_gen = 4

            self.now_enemy_speed = 0.5
            self.max_enemy_speed = 8
            self.cat[0].rise()

    def on_key_release(self, key, modifiers):
        self.keys_held.discard(key)

    def get_next_enemy(self):
        if not self.enemy_gen_bag:
            self.enemy_gen_bag = self.enemy_templates.copy()
            random.shuffle(self.enemy_gen_bag)

        return self.enemy_gen_bag.pop()
    
    def on_update(self, delta_time):
        # Game over
        if self.game_over: 
            self.gray_cat.depth(delta_time) 
            return
        
        # Background
        for bg in self.background:
            bg.center_x -= self.now_enemy_speed
            if bg.center_x < -SCREEN_WIDTH // 2:
                bg.center_x += SCREEN_WIDTH * 2

        # Move
        if arcade.key.RIGHT in self.keys_held:
            if self.gray_cat.center_x < SCREEN_WIDTH - self.gray_cat.width // 2:
                self.gray_cat.move(5)
        if arcade.key.LEFT in self.keys_held:
            if self.gray_cat.center_x > self.gray_cat.width // 2:
                self.gray_cat.move(-5)

        # Enemy generation
        self.timer += delta_time
        if self.timer >= self.now_time_enemy_gen:
            self.timer = 0

            self.now_time_enemy_gen = random.uniform(*self.enemy_time_gen)
            self.enemy_time_gen[0] = max(self.min_enemy_time_gen[0], self.enemy_time_gen[0] - 0.09)
            self.enemy_time_gen[1] = max(self.min_enemy_time_gen[1], self.enemy_time_gen[1] - 0.09)

            self.now_enemy_speed = min(self.max_enemy_speed, self.now_enemy_speed + 0.1)

            template = self.get_next_enemy()
            enemy = Pers(
                sprite_path=template["sprite_path"],
                write_path=template["write_path"],
                x=SCREEN_WIDTH+template["FRAME_WIDTH"],
                y=template["y"],
                row_in_picture=template["row_in_picture"],
                FRAME_COUNT=template["FRAME_COUNT"],
                FRAME_WIDTH=template["FRAME_WIDTH"],
                FRAME_HEIGHT=template["FRAME_HEIGHT"],
                speed=template["speed"],
                scale=template["scale"]
            )

            self.enemies.append(enemy)

        # Enemy move
        for e in self.enemies:
            e.move(-self.now_enemy_speed)
            if e.sprite_path in ("Traps/Bird.png", "Traps/Grackle.png"):
                e.move(-0.5)
            if e.right < 0:
                e.remove_from_sprite_lists()
            

        # Hits
        hit_list = arcade.check_for_collision_with_list(self.gray_cat, self.enemies)
        if hit_list:
            self.game_over = True
            self.gray_cat.start_depth()

        # Animation update
        for c in self.cat:
            c.update_animation(delta_time)
        for e in self.enemies:
            e.update_animation(delta_time)


if __name__ == "__main__":
    MyGame()
    arcade.run()
