from random import choice, randint
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


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализация игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Отрисовка игрового объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Генерация случайной позиции для яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self, screen):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def move(self):
        """Обновление положения змейки."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head[0] + dx) % SCREEN_WIDTH, (head[1] + dy) % SCREEN_HEIGHT)
        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self, screen):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        # Обновление направления движения змейки:
        if snake.next_direction:
            snake.direction = snake.next_direction
            snake.next_direction = None

        # Обновление положения змейки:
        snake.move()

        # Проверка на съедание яблока:
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        # Отрисовка объектов:
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
