import pyglet
import player
import dog
import dogfood
import resources
import random
import itertools

game_window = pyglet.window.Window(width=800, height=600)

main_batch = pyglet.graphics.Batch()

game_background = pyglet.sprite.Sprite(resources.main_background, batch=main_batch)
game_player = None
game_objects = []
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, color=(0, 0, 0, 255))
event_stack_size = 0
score = 0

test_dog = None


def music():
    music = resources.music_background

    loop = pyglet.media.SourceGroup(music.audio_format, None)
    loop.queue(music)
    loop.loop = True

    player = pyglet.media.Player()
    player.queue(loop)
    player.play()

def init():
    reset_level()
    music()


def reset_level():
    global event_stack_size, game_objects, game_player, test_dog

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    game_player = player.Player(batch=main_batch)
    test_dog = dog.Dog(batch=main_batch)
    test_dog.set_lane(3)
    game_objects = [game_player, test_dog]

    for item in game_objects:
        for handler in item.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1

@game_window.event
def on_mouse_press(x,y, button, modifiers):
    score_label.text = str(x)+" "+str(y)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    score_label.draw()

@game_window.event
def update(dt):
    global score, game_objects

    # CHECK FOR GAME OVER


    # CHECK FOR COLLISIONS
    for obj1, obj2 in itertools.combinations(game_objects, 2):
        if obj1.collides_with(obj2):
            obj1.handle_collision(obj2)
            obj2.handle_collision(obj1)

    to_add = []

    # DELETE DESTROYED OBJECTS
    for item in [item for item in game_objects if item.destroyed]:
        game_objects.remove(item)
        item.delete()

        if isinstance(item, dogfood.DogFood) and item.eaten:
            score += 100

        score_label.text = "Score: "+str(score)

    # UPDATE ITEMS
    for item in game_objects:
        item.update(dt)

        to_add.extend(item.new_objects)
        item.new_objects = []

    # GENERATE DOGS
    if random.randint(1, 100) <= 1:
        new_dog = dog.Dog(batch=main_batch)
        new_dog.set_lane(random.randint(1, 3))
        to_add.append(new_dog)

    game_objects.extend(to_add)


if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
