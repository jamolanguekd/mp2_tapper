import pyglet
import player
import dog
import resources

game_window = pyglet.window.Window(width=800, height=600)

main_batch = pyglet.graphics.Batch()

game_background = pyglet.sprite.Sprite(resources.main_background, batch=main_batch)
game_player = None
game_objects = []
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575)
event_stack_size = 0
score = 0

test_dog = None

def music():
    music= resources.music()

    loop= pyglet.media.SourceGroup(music.audio_format, None)
    loop.queue(music)
    loop.loop=True

    player=pyglet.media.Player()
    player.queue(loop)
    player.play()

music()


def init():

    reset_level()


def reset_level():
    global event_stack_size, game_objects, game_player, test_dog

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    game_player = player.Player(batch=main_batch)
    test_dog = dog.Dog(batch=main_batch)
    test_dog.x = 172
    test_dog.y = 80
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
    global score
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            first_obj = game_objects[i]
            second_obj = game_objects[j]

            if first_obj.collides_with(second_obj):
                first_obj.handle_collision(second_obj)
                second_obj.handle_collision(first_obj)

    to_add = []

    for item in game_objects:
        item.update(dt)

        to_add.extend(item.new_objects)
        item.new_objects = []

    for item in [item for item in game_objects if item.destroyed]:
        to_add.extend(item.new_objects)
        item.delete()
        game_objects.remove(item)

    game_objects.extend(to_add)


if __name__ == '__main__':

    init()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
