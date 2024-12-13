import pygame
from my_exceptions import QuitException
import colors as my_colors
from dataclasses import dataclass
from typing import Optional, Tuple
from random import randint
from typing import Optional
from collections import deque


@dataclass(kw_only=True)
class Sprite:
    img: pygame.Surface
    width: int
    height: int


@dataclass(kw_only=True)
class Bubble(Sprite):
    color: str

    def __hash__(self):
        return hash(self.color)


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
    board_pos: Optional[tuple[int, int]] = None


class PythonicBubbleSagaApp:

    margin = 20
    cursor_y = 400

    def __init__(self, difficulty):
        # attributes
        self.width = 1000
        self.height = 600
        self.title = "Pythonic Bubble Sage"
        self.colors = my_colors
        self.bomb = None
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
        self.cheatz = deque(maxlen=9)
        self.pause = False
        self.num_start_rows = min(max(difficulty, 1), self.max_rows)
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

        self.bomb = get_bubble("bomb")

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
            if key[1] < self.num_start_rows:
                game_board[key] = self.bubbles[randint(0, 4)]
        return game_board

    def trigger_bubble(self, game_board: dict, play_bubble: PlayBubble) -> PlayBubble:
        if play_bubble.moving:
            return play_bubble

        play_bubble.moving = True

        pos = [0, self.max_rows]
        while pos[1] >= 0:
            if play_bubble.col % 2 == pos[1] % 2:
                if game_board[(play_bubble.col, pos[1])]:
                    pos[1] += 1
                    pos[0] = min(self.max_cols - 1, max(0, play_bubble.col + (-1)**randint(0, 1)))
                    break
            else:
                if ((play_bubble.col-1, pos[1]) in game_board and game_board[(play_bubble.col-1, pos[1])]) or ((play_bubble.col+1, pos[1]) in game_board and game_board[(play_bubble.col+1, pos[1])]):
                    pos[1] += 1
                    pos[0] = play_bubble.col
                    break
            pos[1] -= 1
            if pos[0] % 2 != pos[1] % 2:
                if pos[0] < self.max_cols:
                    pos[0] += 1
                else:
                    pos[0] -= 1

        play_bubble.board_pos = tuple(pos)
        return play_bubble

    def check_cheatz(self, play_bubble):
        code = "".join(self.cheatz)
        if code == "merryxmas":
            self.cheatz.clear()
            bg_path = "img/bg_xmas.png"
            bg = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(bg, (self.width, self.height))
        if code == "gimmebomb":
            play_bubble.bubble = self.bomb
            self.cheatz.clear()

        return play_bubble

    def check_board(self, pos, board: dict, visited: dict = None):

        if board[pos].color == "bomb":
            explosion = [(pos[0]+c, pos[1]+r) for c in range(-4, 5) for r in range(-2, 3)]
            for n in explosion:
                if n in board:
                    board[n] = None
            return board, visited

        neighbours = [(pos[0]+2, pos[1]), (pos[0]-2, pos[1])]  # same row
        neighbours.extend([(pos[0]+1, pos[1]+1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]-1)])  # upper and lower row
        top_level = False
        if visited is None:
            top_level = True
            visited = {pos: False}

        for neighbour in neighbours:
            if neighbour not in visited:
                if neighbour in board:
                    if board[neighbour] is not None:
                        if board[neighbour].color == board[pos].color:
                            visited[pos] = True
                            visited[neighbour] = True
                            _, visited = self.check_board(neighbour, board, visited=visited)

        if top_level and len(visited) >= 3:
            for pos in visited:
                board[pos] = None

        return board, visited

    def check_finish(self, board: dict):
        if len(set(board.values())) <= 1:
            self.pause = True
            win_path = "img/win.png"
            win = pygame.image.load(win_path)
            pygame.transform.scale(win, (self.width, self.height))
            self.screen.blit(win, (0, 0))
            print("win")
        if max({row for (col, row) in board.keys()}) > self.max_rows:
            self.pause = True
            game_over_path = "img/game_over.png"
            game_over = pygame.image.load(game_over_path)
            pygame.transform.scale(game_over, (self.width, self.height))
            self.screen.blit(game_over, (0, 0))
            print("loose")

    def mainloop(self):
        clock = pygame.time.Clock()
        game_board = {(col, row): None for col in range(self.max_cols) for row in range(self.max_rows+1) if row % 2 == col % 2}
        game_board = self.fill_game_board(game_board)
        cursor_col = 15
        bubbles = list(self.bubbles)
        play_bubble = PlayBubble(bubble=bubbles[randint(0, len(bubbles) - 1)], x=(cursor_col*self.col_width) + self.margin, y=540, moving=False, col=cursor_col)

        while True:
            if self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise QuitException("Got pygame.QUIT event type")
                clock.tick(60)
                continue

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
                        play_bubble = self.trigger_bubble(game_board, play_bubble)
                    if event.key == pygame.K_m:
                        self.cheatz.append("m")
                    if event.key == pygame.K_e:
                        self.cheatz.append("e")
                    if event.key == pygame.K_r:
                        self.cheatz.append("r")
                    if event.key == pygame.K_y:
                        self.cheatz.append("y")
                    if event.key == pygame.K_x:
                        self.cheatz.append("x")
                    if event.key == pygame.K_a:
                        self.cheatz.append("a")
                    if event.key == pygame.K_s:
                        self.cheatz.append("s")
                    if event.key == pygame.K_g:
                        self.cheatz.append("g")
                    if event.key == pygame.K_i:
                        self.cheatz.append("i")
                    if event.key == pygame.K_b:
                        self.cheatz.append("b")
                    if event.key == pygame.K_o:
                        self.cheatz.append("o")

            # Spiellogik hier einfügen (falls erforderlich)
            play_bubble = self.check_cheatz(play_bubble)

            # Hintergrund zeichnen
            self.screen.blit(self.background, (0, 0))

            # Zeichnungen und Updates hier einfügen
            self.draw_cursor(cursor_col)
            self.draw_bubble(play_bubble)
            self.draw_bubbles(game_board)
            if play_bubble.moving:
                play_bubble.y -= 5
                if play_bubble.y < play_bubble.board_pos[1] * play_bubble.bubble.height:
                    if play_bubble.board_pos[1] >= 0:
                        game_board[play_bubble.board_pos] = play_bubble.bubble
                        game_board, _ = self.check_board(play_bubble.board_pos, game_board)
                    play_bubble = PlayBubble(bubble=bubbles[randint(0, len(bubbles) - 1)], x=(cursor_col * self.col_width) + self.margin, y=540, moving=False, col=cursor_col)
            else:
                play_bubble.x = (cursor_col * self.col_width) + self.margin
                play_bubble.col = cursor_col

            # check for game end conditions
            self.check_finish(game_board)
            # Bildschirm aktualisieren
            pygame.display.flip()
            # sleep a while
            clock.tick(60)

    def main(self):
        pygame.init()  # init pygame
        # create display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.mainloop()  # run mainloop


if __name__ == "__main__":
    app = PythonicBubbleSagaApp(1)
    try:
        app.main()  # inits pygame
    except QuitException as err:
        print("Finished Pythonic Bubble Saga")
    finally:
        pygame.quit()  # Pygame beenden
