import torch
import torch.nn as nn


class DQN:
    def __init__(self, num_classes):
        self.grid_conv = nn.Sequential(
            nn.Conv2d(  # 10x20 -> 4x9
                in_channels=1,
                out_channels=8,
                kernel_size=3,
                stride=2,
            ),
            nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.Conv2d(  # 4x9 -> 1x4
                in_channels=8,
                out_channels=16,
                kernel_size=3,
                stride=2,
            ),
            nn.BatchNorm2d(16),
        )
        self.grid_lin = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 64),
        )
        self.figure_lin = nn.Sequential(
            nn.Linear(6, 16),
            nn.ReLU(),
            nn.Linear(16, 64),
        )
        self.lin = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        grid, figure = x
        grid = self.grid_conv(grid)
        grid = grid[0]
        grid = self.grid_lin(grid)

        figure = self.figure_lin(figure)

        out = torch.concat((grid, figure), dim=0)
        out = self.lin(out)
        return out
