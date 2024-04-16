
# Базовый класс для игровых объектов
class GameObject:
    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position

    def draw(self):
        pass


# Класс для змейки
class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)  # По умолчанию вправо
        self.next_direction = None
        self.body_color = (0, 255, 0)  # Зеленый цвет

    def update_direction(self, new_direction):
        if self.length > 1 and (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            return  # Не допускаем поворот на 180 градусов
        if self.next_direction is None:
            self.next_direction = new_direction

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head_pos = self.get_head_position()
        x, y = self.direction
        new_head_pos = ((cur_head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH, (cur_head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(screen, self.body_color, (position[0], position[1], GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        return self.positions[0]


# Класс для яблока
class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

    def draw(self):
        screen.blit(apple_image, self.position)


# Функция для обработки нажатий клавиш
def handle_keys(snake):
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


# Функция для основного игрового цикла
def main():
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
        clock.tick(10)  # Ограничение скорости игры


# Запуск игры
if __name__ == "__main__":
    main()
