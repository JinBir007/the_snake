import random

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центр экрана:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=SCREEN_CENTER, body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта на экране."""
        raise NotImplementedError("Метод draw переопределен в подклассах.")


class Apple(GameObject):
    """Класс для представления яблока на игровом поле."""

    def __init__(self, occupied_cells=None):
        super().__init__()
        self.occupied_cells = occupied_cells if occupied_cells else []
        self.randomize_position()

    def randomize_position(self, occupied_cells=None):
        """Генерация случайной позиции для яблока."""
        available_cells = [(x, y) for x in range(GRID_WIDTH)
                           for y in range(GRID_HEIGHT)
                           if (x, y) not in 
                           (self.occupied_cells + (occupied_cells or []))]
        if available_cells:
            self.position = random.choice(available_cells)

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self, position=SCREEN_CENTER,
                 body_color=SNAKE_COLOR, occupied_cells=None):
        super().__init__(position, body_color)
        self.occupied_cells = occupied_cells if occupied_cells else []

    def move(self):
        """Обновление позиции змейки."""
        cur_head_pos = self.get_head_position()
        x, y = self.direction
        new_head_pos = ((cur_head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (cur_head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if new_head_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def update_direction(self, new_direction):
        """Обновление направления движения змейки."""
        self.direction = new_direction

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
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


# Определение функции handle_keys в модуле the_snake
def handle_keys(game_object):
    """Обработка пользовательского ввода."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def update_snake(snake, apple):
    """Обновление состояния змейки."""
    snake.move()
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.position = apple.randomize_position()


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров объектов:
    apple = Apple()
    snake = Snake()

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
        pygame.display.update()


if __name__ == '__main__':
    main()
