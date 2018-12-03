from pyglet.sprite import Sprite


class GameObject(Sprite):

    def __init__(self, *args, **kwargs):
        super(GameObject, self).__init__(*args, **kwargs)

        # ATTRIBUTES
        self.x = 0
        self.y = 0
        self.direction = None
        self.lane = None
        self.velocity_x = 0.0

        # FLAGS
        self.destroyed = False

        # LISTS
        self.event_handlers = []
        self.new_objects = []

    def update(self, dt):
        if self.direction == "right":
            self.x += self.velocity_x * dt

        if self.direction == "left":
            self.x -= self.velocity_x * dt

    def collides_with(self, other_object):
        if self.direction == "left":
            if self.lane == other_object.lane:
                    if self.x <= other_object.x + other_object.width // 2:
                        return True

        if self.direction == "right":
            if self.lane == other_object.lane:
                if self.x + self.width // 2 >= other_object.x:
                    return True

        return False


