from random import choice
from turtle import Screen, up, goto, down, color, begin_fill, forward, left, end_fill, write, update, onscreenclick, done, hideturtle, tracer
from freegames import floor, vector


tiles = {}
neighbors = [
    vector(100, 0),
    vector(-100, 0),
    vector(0, 100),
    vector(0, -100),
]

def load():
    """타일을 로드하고 섞습니다."""
    count = 1

    for y in range(-200, 200, 100):
        for x in range(-200, 200, 100):
            mark = vector(x, y)
            tiles[mark] = count
            count += 1

    tiles[mark] = None

    for _ in range(1000):
        neighbor = choice(neighbors)
        spot = mark + neighbor

        if spot in tiles:
            number = tiles[spot]
            tiles[spot] = None
            tiles[mark] = number
            mark = spot

def square(mark, number):
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

def check_win():
    """타일이 올바른 순서인지 확인하여 완성 여부를 반환합니다."""
    count = 1
    for y in range(-200, 200, 100):
        for x in range(-200, 200, 100):
            mark = vector(x, y)
            if mark == vector(100, -200):
                return tiles[mark] is None
            if tiles[mark] != count:
                return False
            count += 1
    return True

def tap(x, y):
    """타일과 빈칸을 교체합니다."""
    x = floor(x, 100)
    y = floor(y, 100)
    mark = vector(x, y)

    for neighbor in neighbors:
        spot = mark + neighbor

        if spot in tiles and tiles[spot] is None:
            number = tiles[mark]
            tiles[spot] = number
            square(spot, number)
            tiles[mark] = None
            square(mark, None)
            if check_win():
                up()
                goto(-100, 0)
                write("Congratulations!", font=('Arial', 30, 'normal'))
            break

def draw():
    """모든 타일을 그립니다."""
    for mark in tiles:
        square(mark, tiles[mark])
    update()

def run_tile_game():
    """타일 퍼즐 게임 실행"""
    setup = Screen()
    setup.title("Tile Puzzle Game")  # 창 제목 설정
    setup.setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    load()
    draw()
    onscreenclick(tap)
    done()
