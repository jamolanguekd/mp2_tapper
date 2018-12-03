import pyglet
from pyglet.window import key

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 0
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(400, 140, caption='USERNAME')

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label('USERNAME', x=10, y=60, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Score', x=10, y=20,
                              anchor_y='bottom', color=(0, 0, 0, 255),
                              batch=self.batch),
        ]
        self.widgets = [
            TextWidget('', 200, 60, self.width - 210, self.batch),
        ]

        self.focus = self.widgets[0]

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()


    def on_text(self, text):
    	if self.focus:
            self.focus.caret.on_text(text)
            name.append(text)

    def on_key_press(self, symbol, modifiers):
        username="".join(name)
        if symbol==pyglet.window.key.ENTER:
            self.label=pyglet.text.Label('HELLO  '+username, x=150, y=100, anchor_y='bottom', color=(0, 0, 0, 255), batch=self.batch)
            print(username)
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0


        elif symbol == pyglet.window.key.ESCAPE:
            window.close()
            pyglet.app.exit()

name=[]
window = Window(resizable=True)
pyglet.app.run()
