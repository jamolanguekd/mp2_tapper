import pyglet
import player
import dog
import cat
import dogfood
import catfood
import resources
import random
import itertools
import gamemusic
from pyglet.window import mouse

# SET UP INTERFACE
game_window = pyglet.window.Window(width=800, height=600)
game_window.set_exclusive_mouse(True)

menu_batch = pyglet.graphics.Batch()
main_menu_background = pyglet.sprite.Sprite(img=resources.main_menu, batch=menu_batch)

main_batch = pyglet.graphics.Batch()
main_batch_background = pyglet.graphics.OrderedGroup(0)
main_batch_middle = pyglet.graphics.OrderedGroup(1)
main_batch_foreground = pyglet.graphics.OrderedGroup(2)

game_background = pyglet.sprite.Sprite(resources.main_background, batch=main_batch, group=main_batch_background)
game_over = pyglet.sprite.Sprite(img=resources.image_game_over, y=800, batch=main_batch, group=main_batch_foreground)
score_label = pyglet.text.Label(text="Score: ", x=30, y=560, color=(0, 0, 0, 255),
                                font_name="Geris Font", font_size=18, batch=main_batch, group=pyglet.graphics.OrderedGroup(1))
lives_label = pyglet.text.Label(text="Lives: ", x=580, y=560, color=(0, 0, 0, 255),
                                font_name="Geris Font", font_size=18, batch=main_batch, group=main_batch_middle)

game_objects = []
game_lives = []
game_player = None
score = None
lives = None
event_stack_size = 0
state = "main_menu"

game_music_player = gamemusic.GameMusic()


def init():
    global game_music_player, state
    if state == "main_menu":
        game_music_player.play_background()
        game_window.set_exclusive_mouse(False)

    if state == "play_game":
        game_window.set_exclusive_mouse(True)
        pyglet.clock.schedule_interval(update, 1/120.0)
        game_music_player.play_background()
        reset_level()

@game_window.event
def on_mouse_press(x, y, symbol, modifiers):
    global state
    if symbol == mouse.LEFT:
        print(str(x)+" "+str(y))
        if state == "main_menu":
            if 240 < x < 565:
                if 140 < y < 210:
                    state = "play_game"
                    init()
            if 235 < x < 570:
                if 100 < y < 135:
                    state = "leaderboards"
            if 235 < x < 560:
                if 60 < y < 95:
                    pyglet.app.exit()


def reset_level():
    global game_window, event_stack_size, game_objects, game_player, game_lives, score, lives

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
def on_draw():
    game_window.clear()
    if state == "main_menu":
        menu_batch.draw()
    if state == "play_game":
        main_batch.draw()
        score_label.draw()
        lives_label.draw()

@game_window.event
def update(dt):
    global score, lives, game_music_player, game_window, event_stack_size

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
            if isinstance(item, dog.Dog) or isinstance(item, cat.Cat):
                if item.end:
                    lives -= 1

            score_label.text = "Score: "+str(score)

        # UPDATE ITEMS
        for item in game_objects:
            item.update(dt)

            to_add.extend(item.new_objects)
            item.new_objects = []

        # GENERATE DOGS AND CATS
        if random.randint(1, 100) <= 2:
            chance_dog_cat = random.randint(1, 100)
            if chance_dog_cat > 50:
                new_dog = dog.Dog(batch=main_batch, group=main_batch_foreground)
                new_dog.set_lane(random.randint(1, 3))
                to_add.append(new_dog)
            else:
                new_cat = cat.Cat(batch=main_batch, group=main_batch_foreground)
                new_cat.set_lane(random.randint(1, 3))
                to_add.append(new_cat)

        game_objects.extend(to_add)

    elif lives <= 0:
        for items in game_objects:
            try:
                lives_label.text = "OHOHO U DED SON"
                items.delete()

            except:
                None

        while event_stack_size > 0:
            game_window.pop_handlers()
            event_stack_size -= 1

        game_over.y = 0
        game_music_player.play_game_over()
        game_window.set_exclusive_mouse(False)



if __name__ == '__main__':
    init()
    pyglet.app.run()
