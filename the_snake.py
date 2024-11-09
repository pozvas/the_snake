"""Модуль, описывающий логику игры "Змейка"."""

from random import choice

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
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        """Метод, инициализирующий объект класса GameObject."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """
        Это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        Этот метод должен определять,
        как объект будет отрисовываться на экране.
        """
        pass

    def draw_rect(self, position, mode=True) -> None:
        """
        Метод, который предназначен для отрисовки базовой фигуры
        квадрата на игровом поле.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        if mode:
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        else:
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий игровой объект - яблоко."""

    def __init__(self) -> None:
        """Метод, инициализирующий объект класса Apple."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(self.position)

    def randomize_position(self, snake_positions) -> None:
        """
        Метод, устанавливающий случайное
        положение яблока на игровом поле.
        """
        available_positions = set(
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        )

        self.position = choice(
            tuple(available_positions - set(snake_positions))
        )

    def draw(self):
        """Метод, отрисовывающий яблоко на игровом поле."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс, описывающий игровой объект - змейку."""

    def __init__(self, direction=RIGHT) -> None:
        """Метод, инициализирующий объект класса Snake."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.old_position = None
        self.direction = direction
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self) -> None:
        """Метод, обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple=None) -> None:
        """Метод, обновляющий позицию змейки."""
        cur_head = self.get_head_position()
        new_position = (
            (cur_head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (cur_head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        if new_position not in self.positions[2:]:
            self.positions.insert(0, new_position)
            if apple:
                self.length += 1
            if len(self.positions) > self.length:
                self.old_position = self.positions.pop()
        else:
            self.reset()

    def draw(self) -> None:
        """Метод, отрисовывающий змейку на экране."""
        self.draw_rect(self.get_head_position())
        if self.old_position is not None:
            self.draw_rect(self.old_position, False)

    def get_head_position(self) -> tuple:
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def get_snake_positions(self) -> list[tuple]:
        """Метод, возвращающий позиции змейки в массиве."""
        return self.positions

    def reset(self) -> None:
        """
        Метод, сбрасывающий змейку
        в начальное состояние после столкновения с собой.
        """
        direction = choice([UP, DOWN, LEFT, RIGHT])
        self.__init__(direction)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    """
    Функция, обрабатывающая нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    events_dict = {
        (pygame.K_UP, LEFT): UP,
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_RIGHT, UP): RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            game_object.next_direction = events_dict.get(
                (event.key, game_object.direction)
            )


def main():
    """Функция, запускающая игровой процесс."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        apple.draw()
        snake.draw()

        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.move(apple)
            apple.randomize_position(snake.get_snake_positions())
        else:
            snake.move()

        pygame.display.update()


if __name__ == "__main__":
    main()