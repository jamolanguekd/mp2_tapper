from gameobject import GameObject
import resources
import random

class Dog(GameObject):
    def __init__(self, *args, **kwargs):
        super(Dog, self).__init__(img=resources.image_pikachu, *args, **kwargs)
        self.x = 0
        self.velocity_x = 100
        self.direction = "right"

    def collides_with(self, other_object):
        if self.direction == "right":
            if self.x + self.width // 2 >= other_object.x:
                return True
        return False

    def handle_collision(self, other_object):
        if other_object.__class__.__name__ == "DogFood":
            other_object.eaten = True
            self.direction = "left"
            self.velocity_x = 100

    def check_home(self):
        if self.x <= 172:
            self.destroyed = True

    def update(self, dt):
        super().update(dt)
        self.check_home()
