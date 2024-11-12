import pygame as pg

from typing import Final

pg.init()

playing_field: list[list[int]] = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
WIDTH: Final[int] = 700
HEIGHT: Final[int] = 600
EDGE: Final[int] = WIDTH // 50
FIELD_SIZE: Final[int] = WIDTH // 7
HALF_FIELD_SIZE: Final[int] = FIELD_SIZE // 2
CIRCLE_RADIUS: Final[int] = HALF_FIELD_SIZE - EDGE
screen: pg.display = pg.display.set_mode((WIDTH, HEIGHT))
HOLE_COLOR: Final[tuple[int]] = (200, 200, 200)
FONT: pg.font.Font = pg.font.SysFont("comicsans", FIELD_SIZE // 2)
AGAIN_TEXT: pg.Surface = FONT.render("Erneut spielen!", 1, "green", "black")
AGAIN_RECT: pg.Rect = pg.Rect(WIDTH // 2 - AGAIN_TEXT.get_width() // 2 - 20, HEIGHT // 4 * 2 - AGAIN_TEXT.get_height() // 2 - 10, 
                              AGAIN_TEXT.get_width() + 40, AGAIN_TEXT.get_height() + 20)
QUIT_TEXT: pg.Surface = FONT.render("Beenden",1, "red", "black")
QUIT_RECT: pg.Rect = pg.Rect(WIDTH // 2 - QUIT_TEXT.get_width() // 2 - 20, HEIGHT // 4 * 3 - QUIT_TEXT.get_height() // 2 - 10, 
                             QUIT_TEXT.get_width() + 40, QUIT_TEXT.get_height() + 20)

def check_winning(won: bool) -> bool:
    """
    Checks if one player has four in a row.
    Args:
    won (bool): Whether the game has been won or not.
    Returns:
    bool: Whether the game has been won or not.
    """
    for i in range(6):
        for j in range(7):
            # check diagonals
            if 0 <= i < 3:
                if 0 <= j < 4:  
                    test_won = playing_field[i][j] + playing_field[i+1][j+1] + playing_field[i+2][j+2] + playing_field[i+3][j+3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
                if 3 <= j < 7:
                    test_won = playing_field[i][j] + playing_field[i+1][j-1] + playing_field[i+2][j-2] + playing_field[i+3][j-3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
            if 3 <= i < 6:
                if 0 <= j < 4:
                    test_won = playing_field[i][j] + playing_field[i-1][j+1] + playing_field[i-2][j+2] + playing_field[i-3][j+3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
                if 3 <= j < 7:
                    test_won = playing_field[i][j] + playing_field[i-1][j-1] + playing_field[i-2][j-2] + playing_field[i-3][j-3]
                    if test_won == 4 or test_won == -4:
                        won = True
                        break
            # check columns
            if i < 3:
                test_won = playing_field[i][j] + playing_field[i+1][j] + playing_field[i+2][j] + playing_field[i+3][j]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            if i > 2:
                test_won = playing_field[i][j] + playing_field[i-1][j] + playing_field[i-2][j] + playing_field[i-3][j]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            # check rows
            if j < 4:
                test_won = playing_field[i][j] + playing_field[i][j+1] + playing_field[i][j+2] + playing_field[i][j+3]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
            if j > 2:
                test_won = playing_field[i][j] + playing_field[i][j-1] + playing_field[i][j-2] + playing_field[i][j-3]
                if test_won == 4 or test_won == -4:
                    won = True
                    break
    return won

def player_swap(player: int) -> int:
    """
    This function swaps the current player with the other player.
    It returns the new player number (1 or -1) and updates the current player number in
    the game state.
    Args:
    player (int): The current player number (1 or -1)
    Returns:
    int: The new player number (1 or -1)
    """
    player *= -1
    return player

def mark_field(column: int, player: int) -> None:
    """
    This function marks the field in the specified column with the specified player.
    Args:
    column (int): The column number (0-6)
    player (int): The player number (1 or -1)
    """
    for j in range(5, -1, -1):
        if playing_field[j][column] == 0:
            playing_field[j][column] = player
            break

def check_free(column: int) -> None | bool:
    """
    This function checks if the specified column is free.
    If the column is free, it returns true. Otherwise, it returns nothing.
    Args:
    column (int): The column number (0-6)
    Returns:
    None | bool: True if the column is free, otherwise nothing
    """
    if playing_field[0][column] == 0:
        return True

def get_clicked(pos: tuple[int]) -> int:
    """
    Calculates and returns the clicked column.
    Args:
    pos (tuple[int]): The position of the click (x, y)
    Returns:
    int: The clicked column (0-6)
    """
    x_pos = pos[0] // FIELD_SIZE
    return x_pos

def init_game() -> None:
    """ Fills the playing field with zero's. """
    for i in range(6):
        for j in range(7):
            playing_field[i][j] = 0

def get_player_number(player: int) -> int:
    """
    Changes the player number from -1 to 2 for the end screen.
    Args:
    player (int): The player number (-1 or 1)
    Returns:
    int: The player number (1 or 2)
    """
    if player == -1:
        player = 2
    return player

def draw_winner(player: int) -> None:
    """
    Draws the end screen with the winner and the again and quit rectangles.
    Args:
    player (int): The player number (1 or -1)
    """
    draw_window(player)
    player = get_player_number(player)
    if player == 1:
        winner_color = "red"
    else:
        winner_color = "yellow"
    win_text = FONT.render(f"Spieler {player} hat gewonnen.", 1, winner_color, "black")
    pg.draw.rect(screen, "black", (WIDTH // 2 - win_text.get_width() // 2 - 20, 
                                HEIGHT // 4 - win_text.get_height() // 2 - 10, win_text.get_width() + 40, 
                                win_text.get_height() + 20))
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 4 - win_text.get_height() // 2))
    pg.draw.rect(screen, "black", AGAIN_RECT)
    screen.blit(AGAIN_TEXT, (WIDTH // 2 - AGAIN_TEXT.get_width() // 2, HEIGHT // 4 * 2 - AGAIN_TEXT.get_height() // 2))
    pg.draw.rect(screen, "black", QUIT_RECT)
    screen.blit(QUIT_TEXT, (WIDTH // 2 - QUIT_TEXT.get_width() // 2, HEIGHT // 4 * 3 - QUIT_TEXT.get_height() // 2, 
                  QUIT_TEXT.get_width(), QUIT_TEXT.get_height()))
    pg.display.update()
    
def draw_window(player: int) -> None:
    """
    Draws the game window with the playing field.
    Args:
    player (int): The player number (-1 or 1)
    """
    player = get_player_number(player)
    pg.display.set_caption(f"Vier gewinnt       Spieler {player} ist am Zug")
    screen.fill("blue")
    for i in range(6):
        for j in range(7):
            if playing_field[i][j] == 1:
                pg.draw.circle(screen, "red", (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)
            elif playing_field[i][j] == -1:
                pg.draw.circle(screen, "yellow", (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)
            else:
                pg.draw.circle(screen, HOLE_COLOR, (j * FIELD_SIZE + HALF_FIELD_SIZE, i * FIELD_SIZE + HALF_FIELD_SIZE), CIRCLE_RADIUS)

def main() -> None:
    """ The main function containing the game loop. """
    player = 1
    run = True
    init_game()
    won = False
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if not won:
                draw_window(player)
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == pg.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    mouse_pos = pg.mouse.get_pos()
                    column = get_clicked(mouse_pos)
                    free = check_free(column)
                    if free:
                        mark_field(column, player)
                        won = check_winning(won)
                    if not won:
                        player = player_swap(player)
                    
            if won:
                draw_winner(player)
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == pg.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    mouse_pos = pg.mouse.get_pos()
                if AGAIN_RECT.collidepoint(mouse_pos):
                    won = False
                    init_game()
                    player = player_swap(player)
                if QUIT_RECT.collidepoint(mouse_pos):
                    run = False
        
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()