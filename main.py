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
BUFFER = 10
key_pressed = None

PIECES = {
    "I": [
        [False, False, False, False],
        [True, True, True, True],
        [False, False, False, False],
        [False, False, False, False],
    ],
    "J": [
        [True, False, False],
        [True, True, True],
        [False, False, False],
    ],
    "L": [
        [False, False, True],
        [True, True, True],
        [False, False, False],
    ],
    "O": [
        [True, True],
        [True, True],
    ],
    "S": [
        [False, True, True],
        [True, True, False],
        [False, False, False],
    ],
    "T": [
        [False, True, False],
        [True, True, True],
        [False, False, False],
    ],
    "Z": [
        [True, True, False],
        [False, True, True],
        [False, False, False],
    ],
}


# GAME SETTINGS
MOVE_RIGHT = "l"
MOVE_LEFT = "j"
ROTATE_CLOCKWISE = "f"
ROTATE_COUNTERCLOCKWISE = "s"


class Tetris:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.pos = [0, BOARD_WIDTH // 2]
        self.current_piece = self.get_new_piece()

    def get_new_piece(self) -> list[list[bool]]:
        return random.choice(list(PIECES.values()))

    def move(self, dir: str) -> None:
        new_pos: list[int] = self.pos.copy()

        if dir == "LEFT":
            new_pos[1] -= 1
        elif dir == "RIGHT":
            new_pos[1] += 1
        elif dir == "DOWN":
            new_pos[0] += 1
        elif dir == "UP":
            new_pos[0] -= 1

        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell and not self.valid([new_pos[0] + i, new_pos[1] + j]):
                    if dir == "DOWN":
                        self.place_piece()
                        return
                    else:
                        return

        self.pos = new_pos

    def rotate(self, dir: str) -> None:
        if dir == "CLOCKWISE":
            new_piece: list[list[bool]] = [
                list(row) for row in zip(*self.current_piece[::-1])
            ]
        elif dir == "COUNTERCLOCKWISE":
            new_piece: list[list[bool]] = [
                list(row) for row in zip(*self.current_piece)
            ][::-1]

        for i, row in enumerate(new_piece):
            for j, cell in enumerate(row):
                if cell and not self.valid([self.pos[0] + i, self.pos[1] + j]):
                    return

        self.current_piece = new_piece

    def valid(self, pos: list[int]) -> bool:
        return (
            0 <= pos[0]
            and pos[0] < BOARD_HEIGHT
            and 0 <= pos[1]
            and pos[1] < BOARD_WIDTH
            and not self.board[pos[0]][pos[1]]
        )

    def place_piece(self) -> None:
        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.pos[0] + i][self.pos[1] + j] = True

        self.current_piece = self.get_new_piece()
        self.pos = [0, BOARD_WIDTH // 2]

    def draw(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        board_to_print = [
            [" #" if self.board[i][j] else " ." for j in range(BOARD_WIDTH)]
            for i in range(BOARD_HEIGHT)
        ]

        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    board_to_print[self.pos[0] + i][self.pos[1] + j] = " #"

        print("\n".join(["".join(row) for row in board_to_print]))

    def update(self, frame_count: int) -> None:
        global key_pressed

        if key_pressed:
            if key_pressed == MOVE_RIGHT:
                self.move("RIGHT")
            elif key_pressed == MOVE_LEFT:
                self.move("LEFT")
            elif key_pressed == ROTATE_CLOCKWISE:
                self.rotate("CLOCKWISE")
            elif key_pressed == ROTATE_COUNTERCLOCKWISE:
                self.rotate("COUNTERCLOCKWISE")
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
