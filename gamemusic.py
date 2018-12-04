import pyglet
import resources


class GameMusic(pyglet.media.Player):
    def __init__(self):
        super(GameMusic, self).__init__()

        # MUSIC RESOURCES
        self.background_music = resources.music_background
        self.game_over_music = resources.music_game_over

        self.state = ""

    def play_menu(self):
        print("playmenu")
        loop_background_music = pyglet.media.SourceGroup(self.background_music.audio_format, None)
        loop_background_music.queue(self.background_music)
        loop_background_music.loop = True

        self.queue(loop_background_music)
        self.play()

    def play_background(self):
        print("playbg")
        loop_background_music = pyglet.media.sources.SourceGroup(self.background_music.audio_format, None)
        loop_background_music.queue(self.background_music)
        loop_background_music.loop = True

        self.queue(loop_background_music)
        self.play()

    def play_game_over(self):
        print("playtempo")
        self.queue(self.game_over_music)
        self.play()




