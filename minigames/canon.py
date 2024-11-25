from random import randrange
from turtle import Screen, clear, goto, dot, update, ontimer, setup, hideturtle, up, tracer, onscreenclick, listen, pencolor, fillcolor, write, bgcolor, begin_fill, end_fill, forward, left
import os
import subprocess
import sys

from freegames import vector


class CannonGame:
    def __init__(self):
        self.ball = vector(-200, -200)
        self.speed = vector(0, 0)
        self.targets = []
        self.game_running = True
        self.screen = Screen()  # Screen 객체를 인스턴스 변수로 초기화

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

    def draw_button(self, x, y, text, action):
        """Draw a button and bind it to an action."""
        # Draw button rectangle
        goto(x, y)
        pencolor('black')
        fillcolor('lightgray')
        begin_fill()
        for _ in range(2):
            forward(140)
            left(90)
            forward(40)
            left(90)
        end_fill()

        # Write button text
        goto(x + 70, y + 10)
        write(text, align="center", font=("Arial", 16, "normal"))

        # Store button dimensions for manual click detection
        button_area = {
            "x_start": x,
            "y_start": y,
            "x_end": x + 140,
            "y_end": y + 40,
            "action": action,
        }
        # Add button to a list of clickable areas
        if not hasattr(self, "buttons"):
            self.buttons = []
        self.buttons.append(button_area)

    def handle_click(self, cx, cy):
        """Handle button clicks."""
        # Log the click position
        print(f"Click detected at ({cx}, {cy})")

        # Check if click is within any button bounds
        for button in self.buttons:
            if button["x_start"] <= cx <= button["x_end"] and button["y_start"] <= cy <= button["y_end"]:
                print(f"Button clicked: executing action {button['action'].__name__}")
                button["action"]()
                return
        print("Click outside button bounds.")  # Debug log

    def show_buttons(self):
        """Show Play Again and Main Menu buttons."""
        print("Displaying buttons...")
        self.buttons = []  # Reset the list of clickable areas

        # Draw Play Again button
        self.draw_button(-70, -50, "Play Again", self.restart_game)

        # Draw Main Menu button
        self.draw_button(-70, -120, "Main Menu", self.go_to_main_menu)

        # Rebind onclick to use updated handle_click method
        self.screen.onclick(self.handle_click)




    def restart_game(self):
        """Restart the game."""
        # 게임 상태 초기화
        self.ball = vector(-200, -200)
        self.speed = vector(0, 0)
        self.targets = []
        self.game_running = True
        
        # 화면 초기화
        clear()
        
        # 게임 재시작
        self.screen.onscreenclick(self.tap)
        self.move()

    def go_to_main_menu(self):
        """Go to the main menu."""
        self.cleanup()
        self.launch_main_menu()

    def launch_main_menu(self):
        """Launch the main menu."""
        python_executable = sys.executable  # Get the Python executable path
        mainmenu_path = os.path.join(os.path.dirname(__file__), "mainmenu.py")  # Path to mainmenu.py
        subprocess.Popen([python_executable, mainmenu_path])


    def cleanup(self):
        """Clean up resources."""
        clear()
        self.game_running = False
        # Stop handling events before closing the screen
        self.screen.onclick(None)  # Remove click events
        try:
            self.screen.bye()  # Turtle 창을 완전히 닫음
        except Exception as e:
            print(f"Error closing Turtle screen: {e}")  # Debug log

    def run(self):
        """Run the cannon game."""
        setup(420, 420, 370, 0)
        self.screen.bgcolor('white')  # self.screen을 사용하여 Screen 객체에 접근
        hideturtle()
        up()
        tracer(False)
        listen()
        self.screen.onscreenclick(self.tap)
        self.move()
        self.screen.mainloop()


if __name__ == "__main__":
    game = CannonGame()
    game.run()
