import pygame
import random

# Инициализация Pygame.
pygame.init()

# Параметры окна.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

# Создание окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Иконка яблока и ее расположение.
apple_image = pygame.image.load("apple.png")

# Константы для управления змейкой.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = (255, 255, 255)  # Цвет по умолчанию

    def draw(self):
        """Отрисовывает игровой объект на экране."""
        pass


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)  # По умолчанию вправо.
        self.next_direction = None
        self.body_color = SNAKE_COLOR  # Зеленый цвет.
        self.last = None  # Последний сегмент змейки.

    def reset(self):
        """Метод reset для сброса змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if self.length > 1 and (new_direction[0] * -1,
                                new_direction[1] * -1) == self.direction:
            return  # Не допускаем поворот на 180 градусов.
        if self.next_direction is None:
            self.next_direction = new_direction

    def move(self):
        """Перемещает змейку на один шаг."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head_pos = self.get_head_position()
        x, y = self.direction
        new_head_pos = ((cur_head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (cur_head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.last = self.positions[-1]  # Сохраняем последнюю позицию.
        self.positions.insert(0, new_head_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод draw для отрисовки змейки на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        """Рандомизирует позицию яблока на игровом поле."""
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
                         * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)
                         * GRID_SIZE)

    def draw(self):
        """Яблоко на игровом поле."""
        pygame.draw.rect(screen, APPLE_COLOR,
                         (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)  # Ограничение скорости игры.


# Запуск игры.
if __name__ == "__main__":
    main()
