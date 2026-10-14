import arcade
from pers import *

class Gray_cat(Pers):
    def __init__(self, sprite_path, write_path, x, y, row_in_picture, FRAME_COUNT, FRAME_WIDTH, FRAME_HEIGHT, scale=2):
        super().__init__(sprite_path, write_path, x, y, row_in_picture, FRAME_COUNT, FRAME_WIDTH, FRAME_HEIGHT, scale)
        self.animations = {
            "run": {"row": 7, "frames": 8},
            "jump_up": {"row": 33, "frames": 6},
            "jump_down": {"row": 34, "frames": 4},
            "crouch_down": {"row": 63, "frames": 7},
            "crouch_up": {"row": 45, "frames": 8},
            "depth": {"row": 58, "frames": 9}
        }

        # Прыжок
        self.jump_height = 120;

        self.update_y_value = 0

        self.now_jumping = False
        self.fall = False

        # Пригибание
        self.crouch_down = False
        self.crouch_up = False


    def start_jump(self):
        self.now_jumping = True
        
        self.change_frame(self.animations["jump_up"]["row"], self.animations["jump_up"]["frames"])
        self.current_frame = 0
        self.texture = self.frames[0]

        self.update_y_value = self.jump_height / self.animations["jump_up"]["frames"]        

    def start_crouch_down(self):
        self.crouch_down = True

        if not self.now_jumping and not self.fall:
            self.change_frame(self.animations["crouch_down"]["row"], self.animations["crouch_down"]["frames"])
            self.current_frame = 0
            self.texture = self.frames[0]
            self.center_y = self.ground - 7
    
    def start_depth(self):
        self.change_frame(self.animations["depth"]["row"], self.animations["depth"]["frames"])
        self.current_frame = 0
        self.texture = self.frames[0]
        self.update_y_value = (self.ground - self.center_y) / self.animations["depth"]["frames"]
    
    def depth(self, delta_time):
        if self.current_frame + 1 == len(self.frames): 
            self.current_frame = len(self.frames) - 1
            self.texture = self.frames[self.current_frame]
            return

        self.timer += delta_time
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame]
            self.center_y += self.update_y_value                     

    def rise(self):
        self.move(-self.center_x + self.FRAME_WIDTH, -self.center_y + self.ground)
        self.change_frame(self.animations["run"]["row"], self.animations["run"]["frames"])
        self.current_frame = 0
        self.texture = self.frames[0]
        self.update_y_value = 0
        self.now_jumping = False
        self.fall = False
        self.crouch_down = False
        self.crouch_up = False
        
    def update_animation(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame]

            # Jump
            if (self.now_jumping):
                if (self.current_frame == 0 and not self.fall):
                    self.fall = True
                    
                    self.change_frame(self.animations["jump_down"]["row"], self.animations["jump_down"]["frames"])
                    self.texture = self.frames[0]
                    self.current_frame = 0

                    self.update_y_value = -self.jump_height / self.animations["jump_down"]["frames"]
                
                self.center_y += self.update_y_value                     

                if (self.center_y <= self.ground):
                    self.fall = False
                    self.center_y = self.ground
                    self.now_jumping = False

                    # If hold the key DOWN - we need to chouch down
                    from arcade import key
                    window = arcade.get_window()
                    if window and key.DOWN in window.keys_held:
                        self.start_crouch_down()
                        self.timer = self.speed
                        return

                    self.change_frame(self.animations["run"]["row"], self.animations["run"]["frames"])
                    self.texture = self.frames[0]
                    self.current_frame = 0
                    self.timer = self.speed

            # Crouch
            elif (self.crouch_down):

                if self.current_frame == 0:
                    self.crouch_down = False
                    self.crouch_up = True

                    self.change_frame(self.animations["crouch_up"]["row"], self.animations["crouch_up"]["frames"])
                    self.current_frame = 0
                    self.texture = self.frames[0]

            elif (self.crouch_up):
                from arcade import key
                window = arcade.get_window()
                if window and key.DOWN in window.keys_held:
                    self.crouch_up = False
                    self.center_y = self.ground
                    self.start_crouch_down()
                    self.timer = self.speed
                    return
                if self.current_frame == 0:
                    self.crouch_up = False
                    
                    self.change_frame(self.animations["run"]["row"], self.animations["run"]["frames"])
                    self.texture = self.frames[0]
                    self.current_frame = 0
                    self.timer = self.speed
                    self.center_y = self.ground

