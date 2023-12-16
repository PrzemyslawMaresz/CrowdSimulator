from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from agent import Person, Wall, Exit


class CrowdSimulatorModel(Model):

    def __init__(self, grid_width: int, grid_height: int) -> None:
        super().__init__()
        self.grid = SingleGrid(grid_width, grid_height, False)
        self.schedule = RandomActivation(self)
        self.X = 0
        self.Y = 0

        exit_cell = Exit(1, self)
        self.grid.place_agent(exit_cell, (self.X, self.Y))

        for i in range(200):
            wall = Wall(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x, y)):
                self.grid.place_agent(wall, (x, y))

        for i in range(100):

            x = self.random.randrange(1, self.grid.width - 1)
            y = self.random.randrange(1, self.grid.height - 1)
            if self.grid.is_cell_empty((x, y)):
                agent = Person(i, self)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))

    def step(self) -> None:
        self.schedule.step()
