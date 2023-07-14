import random
from collections import deque

from learner import TetrisLearner
from model import DQN


class TetrisAgent:
    def __init__(self, num_classes, mem_size, batch_size):
        self.n_games_played = 0
        self.batch_size = batch_size
        self.model = DQN(num_classes)
        self.learner = TetrisLearner(self.model, lr=0.001, discount_factor=0.5)
        self.replay_memory_buffer = deque(maxlen=mem_size)

    def learn_from_experience(self, state, action, reward, next_state, done):
        self.learner.train_step(state, action, reward, next_state, done)

    def store_to_memory(self, state, action, reward, next_state, done):
        self.replay_memory_buffer.append(
            (state, action, reward, next_state, done)
        )

    def experience_replay(self):
        if len(self.replay_memory_buffer) > self.batch_size:
            mini_sample = random.sample(
                self.replay_memory_buffer,
                self.batch_size
            )
        else:
            mini_sample = self.replay_buffer

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.learner.train_step(states, actions, rewards, next_states, dones)
