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

image_lives = pyglet.image.load_animation("resources/lives.gif")
image_lives.add_to_texture_bin(animation_bin)

image_dog_food = pyglet.resource.image("dog_food.png")

image_game_over = pyglet.resource.image("game_over.png")
main_background = pyglet.resource.image("bg.png")

music_background = pyglet.media.load("resources/bg.mp3")
music_throw = pyglet.media.load("resources/throw.mp3", streaming=False)
music_life = pyglet.media.load("resources/life.mp3", streaming=False)

pyglet.font.add_file("resources/geris_font.ttf")
font_game = pyglet.font.load("Geris Font")