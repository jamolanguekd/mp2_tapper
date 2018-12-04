import pyglet


# RESOURCES FOLDER
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# ANIMATED SPRITES
animation_bin = pyglet.image.atlas.TextureBin()

image_player = pyglet.image.load_animation("resources/player.gif")
image_player.add_to_texture_bin(animation_bin)

image_dog = pyglet.image.load_animation("resources/biscuit.gif")
image_dog.add_to_texture_bin(animation_bin)

image_dog_reversed = pyglet.image.load_animation("resources/biscuit_reversed.gif")
image_dog_reversed.add_to_texture_bin(animation_bin)

image_cat = pyglet.image.load_animation("resources/oreo.gif")
image_cat.add_to_texture_bin(animation_bin)

image_cat_reversed = pyglet.image.load_animation("resources/oreo_reversed.gif")
image_cat_reversed.add_to_texture_bin(animation_bin)

image_lives = pyglet.image.load_animation("resources/lives.gif")
image_lives.add_to_texture_bin(animation_bin)


# OBJECT SPRITES
image_dog_food = pyglet.resource.image("dog_food.png")
image_cat_food = pyglet.resource.image("cat_food.png")


# BACKGROUND
main_background = pyglet.resource.image("background.png")
leaderboard = pyglet.resource.image("leaderboard.png")
main_menu = pyglet.resource.image("menu.png")

# TEXTS
image_game_over = pyglet.resource.image("game_over.png")
image_game_ready = pyglet.resource.image("game_ready.png")
image_enter_name = pyglet.resource.image("name_input.png")

# MUSIC AND SOUND FX
music_background = pyglet.media.load("resources/background_music.wav", streaming=False)
music_throw = pyglet.media.load("resources/throw.wav", streaming=False)
music_life = pyglet.media.load("resources/life.wav", streaming=False)
music_happy_bork = pyglet.media.load("resources/happy_bork.wav", streaming=False)
music_sad_bork = pyglet.media.load("resources/sad_bork.wav", streaming=False)
music_happy_meow = pyglet.media.load("resources/happy_meow.wav", streaming=False)
music_sad_meow = pyglet.media.load("resources/sad_meow.wav", streaming=False)
music_game_over = pyglet.media.load("resources/sad_bork.wav", streaming=False)

# FONTS
pyglet.font.add_file("resources/geris_font.ttf")
font_game = pyglet.font.load("Geris Font")
pyglet.font.add_file("resources/photographs.ttf")
font_numbers = pyglet.font.load("Photographs")