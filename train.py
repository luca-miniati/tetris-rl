# import torch

from agent import Agent
from game import Game


class TrainAgent:
    def __init__(self):
        self.num_games = 10
        self.max_score = 0

        self.game = Game()
        self.agent = Agent(len(self.game.action_space), self.num_games)

    def train(self):
        for _ in range(self.num_games):
            game_over = False

            while not game_over:
                observation = self.agent.get_observation(self.game)
                action = self.agent.get_random_action()
                action = self.agent.get_action(observation)
                points, game_over, score = self.game.play_step(action)
                next_observation = self.agent.get_observation(self.game)
                self.agent.learn_from_experience(
                    observation, action, points, next_observation, game_over)
                self.agent.save_experience(
                    observation, action, points, next_observation, game_over)

            if game_over:
                self.game.print_game()
                self.game.reset()
                self.agent.num_games_played += 1

                self.agent.update_thresh()

                self.agent.learn_from_past_experiences()

                if score > self.max_score:
                    self.max_score = score
                    torch.save(self.agent.model.state_dict(), 'model.pth')

                # self.game.print_game()
                print(f'Game: {self.agent.num_games_played}, Score: {score}, '
                      f'Max Score: {self.max_score}')


if __name__ == "__main__":
    train = TrainAgent()
    train.train()
