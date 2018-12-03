from gameobject import GameObject
import resources


class CatFood(GameObject):
    def __init__(self, *args, **kwargs):
        super(CatFood, self).__init__(img=resources.image_cat_food, *args, **kwargs)
        self.velocity_x = 500.0
        self.lane = 0
        self.direction = "left"
        self.destroyed = False
        self.eaten = False
        self.wasted = False

    def check_wasted(self):
        if self.lane == 1:
            if self.x <= 170:
                self.wasted = True

        if self.lane == 2:
            if self.x <= 190:
                self.wasted = True

        if self.lane == 3:
            if self.x <= 190:
                self.wasted = True

    def update(self, dt):
        super().update(dt)
        self.check_wasted()
        if self.wasted:
            self.destroy()

    def handle_collision(self, other_object):
        if other_object.__class__.__name__ == "Cat":
            if not other_object.fed:
                other_object.set_direction("left")
                self.eaten = True
                self.destroy()
        if other_object.__class__.__name__ == "Dog":
            if not other_object.fed:
                self.wasted = True
                self.destroy()

    def destroy(self):
        self.destroyed = True
