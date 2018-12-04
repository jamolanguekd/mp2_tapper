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
from pyglet.window import key

# SET UP INTERFACE
game_window = pyglet.window.Window(width=800, height=600)
game_window.set_exclusive_mouse(True)

# GLOBAL VARIABLES
player_name = ""
game_ready_timer = None
game_over_timer = None
game_objects = []
game_lives = []
leaderboard_labels = None
name_input_label = None
name_input = None
game_player = None
score = 0
lives = None
event_stack_size = 0
state = "main_menu"
finished_round = False

# GLOBAL PLAYERS
game_music_player = None
menu_music_player = None
game_over_player = None


# THIS FUNCTION HANDLES ALL THE KEYPRESSES
@game_window.event
def on_key_press(symbol, modifiers):
    global state, player_name, score, name_input_label, name_input, finished_round

    if state == "leaderboards":
        if finished_round:
            if 65 < symbol < 122:
                if len(player_name) < 3:
                    player_name += chr(symbol).upper()
                    name_input_label.text = player_name
            if symbol == key.ENTER:
                name_input_label.delete()
                name_input.delete()
                save_scores()
                scene(state)
            if symbol == key.BACKSPACE:
                if player_name != "":
                    player_name = list(player_name)
                    player_name.pop()
                    player_name = "".join(player_name)
                name_input_label.text = player_name


# THIS FUNCTION HANDLES MOUSE CLICKS
@game_window.event
def on_mouse_press(x, y, symbol, modifiers):
    global state
    print(str(x)+" "+str(y))
    if state == "main_menu":
        if symbol == mouse.LEFT:
            if 240 < x < 565:
                if 140 < y < 210:
                    state = "play_game"
                    scene(state)
            if 235 < x < 570:
                if 100 < y < 135:
                    state = "leaderboards"
                    scene(state)
            if 235 < x < 560:
                if 60 < y < 95:
                    pyglet.app.exit()
    if state == "leaderboards":
        if symbol == mouse.LEFT:
            if 35 < x < 160:
                if 55 < y < 105:
                    state = "main_menu"
                    scene(state)


# THIS FUNCTION GETS CALLED EVERY TIME THE WINDOW IS REDRAWN
@game_window.event
def on_draw():
    game_window.clear()
    if state == "main_menu":
        menu_batch.draw()
    if state == "play_game":
        main_batch.draw()
    if state == "leaderboards":
        leaderboard_batch.draw()


# THIS FUNCTION SETS THE SCENE TO BE DISPLAYED
def scene(string_state):
    if string_state == "main_menu":
        start_menu()

    if string_state == "play_game":
        start_game()
        pyglet.clock.schedule_interval(update, 1/120.0)

    if string_state == "leaderboards":
        start_leaderboards()


# THIS FUNCTION SETS UP THE MENU
def start_menu():
    global menu_music_player, game_music_player, game_over_player, menu_batch, main_menu_background

    # SET UP BATCH
    menu_batch = pyglet.graphics.Batch()
    main_menu_background = pyglet.sprite.Sprite(img=resources.main_menu, batch=menu_batch)

    if isinstance(game_music_player, gamemusic.GameMusic):
        game_music_player.delete()
    if isinstance(game_over_player, gamemusic.GameMusic):
        game_over_player.delete()
    if isinstance(menu_music_player, gamemusic.GameMusic):
        menu_music_player.delete()
    menu_music_player = gamemusic.GameMusic()
    menu_music_player.play_menu()
    game_window.set_exclusive_mouse(False)
    pyglet.clock.unschedule(update)


# THIS FUNCTION SETS UP THE GAME AND THE INITIAL PARAMETERS
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


# THIS FUNCTION UPDATES EACH FRAME
def update(dt):
    global score, lives, game_music_player, game_window, event_stack_size, game_over_timer, state, \
        game_ready_timer, game_ready, game_over, game_over_player, finished_round

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
                        resources.music_life.play()

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
                finished_round = True
                state = "leaderboards"
                scene(state)

            # DISPLAY GAME OVER
            else:
                lives_label.text = "OHOHO U DED SON"

                # DELETE OTHER GAME OBJECTS
                for items in game_objects:
                    try:
                        items.delete()
                    except AttributeError:
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


# THIS FUNCTION SETS UP THE LEADERBOARDS
def start_leaderboards():
    global leaderboard_batch, leaderboard_background_image, menu_music_player, name_input, name_input_label, \
        leaderboard_labels, finished_round

    # DESTROY ANY EXISTING PLAYERS
    if isinstance(menu_music_player, gamemusic.GameMusic):
        menu_music_player.delete()
    if isinstance(game_over_player, gamemusic.GameMusic):
        game_over_player.delete()

    # SET UP PLAYER
    menu_music_player = gamemusic.GameMusic()
    menu_music_player.play_menu()

    # SET UP BATCH
    leaderboard_batch = pyglet.graphics.Batch()
    leaderboard_background = pyglet.graphics.OrderedGroup(0)
    leaderboard_middle = pyglet.graphics.OrderedGroup(1)
    leaderboard_foreground = pyglet.graphics.OrderedGroup(2)

    # SET UP BACKGROUND
    leaderboard_background_image = pyglet.sprite.Sprite(img=resources.leaderboard, batch=leaderboard_batch,
                                                        group=leaderboard_background)

    # READ HI SCORES
    leaderboard_users, leaderboard_scores = read_scores()
    leaderboard_labels = []

    # SET UP USER LABELS
    for i in range(len(leaderboard_users)):
        x = 300
        y = 248 - i * 46
        new_label = pyglet.text.Label(text=leaderboard_users[i], x=x, y=y, font_name="Geris Font",
                                      color=(0, 0, 0, 255), font_size=25, batch=leaderboard_batch,
                                      group=leaderboard_middle)
        leaderboard_labels.append(new_label)

    # SET UP SCORE LABELS
    for i in range(len(leaderboard_scores)):
        x = 467
        y = 248 - i * 46
        new_label = pyglet.text.Label(text=leaderboard_scores[i], x=x, y=y, font_name="Photographs",
                                      color=(0, 0, 0, 255), font_size=25, batch=leaderboard_batch,
                                      group=leaderboard_middle)
        leaderboard_labels.append(new_label)

    # CALL LEADERBOARD WHEN A ROUND IS DONE
    if finished_round:
        name_input = pyglet.sprite.Sprite(img=resources.image_enter_name, x=9, batch=leaderboard_batch,
                                          group=leaderboard_foreground)
        name_input_label = pyglet.text.Label(text="", x=280, y=260, color=(0, 0, 0, 255), batch=leaderboard_batch,
                                             font_name="Geris Font", font_size=25,
                                             group=pyglet.graphics.OrderedGroup(3))

    pyglet.clock.unschedule(update)


# THIS FUNCTION READS SCORES FROM THE TEXT FILE
def read_scores():

    score_file = open("leaderboard.txt")

    score_data = [x.strip() for x in score_file.readlines()]
    user_list = [item.split()[0] for item in score_data]
    score_list = [item.split()[1] for item in score_data]

    score_file.close()

    return user_list, score_list


# THIS FUNCTION WRITES SCORES TO THE TEXT FILE
def save_scores():
    global score, player_name, finished_round

    # READ CURRENT HIGH SCORES
    user_list, score_list = read_scores()

    # INSERT USER SCORE AND SORT
    score_list.append(str(score))
    score_list = [int(item) for item in score_list]
    score_list.sort()
    score_list.reverse()
    user_list.insert(score_list.index(score), player_name)
    score_list = [str(item) for item in score_list]

    # REMOVE EXCESS SCORES
    while len(score_list) > 5:
        score_list.pop()
    while len(user_list) > 5:
        user_list.pop()

    # WRITE HIGH SCORE
    score_file = open("leaderboard.txt", "w")
    for i in range(len(user_list)):
        score_file.write(str(user_list[i]) + " " + str(score_list[i]) + "\n")
    score_file.close()
    player_name = ""
    finished_round = False


if __name__ == '__main__':
    scene(state)
    pyglet.app.run()
