from random import shuffle
from turtle import Screen, Turtle
from freegames import path

class MemoryGame:
    def __init__(self):
        self.car = path('car.gif')
        self.tiles = list(range(32)) * 2
        self.state = {'mark': None}
        self.hide = [True] * 64
        self.screen = Screen()
        self.turtle = Turtle()
        self.screen.setup(420, 420, 370, 0)
        self.screen.addshape(self.car)
        self.screen.tracer(False)
        self.screen.onclick(self.tap)
        shuffle(self.tiles)

    def square(self, x, y):
        self.turtle.up()
        self.turtle.goto(x, y)
        self.turtle.down()
        self.turtle.color('black', 'white')
        self.turtle.begin_fill()
        for count in range(4):
            self.turtle.forward(50)
            self.turtle.left(90)
        self.turtle.end_fill()

    def index(self, x, y):
        return int((x + 200) // 50 + ((y + 200) // 50) * 8)

    def xy(self, count):
        return (count % 8) * 50 - 200, (count // 8) * 50 - 200

    def tap(self, x, y):
        spot = self.index(x, y)
        mark = self.state['mark']

        if mark is None or mark == spot or self.tiles[mark] != self.tiles[spot]:
            self.state['mark'] = spot
        else:
            self.hide[spot] = False
            self.hide[mark] = False
            self.state['mark'] = None

    def draw(self):
        self.turtle.clear()
        self.turtle.up()
        self.turtle.goto(0, 0)
        self.turtle.shape(self.car)
        self.turtle.stamp()

        for count in range(64):
            if self.hide[count]:
                x, y = self.xy(count)
                self.square(x, y)

        mark = self.state['mark']

        if mark is not None and self.hide[mark]:
            x, y = self.xy(mark)
            self.turtle.up()
            self.turtle.goto(x + 2, y)
            self.turtle.color('black')
            self.turtle.write(self.tiles[mark], font=('Arial', 30, 'normal'))

        self.screen.update()
        self.screen.ontimer(self.draw, 100)

    def run(self):
        self.turtle.hideturtle()
        self.draw()
        self.screen.mainloop()
