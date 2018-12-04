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

game_ready_timer = None
game_over_timer = None
game_objects = []
game_lives = []
game_player = None
score = None
lives = None
event_stack_size = 0
state = "main_menu"

game_music_player = None
menu_music_player = None
game_over_player = None

@game_window.event
def on_mouse_press(x, y, symbol, modifiers):
    global state
    if state == "main_menu":
        if symbol == mouse.LEFT:
            if 240 < x < 565:
                if 140 < y < 210:
                    state = "play_game"
                    scene(state)
            if 235 < x < 570:
                if 100 < y < 135:
                    state = "leaderboards"
            if 235 < x < 560:
                if 60 < y < 95:
                    pyglet.app.exit()


@game_window.event
def on_draw():
    game_window.clear()
    if state == "main_menu":
        menu_batch.draw()
    if state == "play_game":
        main_batch.draw()


def scene(string_state):
    if string_state == "main_menu":
        start_menu()

    if string_state == "play_game":
        start_game()
        pyglet.clock.schedule_interval(update, 1/120.0)


def start_menu():
    global menu_music_player, game_music_player,game_over_player
    if isinstance(game_music_player, gamemusic.GameMusic):
        game_music_player.delete()
    if isinstance(game_over_player, gamemusic.GameMusic):
        game_over_player.delete()
    menu_music_player = gamemusic.GameMusic()
    menu_music_player.play_menu()
    game_window.set_exclusive_mouse(False)
    pyglet.clock.unschedule(update)


def start_game():
    global game_window, event_stack_size, game_objects, game_player, game_lives, score, lives, game_over_timer, \
        game_ready_timer, game_ready, score_label, lives_label, game_background, game_over, main_batch,\
        main_batch_background, main_batch_middle, main_batch_foreground, game_music_player, menu_music_player

    # INITIAL VALUES
    game_ready_timer = 120 * 3
    game_over_timer = 120 * 3
    score = 0
    lives = 3

    # BATCHES
    main_batch = pyglet.graphics.Batch()
    main_batch_background = pyglet.graphics.OrderedGroup(0)
    main_batch_middle = pyglet.graphics.OrderedGroup(1)
    main_batch_foreground = pyglet.graphics.OrderedGroup(2)

    # SET UP SPRITES
    game_background = pyglet.sprite.Sprite(resources.main_background, batch=main_batch, group=main_batch_background)
    game_ready = pyglet.sprite.Sprite(img=resources.image_game_ready, batch=main_batch, group=main_batch_foreground)
    game_over = pyglet.sprite.Sprite(img=resources.image_game_over, batch=main_batch, group=main_batch_foreground)
    game_over.y = 800

    # SET UP LABELS
    score_label = pyglet.text.Label(text="Score: 0", x=30, y=560, color=(0, 0, 0, 255),
                                    font_name="Geris Font", font_size=18, batch=main_batch, group=main_batch_middle)
    lives_label = pyglet.text.Label(text="Lives: ", x=580, y=560, color=(0, 0, 0, 255),
                                    font_name="Geris Font", font_size=18, batch=main_batch, group=main_batch_middle)

    # CLEAR ANY PREVIOUS HANDLERS
    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    # SET UP PLAYER
    game_player = player.Player(batch=main_batch, group=main_batch_middle)
    game_objects = [game_player]

    # SET UP LIVES
    game_lives = []
    for i in range(lives):
        new_life = pyglet.sprite.Sprite(img=resources.image_lives, x=650 + (i * 35), y=550, batch=main_batch,
                                        group=main_batch_middle)
        new_life.scale = 0.3
        game_lives.append(new_life)

    # SET UP MUSIC AND MOUSE
    game_window.set_exclusive_mouse(True)
    if isinstance(menu_music_player, gamemusic.GameMusic):
        menu_music_player.delete()
    game_music_player = gamemusic.GameMusic()
    pyglet.clock.schedule_interval(update, 1/120.0)


def update(dt):
    global score, lives, game_music_player, game_window, event_stack_size, game_over_timer, state, \
        game_ready_timer, game_ready, game_over, game_over_player

    # UPDATE LIVES
    while len(game_lives) > lives:
        game_lives[-1].delete()
        game_lives.pop()

    # UPDATE TIMER
    if game_ready_timer > 0:
        if game_ready_timer % 120 == 0:
            resources.music_happy_bork.play()
        game_ready_timer -= 1

    # GAME START
    if game_ready_timer <= 0:
        game_ready.visible = False

        # PLAYER STILL ALIVE
        if lives > 0:

            game_music_player.play_background()

            # PUSH HANDLERS
            if event_stack_size <= 0:
                for item in game_objects:
                    for handler in item.event_handlers:
                        game_window.push_handlers(handler)
                        event_stack_size += 1

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

                if isinstance(item, dogfood.DogFood) or isinstance(item, catfood.CatFood):
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
            if random.randint(1, 100) <= 1:
                chance_dog_cat = random.randint(1, 100)
                if chance_dog_cat > 50:
                    new_dog = dog.Dog(batch=main_batch, group=main_batch_middle)
                    new_dog.set_lane(random.randint(1, 3))
                    to_add.append(new_dog)
                else:
                    new_cat = cat.Cat(batch=main_batch, group=main_batch_middle)
                    new_cat.set_lane(random.randint(1, 3))
                    to_add.append(new_cat)

            game_objects.extend(to_add)

        # PLAYER IS DEAD
        if lives <= 0:

            game_over_timer -= 1

            # GAME OVER DISPLAY IS OVER
            if game_over_timer <= 0:
                score_label.delete()
                lives_label.delete()
                state = "main_menu"
                scene(state)

            # DISPLAY GAME OVER
            else:
                lives_label.text = "OHOHO U DED SON"

                # DELETE OTHER GAME OBJECTS
                for items in game_objects:
                    try:
                        items.delete()
                    except:
                        None

                # DELETE ALL HANDLERS
                while event_stack_size > 0:
                    game_window.pop_handlers()
                    event_stack_size -= 1

                # SHOW GAME OVER AND STOP MUSIC
                game_over.y = 0
                if game_over_timer == 349:
                    game_music_player.pause()
                    game_over_player = gamemusic.GameMusic()
                    game_over_player.play_game_over()

                game_window.set_exclusive_mouse(False)


if __name__ == '__main__':
    scene(state)
    pyglet.app.run()
