import pygame as py
from pygame.locals import *

py.init()

PLAYING_FIELD = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
WIDTH, HEIGHT = 700, 600
EDGE = WIDTH // 50
FIELD_SIZE = WIDTH // 7
HALF_FIELD_SIZE = FIELD_SIZE // 2
CIRCLE_RADIUS = HALF_FIELD_SIZE - EDGE
WIN = py.display.set_mode((WIDTH, HEIGHT))
HOLE_COLOR = (200, 200, 200)
FONT = py.font.SysFont("comicsans", FIELD_SIZE // 2)
AGAIN_TEXT = FONT.render("Erneut spielen!", 1, "green", "black")
AGAIN_RECT = Rect(WIDTH // 2 - AGAIN_TEXT.get_width() // 2 - 20, HEIGHT // 4 * 2 - AGAIN_TEXT.get_height() // 2 - 10, 
                  AGAIN_TEXT.get_width() + 40, AGAIN_TEXT.get_height() + 20)
QUIT_TEXT = FONT.render("Beenden",1, "red", "black")
QUIT_RECT = Rect(WIDTH // 2 - QUIT_TEXT.get_width() // 2 - 20, HEIGHT // 4 * 3 - QUIT_TEXT.get_height() // 2 - 10, 
                  QUIT_TEXT.get_width() + 40, QUIT_TEXT.get_height() + 20)

def check_winning(won):
    for i in range(6):
        for j in range(7):
            if 0 <= i < 3:  # check diagonals
                if 0 <= j < 4:  
                    test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i+1][j+1] + PLAYING_FIELD[i+2][j+2] + PLAYING_FIELD[i+3][j+3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
                if 3 <= j < 7:
                    test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i+1][j-1] + PLAYING_FIELD[i+2][j-2] + PLAYING_FIELD[i+3][j-3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
            if 3 <= i < 6:
                if 0 <= j < 4:
                    test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i-1][j+1] + PLAYING_FIELD[i-2][j+2] + PLAYING_FIELD[i-3][j+3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
                if 3 <= j < 7:
                    test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i-1][j-1] + PLAYING_FIELD[i-2][j-2] + PLAYING_FIELD[i-3][j-3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
            # check colums
            if i < 3:
                test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i+1][j] + PLAYING_FIELD[i+2][j] + PLAYING_FIELD[i+3][j]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            if i > 2:
                test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i-1][j] + PLAYING_FIELD[i-2][j] + PLAYING_FIELD[i-3][j]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            # check rows
            if j < 4:
                test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i][j+1] + PLAYING_FIELD[i][j+2] + PLAYING_FIELD[i][j+3]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            if j > 2:
                test_won = PLAYING_FIELD[i][j] + PLAYING_FIELD[i][j-1] + PLAYING_FIELD[i][j-2] + PLAYING_FIELD[i][j-3]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
    return won

def player_swap(player):
    player *= -1
    return player

def mark_field(column, player):
    for j in range(5, -1, -1):
        if PLAYING_FIELD[j][column] == 0:
            PLAYING_FIELD[j][column] = player
            break

def check_free(column):
    if PLAYING_FIELD[0][column] == 0:
        return True

def get_clicked(pos):
    x_pos = pos[0] // FIELD_SIZE
    return x_pos

def init_game():
    for i in range(6):
        for j in range(7):
            PLAYING_FIELD[i][j] = 0

def get_player_number(player):
    if player == -1:
        player = 2
    return player

def draw_winner(player):
    draw_window(player)
    player = get_player_number(player)
    if player == 1:
        winner_color = "red"
    else:
        winner_color = "yellow"
    win_text = FONT.render(f"Spieler {player} hat gewonnen.", 1, winner_color, "black")
    py.draw.rect(WIN, "black", (WIDTH // 2 - win_text.get_width() // 2 - 20, 
                                HEIGHT // 4 - win_text.get_height() // 2 - 10, win_text.get_width() + 40, 
                                win_text.get_height() + 20))
    WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 4 - win_text.get_height() // 2))
    py.draw.rect(WIN, "black", AGAIN_RECT)
    WIN.blit(AGAIN_TEXT, (WIDTH // 2 - AGAIN_TEXT.get_width() // 2, HEIGHT // 4 * 2 - AGAIN_TEXT.get_height() // 2))
    py.draw.rect(WIN, "black", QUIT_RECT)
    WIN.blit(QUIT_TEXT, (WIDTH // 2 - QUIT_TEXT.get_width() // 2, HEIGHT // 4 * 3 - QUIT_TEXT.get_height() // 2, 
                  QUIT_TEXT.get_width(), QUIT_TEXT.get_height()))
    py.display.update()
    
def draw_window(player):
    player = get_player_number(player)
    py.display.set_caption(f"Vier gewinnt       Spieler {player} ist am Zug")
    WIN.fill("blue")
    for i in range(6):
        for j in range(7):
            if PLAYING_FIELD[i][j] == 1:
                py.draw.circle(WIN, "red", (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)
            elif PLAYING_FIELD[i][j] == -1:
                py.draw.circle(WIN, "yellow", (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)
            else:
                py.draw.circle(WIN, HOLE_COLOR, (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)

def main():
    player = 1
    run = True
    init_game()
    won = False
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            if not won:
                draw_window(player)
                if event.type == py.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == py.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    mouse_pos = py.mouse.get_pos()
                    column = get_clicked(mouse_pos)
                    free = check_free(column)
                    if free:
                        mark_field(column, player)
                        won = check_winning(won)
                    if not won:
                        player = player_swap(player)
                    

            if won:
                draw_winner(player)
                if event.type == py.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == py.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    mouse_pos = py.mouse.get_pos()
                if AGAIN_RECT.collidepoint(mouse_pos):
                    won = False
                    init_game()
                    player = player_swap(player)
                if QUIT_RECT.collidepoint(mouse_pos):
                    run = False
        
        py.display.update()
    py.quit()

if __name__ == "__main__":
    main()