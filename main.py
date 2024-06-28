import threading
from getkey import getkey
import random
import time
import os


# CONSTANTS
BOARD_HEIGHT = 20
BOARD_WIDTH = 10
FPS = 60
FRAME_RATE = 1 / FPS
BUFFER = 30
key_pressed = None

PIECES = {
    "I": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ],
    "T": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],
}


# GAME SETTINGS
MOVE_RIGHT = "l"
MOVE_LEFT = "j"


class Tetris:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.pos = [0, BOARD_WIDTH // 2]

    def move(self, dir: str) -> None:
        new_pos = self.pos.copy()

        if dir == "LEFT":
            new_pos[1] -= 1
        elif dir == "RIGHT":
            new_pos[1] += 1
        elif dir == "DOWN":
            new_pos[0] += 1
        elif dir == "UP":
            new_pos[0] -= 1

        if self.valid(new_pos):
            self.pos = new_pos

    def valid(self, pos: list[int]) -> bool:
        return (
            0 <= pos[0]
            and pos[0] < BOARD_HEIGHT
            and 0 <= pos[1]
            and pos[1] < BOARD_WIDTH
            and not self.board[pos[0]][pos[1]]
        )

    def draw(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        board_to_print = [
            [" #" if self.board[i][j] else " ." for j in range(BOARD_WIDTH)]
            for i in range(BOARD_HEIGHT)
        ]
        board_to_print[self.pos[0]][self.pos[1]] = " #"

        print("\n".join(["".join(row) for row in board_to_print]))

    def update(self, frame_count: int) -> None:
        global key_pressed

        if key_pressed:
            if key_pressed == MOVE_RIGHT:
                self.move("RIGHT")
            elif key_pressed == MOVE_LEFT:
                self.move("LEFT")
            key_pressed = None

        if not frame_count % BUFFER:
            self.move("DOWN")
            frame_count %= BUFFER


def key_listener() -> None:
    global key_pressed
    while True:
        key = getkey()

        if key:
            key_pressed = key


def main() -> None:
    game = Tetris()

    thread = threading.Thread(target=key_listener, daemon=True)
    thread.start()

    frame_count: int = 0
    while True:
        frame_count += 1
        game.draw()
        print("Frame Number:", frame_count)
        game.update(frame_count)
        time.sleep(FRAME_RATE)


if __name__ == "__main__":
    main()
