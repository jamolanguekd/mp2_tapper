import pyglet


def initialize_image(image, width, height):
    image.width = width
    image.height = height


# RESOURCES FOLDER
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

image_player = pyglet.resource.image("player.png")

animation_bin = pyglet.image.atlas.TextureBin()

image_dog = pyglet.image.load_animation("resources/biscuit.gif")
image_dog.add_to_texture_bin(animation_bin)

image_dog_reversed = pyglet.image.load_animation("resources/biscuit_reversed.gif")
image_dog_reversed.add_to_texture_bin(animation_bin)

image_cat = pyglet.image.load_animation("resources/oreo.gif")
image_cat.add_to_texture_bin(animation_bin)

image_cat_reversed = pyglet.image.load_animation("resources/oreo.gif")
image_cat_reversed.add_to_texture_bin(animation_bin)

image_lives = pyglet.image.load_animation("resources/lives.gif")
image_lives.add_to_texture_bin(animation_bin)

image_dog_food = pyglet.resource.image("dog_food.png")

image_cat_food = pyglet.resource.image("cat_food.png")

image_game_over = pyglet.resource.image("game_over.png")
main_background = pyglet.resource.image("background.png")
main_menu = pyglet.resource.image("menu.png")

music_background = pyglet.media.load("resources/background_music.mp3")
music_throw = pyglet.media.load("resources/throw.mp3", streaming=False)
music_life = pyglet.media.load("resources/life.mp3", streaming=False)
music_happy_bork = pyglet.media.load("resources/happy_bork.mp3", streaming=False)
music_sad_bork = pyglet.media.load("resources/sad_bork.mp3", streaming=False)
music_game_over = pyglet.media.load("resources/tempo.mp3")

pyglet.font.add_file("resources/geris_font.ttf")
font_game = pyglet.font.load("Geris Font")