import pygame
import random
import auto_py_to_exe

# Инициализация Pygame
pygame.init()

# Определение размеров окна и цвета
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BACKGROUND_COLOR = (0, 0, 0)

# Цвета для различных тетромино
SHAPES_COLORS = [
    (255, 0, 0),   # T - Красный
    (255, 255, 0), # O - Желтый
    (0, 255, 0),   # S - Зеленый
    (0, 255, 255), # Z - Голубой
    (255, 165, 0), # L - Оранжевый
    (0, 0, 255),   # J - Синий
    (179, 0, 255)  # I - Фиолетовый
]

# Определение формы блоков (Тетромино)
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],        # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 1, 1]]           # I
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Функция для отрисовки блока
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Функция для отрисовки всей фигуры
def draw_shape(shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x + off_x, y + off_y, color)

# Функция для проверки, можно ли поставить фигуру
def valid_position(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= len(board[0]) or y + off_y >= len(board):
                    return False
                if y + off_y >= 0 and board[y + off_y][x + off_x]:
                    return False
    return True

# Функция для добавления фигуры на поле
def add_to_board(board, shape, offset, color, color_board):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = 1
                color_board[y + off_y][x + off_x] = color

# Функция для удаления заполненных линий
def clear_lines(board, color_board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    new_color_board = [row for row in color_board if any(cell == (0, 0, 0) for cell in row)]
    lines_cleared = len(board) - len(new_board)
    new_board = [[0] * len(board[0])] * lines_cleared + new_board
    new_color_board = [[(0, 0, 0)] * len(board[0])] * lines_cleared + new_color_board
    return new_board, new_color_board, lines_cleared

# Функция для отображения текста на экране
def draw_text(text, font, color, position):
    label = font.render(text, True, color)
    screen.blit(label, position)

# Основной цикл игры
def main():
    board = [[0] * 10 for _ in range(20)]
    color_board = [[(0, 0, 0)] * 10 for _ in range(20)]  # Массив для хранения цветов блоков на поле
    clock = pygame.time.Clock()
    running = True
    current_shape = random.choice(SHAPES)
    shape_offset = [4, 0]
    color = random.choice(SHAPES_COLORS)
    score = 0

    # Отображение начального текста
    font = pygame.font.SysFont(None, 50)
    draw_text("TETRIS - Press any key to start", font, (255, 255, 255), (50, 250))
    pygame.display.update()
    pygame.time.delay(2000)  # Задержка перед началом игры

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Проверка на завершение игры
        if not valid_position(board, current_shape, shape_offset):
            print(f"Game Over! Your score: {score}")
            running = False

        # Отображение игры
        draw_shape(current_shape, shape_offset, color)
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == 1:
                    draw_block(x, y, color_board[y][x])  # Отображаем цвет из color_board

        # Проверка на завершение линий
        board, color_board, lines_cleared = clear_lines(board, color_board)
        score += lines_cleared

        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [shape_offset[0] - 1, shape_offset[1]]
                    if valid_position(board, current_shape, new_offset):
                        shape_offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [shape_offset[0] + 1, shape_offset[1]]
                    if valid_position(board, current_shape, new_offset):
                        shape_offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [shape_offset[0], shape_offset[1] + 1]
                    if valid_position(board, current_shape, new_offset):
                        shape_offset = new_offset
                elif event.key == pygame.K_UP:
                    new_shape = [list(reversed(col)) for col in zip(*current_shape)]
                    if valid_position(board, new_shape, shape_offset):
                        current_shape = new_shape

        # Обновление позиции фигуры
        shape_offset[1] += 1
        if not valid_position(board, current_shape, shape_offset):
            shape_offset[1] -= 1
            add_to_board(board, current_shape, shape_offset, color, color_board)
            current_shape = random.choice(SHAPES)
            shape_offset = [4, 0]
            color = random.choice(SHAPES_COLORS)  # Новый цвет для следующей фигуры

        pygame.display.update()
        clock.tick(3)  # Уменьшена скорость игры

    pygame.quit()

if __name__ == "__main__":
    main()
