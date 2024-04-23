from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""
        raise NotImplementedError("Метод draw должен быть определен в подклассах.")


class Apple(GameObject):
    """Класс для представления яблока на игровом поле."""

    def __init__(self, occupied_cells):
        super().__init__(self.randomize_position(occupied_cells), APPLE_COLOR)

    def randomize_position(self, occupied_cells):
        """Генерация случайной позиции для яблока."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in occupied_cells:
                return position

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        cur_head_pos = self.get_head_position()
        x, y = self.direction
        new_head_pos = ((cur_head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (cur_head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_head_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def update_direction(self, new_direction):
        """Обновление направления движения змейки."""
        self.next_direction = new_direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс состояния змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            self.draw_cell(position)
        self.draw_cell(self.positions[0])


def handle_keys(snake):
    """Обработка пользовательского ввода."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def update_snake(snake, apple):
    """Обновление состояния змейки."""
    snake.move()
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.position = apple.randomize_position(snake.positions)


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pg.init()

    # Создание экземпляров объектов:
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        # Обработка действий пользователя:
        handle_keys(snake)

        # Обновление состояния змейки:
        update_snake(snake, apple)

        # Отрисовка объектов:
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
