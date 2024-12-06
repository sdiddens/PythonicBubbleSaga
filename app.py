import pygame
import sys
from my_exceptions import QuitException
import colors as my_colors
from dataclasses import dataclass
from typing import Optional, Tuple
import random
from random import randint

random.seed(42)  # for debug

pygame.init()

@dataclass(kw_only=True)  # TODO add (kw_only=True) to inherit the other with additional members like .color or .pos
class Sprite:
    img: pygame.Surface
    width: int
    height: int


@dataclass(kw_only=True)
class Bubble(Sprite):
    color: str

@dataclass(kw_only=True)
class Cursor(Sprite):
    pass


class PythonicBubbleSagaApp:

    def __init__(self):
        # attributes
        self.width = 1000
        self.height = 600
        self.title = "Pythonic Bubble Sage"
        self.colors = my_colors
        self.bubbles: Optional[Tuple[Bubble]] = None
        self.bubble_width: int = 60
        self.bubble_height: int = 60
        self.cursor: Optional[Cursor] = None
        self.background: Optional[pygame.Surface] = None
        self.screen = None
        # init pygame

        self.load_images()

    def load_images(self):
        bg_path = "img/bg.png"
        bg = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(bg, (self.width, self.height))

        def get_bubble(color: str):
            path = f"img/sprites/bubble_{color}.png"
            img_ori = pygame.image.load(path)#.convert_alpha()
            return Bubble(img=pygame.transform.scale(img_ori, (60, 60)), width=60, height=60, color=color)
        self.bubbles = (get_bubble("blue"),
                        get_bubble("green"),
                        get_bubble("lila"),
                        get_bubble("orange"),
                        get_bubble("red"))

        snake_path = "img/sprites/snake.png"
        snake = pygame.image.load(snake_path)#.convert_alpha()
        self.cursor = Cursor(img=pygame.transform.scale(snake, (100, 200)), width=100, height=200)

    def draw_bubbles(self, game_board):
        bubble_width = self.bubbles[0].width
        for (coord, bubble) in game_board.items():
            bubble_x = 20 + coord[0]*(bubble.width//2)
            bubble_y = coord[1]*bubble.height
            self.screen.blit(bubble.img, (bubble_x, bubble_y))

    def draw_cursor(self, col, bubble_width=60):
        self.screen.blit(self.cursor.img, (col*(bubble_width//2), 400))

    def fill_game_board(self, game_board):
        for key in game_board:
            game_board[key] = self.bubbles[randint(0, 4)]
        return game_board

    def mainloop(self):
        max_rows = 5
        max_cols = 31
        game_board = {(col, row): None for col in range(max_cols) for row in range(max_rows) if row % 2 == col % 2}
        game_board = self.fill_game_board(game_board)
        cursor_col = 15
        while True:
            # Events verarbeiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise QuitException("Got pygame.QUIT event type")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        cursor_col = (cursor_col - 1) % max_cols
                    if event.key == pygame.K_RIGHT:
                        cursor_col = (cursor_col + 1) % max_cols

            # Spiellogik hier einfügen (falls erforderlich)


            # Hintergrund zeichnen
            self.screen.blit(self.background, (0, 0))

            # Zeichnungen und Updates hier einfügen
            self.draw_cursor(cursor_col)
            self.draw_bubbles(game_board)


            # Bildschirm aktualisieren
            pygame.display.flip()

    def main(self):

        # create display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.mainloop()


if __name__ == "__main__":

    app = PythonicBubbleSagaApp()

    # run mainloop
    try:
        app.main()
    except QuitException as err:
        print("Finished Pythonic Bubble Saga")
    finally:
        # Pygame beenden
        pygame.quit()
        sys.exit()
