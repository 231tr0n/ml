import random
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

pygame.init()
import time


def add_coordinates_with_speed(a, b, s):
    return [a[0] + (b[0] * s), a[1] + (b[1] * s)]


class Colors:
    def __init__(self):
        self.white = [255, 255, 255]
        self.red = [255, 0, 0]
        self.green = [0, 255, 0]
        self.black = [0, 0, 0]
        self.blue = [0, 0, 255]


class Slab:
    def __init__(
        self, size, step_size, orientation, display_height, pixel_size, position
    ):
        self.size = size
        self.step_size = step_size
        self.pixel_size = pixel_size
        self.orientation = orientation
        self.display_height = display_height
        self.position = position
        self.pixel_slab_size = self.size * self.pixel_size
        self.buffer_top_size = 0 + self.pixel_slab_size
        self.buffer_bottom_size = self.display_height - self.pixel_slab_size

    def move(self, movement):
        if movement == 1:
            if self.position - self.step_size < self.buffer_top_size:
                self.position = self.buffer_top_size
            else:
                self.position -= self.step_size
        elif movement == 0:
            if self.position + self.step_size > self.buffer_bottom_size:
                self.position = self.buffer_bottom_size
            else:
                self.position += self.step_size


class Ball:
    def __init__(
        self, speed, display_width, display_height, pixel_size, position, direction
    ):
        self.direction = direction
        self.pixel_size = pixel_size
        self.speed = speed
        self.display_width = display_width
        self.display_height = display_height
        self.radius = self.pixel_size / 2
        self.position = position
        self.buffer_top_size = 0 + (self.radius)
        self.buffer_bottom_size = self.display_height - (self.radius)
        self.buffer_left_size = 0 + (self.radius)
        self.buffer_right_size = self.display_width - (self.radius)
        self.buffer_left_slab_size = 0 + (self.radius) + self.pixel_size
        self.buffer_right_slab_size = (
            self.display_width - (self.radius) - self.pixel_size
        )

    def step(self, left_slab, right_slab):
        if self.position[0] < self.buffer_left_size:
            return "Left"
        if self.position[0] > self.buffer_right_size:
            return "Right"
        temp = 0
        if self.position[1] <= self.buffer_top_size:
            self.direction[1] = 1
        if self.position[1] >= self.buffer_bottom_size:
            self.direction[1] = -1
        if (
            self.position[0] <= self.buffer_left_slab_size
            and self.position[1] >= left_slab.position - left_slab.pixel_slab_size
            and self.position[1] <= left_slab.position + left_slab.pixel_slab_size
        ):
            self.direction[0] = 1
            temp = ["Left", 1]
        if (
            self.position[0] >= self.buffer_right_slab_size
            and self.position[1] >= right_slab.position - right_slab.pixel_slab_size
            and self.position[1] <= right_slab.position + right_slab.pixel_slab_size
        ):
            self.direction[0] = -1
            temp = ["Right", 1]
        self.position = add_coordinates_with_speed(
            self.position, self.direction, self.speed
        )
        return temp


class Display:
    def __init__(self, display_width, display_height):
        self.display_width = display_width
        self.display_height = display_height
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        pygame.display.set_caption("Ping-Pong Tron")

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.update()

    def circle(self, coordinates, radius, color):
        pygame.draw.circle(self.screen, color, coordinates, radius)

    def rect(self, coordinates, color):
        pygame.draw.rect(self.screen, color, coordinates)

    def quit(self):
        pygame.display.quit()
        pygame.quit()


class Environment:
    def __init__(
        self,
        time_delay=0.01,
        ball_speed=10,
        slab_step_size=10,
        pixel_size=30,
        slab_size=2,
        display_width=1500,
        display_height=900,
        headless=False,
        automatic=False,
        left_slab_position=900 / 2,
        right_slab_position=900 / 2,
        ball_position=[1500 / 2, random.randint(100, 800)],
        ball_direction=[random.choice([1, -1]), random.choice([1, -1])],
    ):
        self.headless = headless
        self.score = 0
        self.time_delay = time_delay
        self.automatic = automatic
        self.ball_speed = ball_speed
        self.colors = Colors()
        self.slab_step_size = slab_step_size
        self.pixel_size = pixel_size
        self.slab_size = slab_size
        self.display_width = display_width
        self.display_height = display_height
        self.left_slab = Slab(
            self.slab_size,
            self.slab_step_size,
            1,
            self.display_height,
            self.pixel_size,
            left_slab_position,
        )
        self.right_slab = Slab(
            self.slab_size,
            self.slab_step_size,
            2,
            self.display_height,
            self.pixel_size,
            right_slab_position,
        )
        self.ball = Ball(
            self.ball_speed,
            self.display_width,
            self.display_height,
            self.pixel_size,
            ball_position,
            ball_direction,
        )
        if not self.headless:
            self.display = Display(self.display_width, self.display_height)

    def play(self):
        if not self.headless:
            self.render()
            time.sleep(3)
            boolean = True
            while boolean:
                time.sleep(self.time_delay)
                temp = self.step()
                if temp == "Left" or temp == "Right":
                    boolean = False
                    self.game_over(temp)
                    break
                self.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        boolean = False
                if not self.automatic:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.right_slab.move(1)
                    if keys[pygame.K_DOWN]:
                        self.right_slab.move(0)
                    if keys[pygame.K_w]:
                        self.left_slab.move(1)
                    if keys[pygame.K_s]:
                        self.left_slab.move(0)
                    if keys[pygame.K_q]:
                        boolean = False
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        boolean = False
                    if keys[pygame.K_UP]:
                        self.right_slab.move(1)
                    if keys[pygame.K_DOWN]:
                        self.right_slab.move(0)
                    # 					if self.right_slab.position > self.ball.position[1]:
                    # 						self.right_slab.move(1)
                    # 					else:
                    # 						self.right_slab.move(0)
                    if self.left_slab.position > self.ball.position[1]:
                        self.left_slab.move(1)
                    else:
                        self.left_slab.move(0)

    def step(self):
        temp = self.ball.step(self.left_slab, self.right_slab)
        if type(temp) == list:
            print(temp[0], "has continued the streak of", str(self.score))
            self.score += temp[1]
        return temp

    def game_over(self, orientation):
        print(orientation, "lost with a streak of", str(self.score))
        return self.score

    def render(self):
        if not self.headless:
            self.display.fill(self.colors.black)
            self.display.rect(
                [
                    0,
                    self.left_slab.position - self.left_slab.pixel_slab_size,
                    self.pixel_size,
                    2 * self.left_slab.pixel_slab_size,
                ],
                self.colors.red,
            )
            self.display.rect(
                [
                    self.display_width - self.pixel_size,
                    self.right_slab.position - self.right_slab.pixel_slab_size,
                    self.pixel_size,
                    2 * self.right_slab.pixel_slab_size,
                ],
                self.colors.red,
            )
            self.display.circle(
                [self.ball.position[0], self.ball.position[1]],
                self.ball.radius,
                self.colors.green,
            )
            self.display.update()


if __name__ == "__main__":
    environment = Environment(headless=False, automatic=False, time_delay=0.009)
    environment.play()
