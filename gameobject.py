from pyglet.sprite import Sprite


class GameObject(Sprite):

    def __init__(self, *args, **kwargs):
        super(GameObject, self).__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.direction = "left"
        self.new_objects = []
        self.event_handlers = []
        self.destroyed = False
        self.lane = 1
        self.wasted = False
        self.eaten = False

    def update(self, dt):
        if self.direction == "right":
            self.x += self.velocity_x * dt

        if self.direction == "left":
            self.x -= self.velocity_x * dt

    def collides_with(self, other_object):
        self.lane = self.lane


