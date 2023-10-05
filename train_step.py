import torch


class TrainStep:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma

        self.optimizer = torch.optim.Adam(model.parameters(), lr)
        self.loss_func = torch.nn.MSELoss()

    def step(self, observation, action, points, next_observation, game_over):
        out = self.model(observation)
        target = out.clone()
        
