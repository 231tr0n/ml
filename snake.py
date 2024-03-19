import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import random
import sqlite3


class Snake(object):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    EMPTY = 0
    WALL = 1
    BODY = 2
    HEAD = 3
    FOOD = 4

    def __init__(self, x_pixels, y_pixels):
        if x_pixels < 10 or y_pixels < 10:
            raise Exception(
                "Both x_pixels and y_pixels should be greater than or equal to 10"
            )

        self.__x = x_pixels
        self.__y = y_pixels
        self.__snake = [
            (3, self.__y // 2),
            (2, self.__y // 2),
            (1, self.__y // 2),
        ]
        self.__food = (x_pixels - 2, self.__y // 2)
        self.__movement = Snake.RIGHT
        self.__score = 0
        self.__game_over = False
        self.__matrix = []

        for i in range(self.__x):
            self.__matrix += [[]]
            for j in range(self.__y):
                if i == 0 or i == self.__x - 1:
                    self.__matrix[i] += [Snake.WALL]
                    continue
                if j == 0 or j == self.__y - 1:
                    self.__matrix[i] += [Snake.WALL]
                    continue
                self.__matrix[i] += [Snake.EMPTY]
        self.__matrix[self.__snake[0][0]][self.__snake[0][1]] = Snake.HEAD
        for val in self.__snake[1:]:
            self.__matrix[val[0]][val[1]] = Snake.BODY
        self.__matrix[self.__food[0]][self.__food[1]] = Snake.FOOD

    def get_food(self):
        return self.__food

    def get_snake(self):
        return self.__snake

    def get_score(self):
        return self.__score

    def get_movement(self):
        return self.__movement

    def game_over(self):
        return self.__game_over

    def get_matrix(self):
        return self.__matrix

    def step(self, movement):
        if self.__game_over:
            return
        match movement:
            case "left":
                if self.__movement == Snake.LEFT:
                    self.__movement = Snake.DOWN
                elif self.__movement == Snake.RIGHT:
                    self.__movement = Snake.UP
                elif self.__movement == Snake.UP:
                    self.__movement = Snake.LEFT
                elif self.__movement == Snake.DOWN:
                    self.__movement = Snake.RIGHT
            case "right":
                if self.__movement == Snake.LEFT:
                    self.__movement = Snake.UP
                elif self.__movement == Snake.RIGHT:
                    self.__movement = Snake.DOWN
                elif self.__movement == Snake.UP:
                    self.__movement = Snake.RIGHT
                elif self.__movement == Snake.DOWN:
                    self.__movement = Snake.LEFT

        self.__snake = [
            (
                self.__snake[0][0] + self.__movement[0],
                self.__snake[0][1] + self.__movement[1],
            )
        ] + self.__snake
        self.__matrix[self.__snake[0][0]][self.__snake[0][1]] = Snake.HEAD
        self.__matrix[self.__snake[1][0]][self.__snake[1][1]] = Snake.BODY
        if self.__snake[0] == self.__food:
            self.__score += 1
            available_coordinates = []
            for i in range(1, self.__x - 1):
                for j in range(1, self.__y - 1):
                    if self.__matrix[i][j] == Snake.EMPTY:
                        available_coordinates += [(i, j)]
            self.__food = random.choice(available_coordinates)
            self.__matrix[self.__food[0]][self.__food[1]] = Snake.FOOD
            return
        if (
            self.__snake[0][0] == 0
            or self.__snake[0][0] == self.__x - 1
            or self.__snake[0][1] == 0
            or self.__snake[0][1] == self.__y - 1
        ):
            self.__game_over = True
            return
        for val in self.__snake[1:]:
            if val == self.__snake[0]:
                self.__game_over = True
                return
        self.__matrix[self.__snake[-1][0]][self.__snake[-1][1]] = Snake.EMPTY
        del self.__snake[-1]
        return


class Display(object):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    def __init__(self, x_pixels, y_pixels, pixel_size, tick, name):
        pygame.init()

        self.__clock = pygame.time.Clock()

        if pixel_size < 5:
            raise Exception("Pixel size too small")
        if x_pixels < 10 or y_pixels < 10:
            raise Exception("Both x and y pixels should be greater than or equal to 10")

        self.__x = x_pixels
        self.__y = y_pixels
        self.__tick = tick
        self.__pixel_size = pixel_size

        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(
            (self.__x * self.__pixel_size, self.__y * self.__pixel_size)
        )

    def resize(self, x_pixels, y_pixels, pixel_size):
        if pixel_size < 5:
            raise Exception("Pixel size too small")
        if x_pixels < 10 or y_pixels < 10:
            raise Exception("Both x and y pixels should be greater than or equal to 10")

        self.__x = x_pixels
        self.__y = y_pixels
        self.__pixel_size = pixel_size
        self.screen = pygame.display.set_mode(
            (self.__x * self.__pixel_size, self.__y * self.__pixel_size)
        )

    def change_tick(self, tick):
        self.__tick = tick

    def change_name(self, name):
        pygame.display.set_caption(name)

    def tick(self):
        if self.__tick != 0:
            self.__clock.tick(self.__tick)

    def get_keys(self):
        return pygame.key.get_pressed()

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

    def circle(self, color, coordinates):
        pygame.draw.circle(
            self.screen,
            color,
            (
                (coordinates[0] * self.__pixel_size) + (self.__pixel_size // 2),
                (coordinates[1] * self.__pixel_size) + (self.__pixel_size // 2),
            ),
            self.__pixel_size // 2,
        )

    def rect(self, color, coordinates):
        pygame.draw.rect(
            self.screen,
            color,
            [
                coordinates[0] * self.__pixel_size,
                coordinates[1] * self.__pixel_size,
                self.__pixel_size,
                self.__pixel_size,
            ],
        )

    def quit(self):
        pygame.display.quit()
        pygame.quit()


class Database(object):
    def __init__(self):
        self.__conn = sqlite3.connect("rl.db")
        self.__conn.execute(
            "CREATE TABLE IF NOT EXISTS rl (state TEXT NOT NULL UNIQUE, straight TEXT NOT NULL, left TEXT NOT NULL, right TEXT NOT NULL)"
        )

    def close(self):
        self.__conn.commit()
        self.__conn.close()

    def update(self, state, straight, left, right):
        self.__conn.execute(
            "REPLACE INTO rl (state, straight, left, right) VALUES (?, ?, ?, ?)",
            [state, str(round(straight, 2)), str(round(left, 2)), str(round(right, 2))],
        )

    def get(self, state):
        item = self.__conn.execute(
            "SELECT straight, left, right FROM rl WHERE state = ?", [state]
        ).fetchone()
        if item is None:
            self.update(state, 0.0, 0.0, 0.0)
            return (0.0, 0.0, 0.0)
        return (float(item[0]), float(item[1]), float(item[2]))


class Environment(object):
    def __init__(self, pixel_size, tick):
        self.__x = 10
        self.__y = 10
        self.__display = Display(self.__x, self.__y, pixel_size, tick, "Snake")
        self.__state = []
        self.__db = Database()
        self.__gamma = 0.9
        self.__alpha = 0.1
        self.__no_food_counter = 0
        self.__threshold = 10

        for i in range(self.__x):
            self.__state += [[]]
            for _ in range(self.__y):
                self.__state[i] += [-1]

    def play(self):
        self.__refresh()
        snake = Snake(self.__x, self.__y)
        self.__render(snake.get_matrix())

        while not snake.game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return snake.get_score()

            keys = self.__display.get_keys()
            if keys[pygame.K_q]:
                return snake.get_score()
            elif keys[pygame.K_a]:
                snake.step("left")
            elif keys[pygame.K_d]:
                snake.step("right")
            elif keys[pygame.K_LEFT]:
                snake.step("left")
            elif keys[pygame.K_RIGHT]:
                snake.step("right")
            else:
                snake.step("")

            self.__render(snake.get_matrix())
            self.__display.tick()

        return snake.get_score()

    def agent(self):
        episodes = 0
        highest_score = 0
        action_space = ["", "left", "right"]

        while True:
            episodes += 1
            self.__refresh()
            snake = Snake(self.__x, self.__y)
            self.__render(snake.get_matrix())

            old_body = snake.get_snake()
            old_food = snake.get_food()
            old_state = self.__state_string_generator(old_food, old_body)
            old_q = self.__db.get(old_state)

            while not snake.game_over():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                keys = self.__display.get_keys()
                if keys[pygame.K_q]:
                    return snake.get_score()
                if keys[pygame.K_t]:
                    self.__display.change_tick(
                        int(input("Enter tick[10]: ").strip() or "10")
                    )

                action = 0

                action = old_q.index(max(old_q))
                snake.step(action_space[action])

                new_body = snake.get_snake()
                new_food = snake.get_food()
                new_state = self.__state_string_generator(new_food, new_body)
                new_q = self.__db.get(new_state)

                reward = self.__reward_calculator(
                    snake.game_over(), old_food, new_body, old_body
                )

                # q_value = (1 - self.__alpha) * old_q[action] + self.__alpha * (
                #     reward + self.__gamma * max(new_q)
                # )
                q_value = old_q[action] + self.__alpha * (
                    reward + (self.__gamma * max(new_q)) - old_q[action]
                )

                if action == 0:
                    self.__db.update(old_state, q_value, old_q[1], old_q[2])
                elif action == 1:
                    self.__db.update(old_state, old_q[0], q_value, old_q[2])
                elif action == 2:
                    self.__db.update(old_state, old_q[0], old_q[1], q_value)

                old_body = new_body
                old_food = new_food
                old_state = new_state
                old_q = new_q

                self.__render(snake.get_matrix())
                self.__display.tick()

            if highest_score < snake.get_score():
                highest_score = snake.get_score()
            print(
                "Episode:",
                episodes,
                "|",
                "Score:",
                snake.get_score(),
                "Highest:",
                highest_score,
            )

    def __reward_calculator(self, game_over, food, new, old):
        old_distance = abs(food[0] - old[0][0]) + abs(food[0] - old[0][0])
        new_distance = abs(food[0] - new[0][0]) + abs(food[0] - new[0][1])
        self.__no_food_counter += 1
        if game_over:
            return -1
        if new[0] == food:
            self.__no_food_counter = 0
            return 1
        if self.__no_food_counter > self.__threshold:
            return -1
        if old_distance > new_distance:
            return 0
        return -0.1

    def __state_string_generator(self, food, snake):
        frame_string = ""
        for val in food:
            frame_string += str(val) + ","
        for val in snake:
            for v in val:
                frame_string += str(v) + ","
        return frame_string[:-1]

    def change(self, pixels, pixel_size, tick, name):
        self.__display.resize(pixels, pixels, pixel_size)
        self.__display.change_tick(tick)
        self.__display.change_name(name)
        self.__x = pixels
        self.__y = pixels
        self.__state = []

        for i in range(self.__x):
            self.__state += [[]]
            for _ in range(self.__y):
                self.__state[i] += [-1]

    def destroy(self):
        self.__display.quit()
        self.__db.close()

    def __refresh(self):
        self.__display.fill(Display.BLACK)
        self.__display.update()
        for i in range(self.__x):
            for j in range(self.__y):
                self.__state[i][j] += -1

    def __render(self, matrix):
        for i in range(self.__x):
            for j in range(self.__y):
                if self.__state[i][j] != matrix[i][j]:
                    self.__state[i][j] = matrix[i][j]
                    match self.__state[i][j]:
                        case Snake.FOOD:
                            self.__display.circle(Display.GREEN, (i, j))
                        case Snake.EMPTY:
                            self.__display.rect(Display.BLACK, (i, j))
                        case Snake.WALL:
                            self.__display.rect(Display.RED, (i, j))
                        case Snake.BODY:
                            self.__display.rect(Display.BLUE, (i, j))
                        case Snake.HEAD:
                            self.__display.rect(Display.WHITE, (i, j))
        self.__display.update()


if __name__ == "__main__":
    if (
        int(input("Enter 0 for running agent or 1 for playing game: ").strip() or "0")
        == 0
    ):
        env = Environment(
            int(input("Enter pixel size[40]: ").strip() or "40"),
            int(input("Enter tick[10]: ").strip() or "10"),
        )
        env.agent()
        env.destroy()
    else:
        env = Environment(
            int(input("Enter pixel size[40]: ").strip() or "40"),
            int(input("Enter tick[2]: ").strip() or "2"),
        )
        print("Score:", env.play())
        env.destroy()
