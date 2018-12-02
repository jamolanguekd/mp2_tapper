import pyglet


def initialize_image(image, width, height):
    image.width = width
    image.height = height


# RESOURCES FOLDER
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

image_pikachu = pyglet.resource.image("pikachu.png")
image_pokeball = pyglet.resource.image("pokeball.png")
main_background = pyglet.resource.image("bg.png")

initialize_image(image_pikachu, 100, 80)
initialize_image(image_pokeball, 30, 30)


def music():
	music= pyglet.media.load("bg.mp3")
	return music
