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
        # check shapes
        for i in range(observation.shape[0]):
            x = points[i]
            if not game_over[i]:
                x += self.gamma * torch.max(self.model(next_observation[i]))
            target[i][action] = x

        self.optimizer.zero_grad()
        loss = self.loss_func(out, target)
        loss.backward()
        self.optimizer.step()
