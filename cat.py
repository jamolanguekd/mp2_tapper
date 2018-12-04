from gameobject import GameObject
import resources


class Cat(GameObject):
    def __init__(self, *args, **kwargs):
        super(Cat, self).__init__(img=resources.image_cat, *args, **kwargs)

        # ATTRIBUTES
        self.x = 0
        self.y = 0
        self.direction = None
        self.lane = None
        self.velocity_x = 150

        # FLAGS
        self.destroyed = False
        self.end = False
        self.fed = False

        # INITIAL VALUES
        self.set_direction("right")

    # CHECKS IF THE CAT REACHES THE END OF EACH LANE
    def check_end(self):
        if self.lane == 1:
            if self.x + self.width // 2 >= 665:
                self.end = True
                self.destroyed = True
                resources.music_sad_meow.play()
        if self.lane == 2:
            if self.x + self.width // 2 >= 665:
                self.end = True
                self.destroyed = True
                resources.music_sad_meow.play()
        if self.lane == 3:
            if self.x + self.width // 2 >= 655:
                self.end = True
                self.destroyed = True
                resources.music_sad_meow.play()

    # CHECKS IF THE DOG
    def check_home(self):
        if self.lane == 1:
            if self.x <= 170:
                self.destroyed = True

        if self.lane == 2:
            if self.x <= 190:
                self.destroyed = True

        if self.lane == 3:
            if self.x <= 190:
                self.destroyed = True

    def handle_collision(self, other_object):

        # ONLY CHECK FOR COLLISION IF NOT FED
        if not self.fed:

            # IF CAT EATS CAT FOOD
            if other_object.__class__.__name__ == "CatFood":
                if other_object.destroyed is False:
                    self.set_direction("left")
                    other_object.eaten = True
                    other_object.destroy()
                    resources.music_happy_meow.play()

            # IF CAT EATS DOG FOOD
            if other_object.__class__.__name__ == "DogFood":
                if other_object.destroyed is False:
                    self.set_direction("left")
                    other_object.wasted = True
                    other_object.destroy()
                    resources.music_sad_meow.play()

    # SET DIRECTION OF CAT
    def set_direction(self, direction):
        self.direction = direction
        if self.direction == "right":
            self.image = resources.image_cat
        if self.direction == "left":
            self.fed = True
            self.image = resources.image_cat_reversed
            self.velocity_x = 500

    # SET LANE OF CAT
    def set_lane(self, num):
        self.lane = num
        if self.lane == 1:
            self.x = 170
            self.y = 70

        if self.lane == 2:
            self.x = 190
            self.y = 185

        if self.lane == 3:
            self.x = 190
            self.y = 295

    # FUNCTIONS TO CALL EVERY FRAME
    def update(self, dt):
        super().update(dt)
        self.check_end()
        self.check_home()
