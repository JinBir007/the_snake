import random

import pygame

import time

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

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
SNAKE_COLOR = (0, 255, 0)
DEFAULT_BODY_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 5

# Пути к изображениям
APPLE_IMAGE_PATH = "apple.png"
OBSTACLE_IMAGE_PATH = "556.png"

# Настройка игрового окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

# Центр экрана:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Все клетки на поле:
ALL_CELLS = {(x * GRID_SIZE, y * GRID_SIZE)
             for x in range(GRID_WIDTH)
             for y in range(GRID_HEIGHT)}


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=SCREEN_CENTER, body_color=DEFAULT_BODY_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта на экране."""
        raise NotImplementedError("Метод draw переопределен в подклассах.")


class Apple(GameObject):
    """Класс для представления яблока на игровом поле."""

    def __init__(self, position=SCREEN_CENTER):
        super().__init__(position)
        self.image = pygame.image.load(APPLE_IMAGE_PATH)

    def randomize_position(self, occupied_cells=set()):
        """Генерация случайной позиции для яблока."""
        available_cells = ALL_CELLS.copy() - occupied_cells
        if available_cells:
            self.position = random.choice(list(available_cells))

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = self.image.get_rect(topleft=self.position)
        screen.blit(self.image, rect)


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def move(self):
        """Обновление позиции змейки."""
        cur_head_pos = self.get_head_position()
        x, y = self.direction
        new_head_pos = ((cur_head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (cur_head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        # Проверяем столкновение головы змейки с ее телом
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
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


class Obstacle(GameObject):
    """Класс для представления препятствий на игровом поле."""

    def __init__(self, position, body_color=BORDER_COLOR):
        super().__init__(position, body_color)
        self.image = pygame.image.load(OBSTACLE_IMAGE_PATH)

    def draw(self):
        """Отрисовка препятствия на экране."""
        rect = self.image.get_rect(topleft=self.position)
        screen.blit(self.image, rect)


def create_obstacles():
    """Создание препятствий на поле."""
    obstacles = set()
    while len(obstacles) < 10:
        obstacle_position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        obstacles.add(obstacle_position)
    return [Obstacle(position) for position in obstacles]


def handle_keys(gameobject):
    """Обработка пользовательского ввода."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and gameobject.direction != DOWN:
                gameobject.update_direction(UP)
            elif event.key == pygame.K_DOWN and gameobject.direction != UP:
                gameobject.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and gameobject.direction != RIGHT:
                gameobject.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and gameobject.direction != LEFT:
                gameobject.update_direction(RIGHT)


def update_snake(snake, apple, obstacles):
    """Обновление состояния змейки."""
    snake.move()
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position(set(snake.positions))
    # Проверяем столкновение с препятствиями
    if snake.get_head_position() in [obstacle.position for obstacle in obstacles]:
        snake.reset()


def main():
    """Основная функция игры."""

    apple = Apple()
    snake = Snake()
    obstacles = create_obstacles()
    last_time = time.time()

    while True:
        current_time = time.time()
        if current_time - last_time >= 30:
            last_time = current_time
            obstacles = create_obstacles()  # Модификация препятствий каждые 30 секунд

        clock.tick(SPEED)

        handle_keys(snake)

        update_snake(snake, apple, obstacles)

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        for obstacle in obstacles:
            obstacle.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
