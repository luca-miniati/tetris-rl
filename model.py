import torch.nn as nn


class TetrisModel(nn.Module):
    def __init__(self, in_channels=1, action_space=5):
        super().__init__()

        self.in_channels = in_channels
        self.action_space = action_space
        self.conv1 = nn.Conv2d(self.in_channels, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.maxpool = nn.MaxPool2d(2)
        self.flatten = nn.Flatten()
        self.linear1 = nn.Linear(1024,  128)
        self.linear2 = nn.Linear(128, 32)
        self.linear3 = nn.Linear(32, self.action_space)
        self.dropout = nn.Dropout(0.25)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)  # [64, 10, 16]
        x = self.maxpool(x)  # [64, 5, 8]
        x = self.conv2(x)  # [128, 5, 8]
        x = self.maxpool(x)  # [128, 2, 4]
        x = self.flatten(x)  # [1024]
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x = self.dropout(x)
        x = self.relu(x)
        x = self.linear3(x)
        return x
