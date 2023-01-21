from settings import *
import pygame
import random

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

font = pygame.font.Font('freesansbold.ttf', 32)

win_screen = font.render('Game won! Press \'r\' to play again!', True, (0, 255, 0))
end_screen = font.render('Game lost! Press \'r\' to start over!', True, (255, 0, 0))

mine = pygame.image.load('images/mine.png')
flag = pygame.image.load('images/flag.png')

mouse = [False, False]
game = 0

class Tiles:

    tiles = []

    def __init__(self, x, y, size_x, size_y, mine):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.mine = mine
        self.text = ''
        self.marked = False

        self.mines_around = 0

        self.revealed = False

    def reveal_empty(self):
        self.revealed = True
        for tile in Tiles.tiles:
            if self.x - 1 <= tile.x <= self.x + 1 and self.y - 1 <= tile.y <= self.y + 1:
                if not tile.revealed and not tile.mine:
                    if not tile.mines_around and not tile.marked:
                        tile.reveal_empty()
                    elif not tile.marked:
                        tile.revealed = True

    def create_surface(self):
        if self.mines_around > 0:
            s = str(self.mines_around)
        else:
            s = ''
        self.text = font.render(s, True, TEXT_COLOR, LAND_TILE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x * self.size_x + self.size_x / 2, self.y * self.size_y + self.size_y / 2)


def start_game(grid_size, mines):
    global game
    game = 0
    grid_size_x, grid_size_y = int(grid_size.split('x')[0]), int(grid_size.split('x')[1])
    total_tiles = grid_size_x * grid_size_y
    tiles = (total_tiles - mines) * [False] + mines * [True]
    random.shuffle(tiles)        
    square_size_x, square_size_y = WIDTH / grid_size_x, HEIGHT / grid_size_y

    for x in range(grid_size_x):
        for y in range(grid_size_y):
            Tiles.tiles.append(Tiles(x, y, square_size_x, square_size_y, tiles[x * grid_size_x + y]))

    for tile in Tiles.tiles:
        for tile2 in Tiles.tiles:
            if tile.x - 1 <= tile2.x <= tile.x + 1 and tile.y - 1 <= tile2.y <= tile.y + 1:
                if tile2.mine:
                    tile.mines_around += 1
            tile.create_surface()

def victory():
    global game
    for tile in Tiles.tiles:
        if not tile.mine and not tile.revealed:
            return
    game = 2

def end_game():
    global game
    game = 1

def click():
    mx, my = pygame.mouse.get_pos()
    for tile in Tiles.tiles:
        if (tile.x * tile.size_x <= mx <= tile.x * tile.size_x + tile.size_x and tile.y * tile.size_y <= my <= tile.y * tile.size_y + tile.size_y):
            if pygame.mouse.get_pressed()[0]:
                if mouse[0]:
                    mouse[0] = False
                    if tile.mine:
                        end_game()
                    if not tile.mines_around and not tile.marked:
                        tile.reveal_empty()
                    else:
                        tile.revealed = True
                    break
            else:
                mouse[0] = True
            if pygame.mouse.get_pressed()[2]:
                if mouse[1]:
                    tile.marked = not tile.marked
                    mouse[1] = False
                    break
            else:
                mouse[1] = True

def update_display():

    for tile in Tiles.tiles:
        if not tile.revealed:
            pygame.draw.rect(win, HIDDEN_TILE, (tile.x * tile.size_x, tile.y * tile.size_y, tile.size_x, tile.size_y))
            if tile.marked:
                win.blit(flag, (tile.x * tile.size_x, tile.y * tile.size_y))
        else:
            pygame.draw.rect(win, LAND_TILE, (tile.x * tile.size_x, tile.y * tile.size_y, tile.size_x, tile.size_y))
            if tile.mine:
                win.blit(mine, (tile.x * tile.size_x, tile.y * tile.size_y))
            else:
                win.blit(tile.text, tile.text_rect)
    
    if game == 1:
        rect = end_screen.get_rect().center
        win.blit(end_screen, (WIDTH / 2 - rect[0], HEIGHT / 2 - rect[1]))
    if game == 2:
        rect = win_screen.get_rect().center
        win.blit(win_screen, (WIDTH / 2 - rect[0], HEIGHT / 2 - rect[1]))

    pygame.display.update()

start_game('16x16', MINE_AMOUNT)

clock = pygame.time.Clock()
interrupted = False

mine = pygame.transform.scale(mine, (Tiles.tiles[0].size_x, Tiles.tiles[0].size_y))
flag = pygame.transform.scale(flag, (Tiles.tiles[0].size_x, Tiles.tiles[0].size_y))

while not interrupted:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            interrupted = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Tiles.tiles = []
                start_game('16x16', MINE_AMOUNT)

    if game == 0:
        click()
    victory()

    update_display()


pygame.quit()