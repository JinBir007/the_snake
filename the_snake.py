import pygame
import random

# Инициализация Pygame.
pygame.init()

# Параметры окна.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BACKGROUND_COLOR = (0, 0, 0)

# Создание окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Иконка яблока и ее расположение.
apple_image = pygame.image.load("apple.png")


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position

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
        self.body_color = (0, 255, 0)  # Зеленый цвет.

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
        self.positions.insert(0, new_head_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             (position[0], position[1], GRID_SIZE, GRID_SIZE))

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
        screen.blit(apple_image, self.position)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((1, 0))


def main():
    """Основная функция игры."""
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(10)  # Ограничение скорости игры.


# Запуск игры.
if __name__ == "__main__":
    main()
