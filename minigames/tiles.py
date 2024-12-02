import threading
from random import choice
from turtle import Screen, up, goto, down, color, begin_fill, forward, left, end_fill, write, update, onscreenclick, done, hideturtle, tracer, shape, fillcolor, stamp
from freegames import floor, vector

class TileGame:
    def __init__(self):
        self.tiles = {}
        self.timer_expired = False
        self.neighbors = [
            vector(100, 0),
            vector(-100, 0),
            vector(0, 100),
            vector(0, -100),
        ]
        self.screen = Screen()
        self.running = True

    def load(self):
        """타일을 로드하고 섞습니다."""
        count = 1

        for y in range(-200, 200, 100):
            for x in range(-200, 200, 100):
                mark = vector(x, y)
                self.tiles[mark] = count
                count += 1

        self.tiles[mark] = None

        for _ in range(1000):
            neighbor = choice(self.neighbors)
            spot = mark + neighbor

            if spot in self.tiles:
                number = self.tiles[spot]
                self.tiles[spot] = None
                self.tiles[mark] = number
                mark = spot

    def square(self, mark, number):
        """검은색 윤곽선과 숫자가 있는 흰색 사각형을 그립니다."""
        up()
        goto(mark.x, mark.y)
        down()

        color('black', 'white')
        begin_fill()
        for _ in range(4):
            forward(99)
            left(90)
        end_fill()

        if number is None:
            return
        elif number < 10:
            forward(20)

        write(number, font=('Arial', 60, 'normal'))

    def draw(self):
        """모든 타일을 그립니다."""
        for mark in self.tiles:
            self.square(mark, self.tiles[mark])
        update()

    def tap(self, x, y):
        """타일과 빈칸을 교체합니다."""
        if self.timer_expired or not self.running:
            return

        x = floor(x, 100)
        y = floor(y, 100)
        mark = vector(x, y)

        for neighbor in self.neighbors:
            spot = mark + neighbor

            if spot in self.tiles and self.tiles[spot] is None:
                number = self.tiles[mark]
                self.tiles[spot] = number
                self.tiles[mark] = None
                self.draw()
                return

    def start_timer(self):
        """1분 타이머 시작"""
        def timeout():
            self.timer_expired = True
            self.show_buttons()

        timer = threading.Timer(60, timeout)
        timer.start()

    def show_buttons(self):
        """타이머 초과 후 버튼 표시"""
        up()
        goto(-100, -50)
        self.draw_button(-100, -50, 'green', "Return to Game")
        goto(100, -50)
        self.draw_button(100, -50, 'blue', "Back to Menu")
        onscreenclick(self.handle_click)
        update()

    def draw_button(self, x, y, button_color, text):
        """버튼을 그립니다."""
        up()
        goto(x, y)

        # 버튼 크기 및 색상
        shape('square')
        fillcolor(button_color)
        stamp()

        # 텍스트 표시
        goto(x, y - 10)
        color('white')
        write(text, align="center", font=("Arial", 12, "bold"))

    def handle_click(self, x, y):
        """버튼 클릭 이벤트 처리"""
        if -150 < x < -50 and -70 < y < -30:  # Return to Game
            self.timer_expired = False
            self.reset_game()
        elif 50 < x < 150 and -70 < y < -30:  # Back to Menu
            self.running = False
            self.cleanup()
            try:
                from mainmenu import MainMenu
                menu = MainMenu()
                menu.run()
            except Exception as e:
                print("Error returning to main menu:", e)

    def reset_game(self):
        """게임을 재설정합니다."""
        self.screen.clear()  # 화면 초기화
        self.screen.title("Tile Puzzle Game")
        self.screen.setup(420, 420, 370, 0)
        hideturtle()
        tracer(False)  # 화면 갱신을 제어
        self.timer_expired = False  # 타이머 상태 초기화
        self.running = True  # 게임 실행 상태 초기화
        self.load()  # 타일 재설정
        self.draw()  # 타일 그리기
        self.start_timer()  # 타이머 재설정
        onscreenclick(self.tap)  # 클릭 이벤트 핸들러 재등록

    def cleanup(self):
        """리소스를 정리합니다."""
        self.screen.clear()

    def run(self):
        """타일 퍼즐 게임 실행"""
        self.screen.title("Tile Puzzle Game")
        self.screen.setup(420, 420, 370, 0)
        hideturtle()
        tracer(False)
        self.load()
        self.draw()
        self.start_timer()
        onscreenclick(self.tap)
        done()


if __name__ == "__main__":
    game = TileGame()
    game.run()
