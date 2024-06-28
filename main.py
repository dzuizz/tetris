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
ROTATE_180 = "d"
HARD_DROP = " "
SOFT_DROP = "k"
RESET = "r"


class Tetris:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board: list[list[bool]] = [
            [0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)
        ]
        self.current_piece: list[list[bool]] = self.get_new_piece()
        self.i: int = 0
        self.j: int = BOARD_WIDTH // 2

    def get_new_piece(self) -> list[list[bool]]:
        return random.choice(list(PIECES.values()))

    def move(self, dir: str) -> None:
        new_i: int = self.i
        new_j: int = self.j

        if dir == "LEFT":
            new_j -= 1
        elif dir == "RIGHT":
            new_j += 1
        elif dir == "DOWN":
            new_i += 1
        elif dir == "UP":
            new_i -= 1

        if not self.valid(self.current_piece, new_i, new_j):
            if dir == "DOWN":
                self.place_piece()
            return

        self.i = new_i
        self.j = new_j

    def rotate(self, dir: str) -> None:
        if dir == "CLOCKWISE":
            new_piece: list[list[bool]] = [
                list(row) for row in zip(*self.current_piece[::-1])
            ]
        elif dir == "COUNTERCLOCKWISE":
            new_piece: list[list[bool]] = [
                list(row) for row in zip(*self.current_piece)
            ][::-1]
        elif dir == "180":
            new_piece: list[list[bool]] = [
                row[::-1] for row in self.current_piece[::-1]
            ]

        if not self.valid(new_piece, self.i, self.j):
            return

        self.current_piece = new_piece

    def soft_drop(self) -> None:
        if self.valid(self.current_piece, self.i + 1, self.j):
            self.i += 1
        else:
            self.place_piece()

    def hard_drop(self) -> None:
        while self.valid(self.current_piece, self.i + 1, self.j):
            self.i += 1
        self.place_piece()

    def clear_lines(self) -> None:
        for i, row in enumerate(self.board):
            if all(row):
                self.board.pop(i)
                self.board.insert(0, [False for _ in range(BOARD_WIDTH)])

    def valid(self, piece: list[list[bool]], offset_i: int, offset_j: int) -> bool:
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell:
                    new_i = offset_i + i
                    new_j = offset_j + j

                    if (
                        new_i < 0
                        or new_i >= BOARD_HEIGHT
                        or new_j < 0
                        or new_j >= BOARD_WIDTH
                        or self.board[new_i][new_j]
                    ):
                        return False
        return True

    def place_piece(self) -> None:
        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.i + i][self.j + j] = True

        self.current_piece = self.get_new_piece()
        self.i = 0
        self.j = BOARD_WIDTH // 2

        self.clear_lines()

    def draw(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        board_to_print = [
            [" #" if self.board[i][j] else " ." for j in range(BOARD_WIDTH)]
            for i in range(BOARD_HEIGHT)
        ]

        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    board_to_print[self.i + i][self.j + j] = " #"

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
            elif key_pressed == ROTATE_180:
                self.rotate("180")
            elif key_pressed == HARD_DROP:
                self.hard_drop()
            elif key_pressed == SOFT_DROP:
                self.soft_drop()
            elif key_pressed == RESET:
                self.reset()
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
