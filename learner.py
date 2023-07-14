import torch
import torch.nn as nn
import torch.optim


class Learner:
    def __init__(self, model, lr, discount_factor):
        self.model = model
        self.lr = lr
        self.gamma = discount_factor

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_func = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.long)
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            value = reward[idx]
            if not done[idx]:
                value = reward[idx] + self.gamma * max(
                    self.model(next_state[idx])
                )

            target[idx][torch.argmax(action[idx]).item()] = value

        self.optimizer.zero_grad()
        loss = self.loss_func(pred, target)
        loss.backward()
        self.optimizer.step()
