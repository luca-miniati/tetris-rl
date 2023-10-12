import torch
from model import TetrisModel
import random
from train_step import TrainStep
from collections import deque

LR = 0.001
GAMMA = 0.9
MAX_NUM_PAST_EXPERIENCES = 200_000
NUM_PAST_EXPERIENCES = 2_000
BATCH_SIZE = 64


class Agent:
    def __init__(self, num_actions, num_games):
        self.num_games_played = 0
        self.model = TetrisModel()
        self.train_step_handler = TrainStep(self.model, lr=LR, gamma=GAMMA)
        self.thresh = 1
        self.num_actions = num_actions
        self.num_games = num_games

        self.past_experiences = deque(maxlen=MAX_NUM_PAST_EXPERIENCES)

    def get_observation(self, game):
        image = game.grid_to_image()
        return image

    def get_action(self, observation):
        p = random.random()
        if p < self.thresh:
            i = random.randint(0, self.num_actions - 1)
        else:
            pred = self.model(observation)
            i = torch.argmax(pred).item()
        return i

    def get_random_action(self):
        i = random.randint(0, self.num_actions - 1)
        return i

    def save_experience(self, observation, action, points,
                        next_observation, game_over):
        self.past_experiences.append(
            (observation, action, points,
             next_observation, game_over)
        )

    def learn_from_past_experiences(self):
        experiences = random.sample(
            self.past_experiences,
            min(NUM_PAST_EXPERIENCES, len(self.past_experiences))
        )

        i = 0
        while i < range(len(experiences)):
            observations, actions, points, next_observations, game_overs \
                  = zip(*experiences)

            observations = torch.stack(observations[i:i+BATCH_SIZE])
            actions = torch.stack(actions[i:i+BATCH_SIZE])
            points = torch.stack(points[i:i+BATCH_SIZE])
            next_observations = torch.stack(next_observations[i:i+BATCH_SIZE])
            game_overs = torch.stack(game_overs[i:i+BATCH_SIZE])

            self.train_step_handler.step(
                observations, actions, points, next_observations, game_overs)
            i += BATCH_SIZE

    def learn_from_experience(self, observation, action, points,
                              next_observation, game_over):
        action = torch.tensor(action)
        points = torch.tensor(points)
        self.train_step_handler.step(observation, action, points,
                                     next_observation, game_over)

    def update_thresh(self):
        if self.num_games_played >= 0.8*self.num_games:
            self.thresh = 0
        else:
            self.thresh -= 1/(0.8*self.num_games)
