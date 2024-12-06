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


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
class PlayBubble:
    bubble: Bubble
    x: int
    y: int
    moving: bool
    col: int


class PythonicBubbleSagaApp:

    margin = 20
    cursor_y = 400



    def __init__(self):
        # attributes
        self.width = 1000
        self.height = 600
        self.title = "Pythonic Bubble Sage"
        self.colors = my_colors
        self.bubbles: Optional[Tuple[Bubble]] = None
        self.bubble_width: int = 60
        self.bubble_height: int = 60
        self.current_bubble_y = 540
        self.col_width = self.bubble_width//2
        self.cursor: Optional[Cursor] = None
        self.background: Optional[pygame.Surface] = None
        self.screen = None
        self.max_rows = 6
        self.max_cols = 31
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
            if bubble:
                bubble_x = self.margin + coord[0]*(bubble.width//2)
                bubble_y = coord[1]*bubble.height
                self.screen.blit(bubble.img, (bubble_x, bubble_y))

    def draw_bubble(self, bubble: PlayBubble):
        self.screen.blit(bubble.bubble.img, (bubble.x, bubble.y))

    def draw_cursor(self, col, bubble_width=60):
        self.screen.blit(self.cursor.img, (col*self.col_width, self.cursor_y))

    def fill_game_board(self, game_board):
        for key in game_board:
            if key[1] < 4:
                game_board[key] = self.bubbles[randint(0, 4)]
        return game_board

    def trigger_bubble(self, game_board: dict, play_bubble: PlayBubble) -> (dict, PlayBubble):
        if play_bubble.moving:
            return game_board, play_bubble

        play_bubble.moving = True

        pos = [0, self.max_rows]
        while True:
            if play_bubble.col % 2 == pos[1] % 2:
                if game_board[(play_bubble.col, pos[1])]:
                    pos[1] += 1
                    pos[0] = play_bubble.col + (-1)**randint(0,1)
                    break
            else:
                if game_board[(play_bubble.col-1, pos[1])] or game_board[(play_bubble.col+1, pos[1])]:
                    pos[1] += 1
                    pos[0] = play_bubble.col
                    break
            pos[1] -= 1

        game_board[(pos[0], pos[1])] = play_bubble.bubble

        return game_board, play_bubble

    def mainloop(self):
        clock = pygame.time.Clock()

        game_board = {(col, row): None for col in range(self.max_cols) for row in range(self.max_rows+1) if row % 2 == col % 2}
        game_board = self.fill_game_board(game_board)
        cursor_col = 15
        bubbles = list(self.bubbles)

        play_bubble = PlayBubble(bubble=bubbles[randint(0, len(bubbles) - 1)], x=(cursor_col*self.col_width) + self.margin, y=540, moving=False, col=cursor_col)

        while True:
            # Events verarbeiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise QuitException("Got pygame.QUIT event type")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        cursor_col = (cursor_col - 1) % self.max_cols
                    if event.key == pygame.K_RIGHT:
                        cursor_col = (cursor_col + 1) % self.max_cols
                    if event.key == pygame.K_SPACE:
                        game_board, play_bubble = self.trigger_bubble(game_board, play_bubble)

            # Spiellogik hier einfügen (falls erforderlich)


            # Hintergrund zeichnen
            self.screen.blit(self.background, (0, 0))

            # Zeichnungen und Updates hier einfügen

            self.draw_cursor(cursor_col)
            self.draw_bubble(play_bubble)
            self.draw_bubbles(game_board)
            if play_bubble.moving:
                play_bubble.y -= 5
            else:
                play_bubble.x = (cursor_col * self.col_width) + self.margin
                play_bubble.col = cursor_col
            if play_bubble.y < 0:
                play_bubble = PlayBubble(bubble=bubbles[randint(0, len(bubbles) - 1)], x=(cursor_col*self.col_width) + self.margin, y=540, moving=False, col=cursor_col)



            # Bildschirm aktualisieren
            pygame.display.flip()

            clock.tick(60)

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
        #sys.exit()
