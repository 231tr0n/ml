import json
import os
from environment import *
import math


class Agent:
    def __init__(self, alpha, gamma, orientation):
        self.alpha = alpha
        self.orientation = orientation
        self.gamma = gamma
        self.dataset = None
        if not os.path.exists("dataset.json"):
            file = open("dataset.json", "w")
            file_data = {
                "information": {"games": 0, "highest_streak": 0},
                "q_table": {},
            }
            json.dump(file_data, file, indent=4)
            file.close()
        self.env = None

    def dump_dataset(self):
        file = open("dataset.json", "w")
        json.dump(self.dataset, file, indent=4)
        file.close()

    def load_dataset(self):
        file = open("dataset.json", "r")
        self.dataset = json.load(file)
        file.close()

    def state_string_generator(self):
        if self.orientation == "Left":
            return (
                "|"
                + str(self.env.left_slab.position)
                + "|"
                + str(self.env.ball.position)
                + "|"
                + str(self.env.ball.direction)
                + "|"
            )
        elif self.orientation == "Right":
            return (
                "|"
                + str(self.env.right_slab.position)
                + "|"
                + str(self.env.ball.position)
                + "|"
                + str(self.env.ball.direction)
                + "|"
            )

    def reward_generator(self):
        if self.orientation == "Left":
            up = math.dist(
                (self.env.ball.position[0], self.env.ball.position[1]),
                (
                    0 + (self.env.pixel_size / 2),
                    self.env.left_slab.position - self.env.left_slab.step_size,
                ),
            )
            down = math.dist(
                (self.env.ball.position[0], self.env.ball.position[1]),
                (
                    0 + (self.env.pixel_size / 2),
                    self.env.left_slab.position + self.env.left_slab.step_size,
                ),
            )
        elif self.orientation == "Right":
            up = math.dist(
                (self.env.ball.position[0], self.env.ball.position[1]),
                (
                    self.env.display_height - (self.env.pixel_size / 2),
                    self.env.left_slab.position - self.env.left_slab.step_size,
                ),
            )
            down = math.dist(
                (self.env.ball.position[0], self.env.ball.position[1]),
                (
                    self.env.display_height - (self.env.pixel_size / 2),
                    self.env.left_slab.position + self.env.left_slab.step_size,
                ),
            )
        return [down, up]

    def train(self, games_count):
        self.load_dataset()
        self.dataset["information"]["games"] += games_count
        for i in range(games_count):
            self.env = Environment(headless=False)
            boolean = True
            score = 0
            if not self.env.headless:
                self.env.render()
            while boolean:
                temp = self.env.step()
                if temp == "Left" or temp == "Right":
                    boolean = False
                    score = self.env.game_over(temp)
                    if self.dataset["information"]["highest_streak"] < score:
                        self.dataset["information"]["highest_streak"] = score
                    break
                if not self.env.headless:
                    self.env.render()
                state = self.state_string_generator()
                reward = self.reward_generator()
                temp_action = -1
                if reward[0] > reward[1]:
                    temp_action = 1
                else:
                    temp_action = 0
                self.env.right_slab.move(temp_action)
                if self.orientation == "Left":
                    if self.env.right_slab.position > self.env.ball.position[1]:
                        self.env.right_slab.move(1)
                    else:
                        self.env.right_slab.move(0)
                elif self.orientation == "Right":
                    if self.env.left_slab.position > self.env.ball.position[1]:
                        self.env.left_slab.move(1)
                    else:
                        self.env.left_slab.move(0)
                if state not in self.dataset["q_table"]:
                    self.dataset["q_table"][state] = {"up": 0, "down": 0}
                temp1 = self.dataset["q_table"][state]
                if temp_action == 1:
                    self.dataset["q_table"][state]["up"] = round(
                        temp1["up"]
                        + (
                            self.alpha
                            * (
                                reward[temp_action]
                                + (self.gamma * max(temp1["up"], temp1["down"]))
                                - temp1["up"]
                            )
                        ),
                        5,
                    )
                else:
                    self.dataset["q_table"][state]["down"] = round(
                        temp1["down"]
                        + (
                            self.alpha
                            * (
                                reward[temp_action]
                                + (self.gamma * max(temp1["up"], temp1["down"]))
                                - temp1["down"]
                            )
                        ),
                        5,
                    )
        self.dump_dataset()


if __name__ == "__main__":
    agent = Agent(0.1, 0.1, "Right")
    agent.train(10)
