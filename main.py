import pygame
import sudoku

pygame.init()

game_over = False
end_time_ms = None
TOP_MARGIN = 50
GAME_STATE = "menu"
difficulty_choice = None

font = pygame.font.SysFont("arial", 30)

WIDTH, HEIGHT = 540, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

def draw_grid(screen):
    cell = 60
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0,0,0),(i*cell, TOP_MARGIN),(i*cell, TOP_MARGIN + 540),thickness)
        pygame.draw.line(screen, (0,0,0),(0, TOP_MARGIN + i*cell),(540, TOP_MARGIN + i*cell),thickness)

def draw_fixed_cells(screen, fixed):
    for r in range(9):
        for c in range(9):
            if fixed[r][c]:
                pygame.draw.rect(screen, (200,200,200), (c*60, TOP_MARGIN+r*60, 60, 60))

def draw_numbers(screen, board, fixed, mistakes):
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                if fixed[r][c]:
                    color = (0,0,0)
                elif mistakes[r][c]:
                    color = (255,0,0)
                else:
                    color = (0,0,255)

                text = font.render(str(board[r][c]), True, color)
                rect = text.get_rect(center=(c*60+30, TOP_MARGIN+r*60+30))
                screen.blit(text, rect)

def draw_selection(screen, selected):
    if selected:
        r, c = selected
        pygame.draw.rect(screen, (180,200,255), (c*60, TOP_MARGIN+r*60, 60, 60), 4)

def is_complete(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return False
            if not sudoku.isValid(board, r, c, board[r][c]):
                return False
    return True

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont("arial", 24)

    def draw(self, screen):
        pygame.draw.rect(screen, (80,80,200), self.rect, border_radius=8)
        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

easy_button   = Button(180, 200, 180, 50, "Easy")
medium_button = Button(180, 280, 180, 50, "Medium")
hard_button   = Button(180, 360, 180, 50, "Hard")

new_game_button = Button(30, 610, 120, 40, "New Game")
solve_button    = Button(180, 610, 120, 40, "Solve")
check_button    = Button(330, 610, 120, 40, "Check")

board = None
fixed = None
selected = None
mistakes = [[False]*9 for _ in range(9)]
start_time = pygame.time.get_ticks()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if GAME_STATE == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if easy_button.is_clicked(pos):
                difficulty_choice = "easy"
            elif medium_button.is_clicked(pos):
                difficulty_choice = "medium"
            elif hard_button.is_clicked(pos):
                difficulty_choice = "hard"
            else:
                continue

            full_board = [[0]*9 for _ in range(9)]
            sudoku.solve(full_board)
            board, fixed = sudoku.generatePuzzle(
                sudoku.copyBoard(full_board), difficulty_choice)

            mistakes = [[False]*9 for _ in range(9)]
            start_time = pygame.time.get_ticks()
            selected = None
            GAME_STATE = "playing"
            continue

        if GAME_STATE == "playing":

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if TOP_MARGIN <= pos[1] < TOP_MARGIN + 540:
                    row = (pos[1] - TOP_MARGIN) // 60
                    col = pos[0] // 60
                    selected = (row, col)

                if new_game_button.is_clicked(pos):
                    GAME_STATE = "menu"
                    selected = None
                    mistakes = [[False]*9 for _ in range(9)]
                    game_over = False
                    end_time_ms = None

                elif solve_button.is_clicked(pos):
                    sudoku.solve(board)
                    if not game_over:
                        end_time_ms = pygame.time.get_ticks()
                    game_over = True
                    mistakes = [[False]*9 for _ in range(9)]

                elif check_button.is_clicked(pos):
                    mistakes = sudoku.checkMistakes(board)

            if event.type == pygame.KEYDOWN and selected and not game_over:
                r, c = selected
                if not fixed[r][c]:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board[r][c] = event.key - pygame.K_0
                    elif event.key == pygame.K_BACKSPACE:
                        board[r][c] = 0

    screen.fill((240,240,240))

    if GAME_STATE == "menu":
        start_time = pygame.time.get_ticks()
        game_over = False
        end_time_ms = None

        title = font.render("Select Difficulty", True, (0,0,0))
        screen.blit(title, (140, 100))

        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

        pygame.display.update()
        continue

    if game_over and end_time_ms is not None:
        elapsed_ms = end_time_ms - start_time
    else:
        elapsed_ms = pygame.time.get_ticks() - start_time

    if is_complete(board):
        if not game_over:
            end_time_ms = pygame.time.get_ticks()
            game_over = True

    elapsed = elapsed_ms // 1000
    timer_text = f"{elapsed//60:02}:{elapsed%60:02}"
    screen.blit(font.render(timer_text, True, (0,0,0)), (10, 10))

    draw_fixed_cells(screen, fixed)
    draw_grid(screen)
    draw_numbers(screen, board, fixed, mistakes)
    draw_selection(screen, selected)

    new_game_button.draw(screen)
    solve_button.draw(screen)
    check_button.draw(screen)

    pygame.display.update()

pygame.quit()
