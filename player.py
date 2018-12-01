from pyglet.window import key
from gameobject import GameObject
from dogfood import DogFood
import resources


class Player(GameObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.image_pikachu, *args, **kwargs)
        self.x = 690
        self.y = 80
        self.velocity_x = 0.0
        self.direction = "none"
        self.lane = 1
        self.new_objects = []
        self.event_handlers = [self.on_key_press]

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if self.lane != 3:
                self.y += 110
                self.lane += 1

        if symbol == key.DOWN:
            if self.lane != 1:
                self.y -= 110
                self.lane -= 1

        if symbol == key.Q:
            self.throw_dog_food()

    def throw_dog_food(self):
        new_food = DogFood(batch=self.batch)
        new_food.x = self.x
        new_food.y = self.y
        new_food.lane = self.lane

        self.new_objects.append(new_food)


