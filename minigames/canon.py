from random import randrange
from turtle import Screen, clear, goto, dot, shapesize, update, ontimer, setup, hideturtle, up, tracer, onscreenclick, listen, shape, write, pencolor, fillcolor, stamp, onkey, done
from freegames import vector

class CannonGame:
    def __init__(self):
        self.ball = vector(-200, -200)
        self.speed = vector(0, 0)
        self.targets = []
        self.game_running = True

    def tap(self, x, y):
        """Respond to screen tap."""
        if not self.inside(self.ball):
            self.ball.x = -199
            self.ball.y = -199
            self.speed.x = (x + 200) / 15
            self.speed.y = (y + 200) / 15

    def inside(self, xy):
        """Return True if xy within screen."""
        return -200 < xy.x < 200 and -200 < xy.y < 200

    def draw(self):
        """Draw ball and targets."""
        clear()
        for target in self.targets:
            goto(target.x, target.y)
            dot(20, 'blue')

        if self.inside(self.ball):
            goto(self.ball.x, self.ball.y)
            dot(6, 'red')

        update()

    def move(self):
        """Move ball and targets."""
        
        if not self.game_running:
            return
        
        if randrange(40) == 0:
            y = randrange(-150, 150)
            target = vector(200, y)
            self.targets.append(target)

        for target in self.targets:
            target.x -= 0.5

        if self.inside(self.ball):
            self.speed.y -= 0.35
            self.ball.move(self.speed)

        dupe = self.targets.copy()
        self.targets.clear()

        for target in dupe:
            if abs(target - self.ball) > 13:
                self.targets.append(target)

        self.draw()

        for target in self.targets:
            if not self.inside(target):
                self.game_over()
                return

        ontimer(self.move, 50)
        
    def game_over(self):
        """Handle game over state."""
        self.game_running = False
        clear()
        up()

        # Display Game Over text
        goto(0, 100)
        pencolor('red')
        write("GAME OVER!", align="center", font=("Arial", 30, "normal"))

        # Display buttons
        self.show_buttons()
        
    def game_over(self):
        """Handle game over state."""
        self.game_running = False
        clear()
        up()

        # Display Game Over text
        goto(0, 100)
        pencolor('red')
        write("GAME OVER!", align="center", font=("Arial", 30, "normal"))

        # Display buttons
        self.show_buttons()

    def show_buttons(self):
        """Display Play Again and Back to Menu buttons."""
        button_spacing = 20  # 버튼 간격
        button_width = 100   # 버튼 기본 너비 (픽셀 단위)
        left_button_x = -(button_width + button_spacing) // 2  # 왼쪽 버튼 X 좌표
        right_button_x = (button_width + button_spacing) // 2  # 오른쪽 버튼 X 좌표

        # 버튼 배치
        self.draw_button(left_button_x, -50, 'green', "Play Again")
        self.draw_button(right_button_x, -50, 'blue', "Back to Menu")

        update()
        onscreenclick(self.handle_click)



    def draw_button(self, x, y, button_color, text):
        """텍스트 크기에 맞춘 버튼 그리기"""
        up()
        goto(x, y)

        # 텍스트 길이에 따라 버튼 크기 동적 조정
        text_length = len(text)
        width = max(3, text_length * 1.5)  # 버튼 너비 계산 (텍스트 길이에 비례)
        height = 2  # 버튼 높이

        # 버튼 그리기
        shapesize(height, width)  # 버튼 크기 설정
        shape('square')
        fillcolor(button_color)
        stamp()

        # 텍스트 쓰기
        goto(x, y - 6)  # 텍스트를 중앙에 맞추기 위해 위치 조정
        pencolor('white')
        write(text, align="center", font=("Arial", 12, "bold"))





    def handle_click(self, x, y):
        """Handle button click events."""
        if not self.game_running:
            # Play Again button
            if -115 < x < -25 and -70 < y < -30:
                self.reset_game()
            # Back to Menu button
            elif 25 < x < 115 and -70 < y < -30:
                self.cleanup()
                try:
                    from mainmenu import MainMenu  # Placeholder for menu functionality
                    menu = MainMenu()
                    menu.run()
                except Exception as e:
                    print("Error returning to main menu:", e)

    def reset_game(self):
        """Reset and restart the game."""
        clear()
        self.__init__()
        self.run()

    def cleanup(self):
        """Clean up resources."""
        clear()
        self.game_running = False

    def run(self):
        """Run the cannon game."""
        screen = Screen()
        setup(420, 420, 370, 0)
        hideturtle()
        up()
        tracer(False)
        listen()
        screen.onscreenclick(self.tap)
        self.move()
        done()
        # screen.mainloop()

if __name__ == "__main__":
    game = CannonGame()
    game.run()