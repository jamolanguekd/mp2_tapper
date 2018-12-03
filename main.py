import pyglet
import player
import dog
import dogfood
import resources
import random
import itertools
import gamemusic

# SET UP INTERFACE
game_window = pyglet.window.Window(width=800, height=600)

main_batch = pyglet.graphics.Batch()
main_batch_background = pyglet.graphics.OrderedGroup(0)
main_batch_foreground = pyglet.graphics.OrderedGroup(1)

game_background = pyglet.sprite.Sprite(resources.main_background, batch=main_batch, group=main_batch_background)
game_over = pyglet.sprite.Sprite(img=resources.image_game_over, y=800, batch=main_batch, group=main_batch_background)
score_label = pyglet.text.Label(text="Score: ", x=30, y=560, color=(0, 0, 0, 255),
                                font_name="Geris Font", font_size=18, batch=main_batch, group=main_batch_background)
lives_label = pyglet.text.Label(text="Lives: ", x=580, y=560, color=(0, 0, 0, 255),
                                font_name="Geris Font", font_size=18, batch=main_batch, group=main_batch_background)

game_objects = []
game_lives = []
game_player = None
score = None
lives = None
event_stack_size = 0

game_music_player = gamemusic.GameMusic()


def init():
    global game_music_player
    game_music_player.play_background()
    reset_level()


def reset_level():
    global event_stack_size, game_objects, game_player, game_lives, score, lives

    score = 0
    lives = 3

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    game_player = player.Player(batch=main_batch, group=main_batch_foreground)
    game_objects = [game_player]
    game_lives = []
    for i in range(lives):
        new_life = pyglet.sprite.Sprite(img=resources.image_lives, x=650 + (i * 35), y=550, batch=main_batch,
                                        group=main_batch_background)
        new_life.scale = 0.3
        game_lives.append(new_life)

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
    lives_label.draw()

@game_window.event
def update(dt):
    global score, lives, game_music_player

    while len(game_lives) > lives:
        game_lives[-1].delete()
        game_lives.pop()

    if lives > 0:

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

            if isinstance(item, dogfood.DogFood):
                if item.eaten:
                    score += 100
                if item.wasted:
                    lives -= 1
            if isinstance(item, dog.Dog):
                if item.end:
                    lives -= 1

            score_label.text = "Score: "+str(score)

        # UPDATE ITEMS
        for item in game_objects:
            item.update(dt)

            to_add.extend(item.new_objects)
            item.new_objects = []

        # GENERATE DOGS
        if random.randint(1, 100) <= 2:
            new_dog = dog.Dog(batch=main_batch, group=main_batch_foreground)
            new_dog.set_lane(random.randint(1, 3))
            to_add.append(new_dog)

        game_objects.extend(to_add)

    else:
        for items in game_objects:
            try:
                items.delete()
            except:
                None
        game_over.y = 0
        game_music_player.play_game_over()


if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
