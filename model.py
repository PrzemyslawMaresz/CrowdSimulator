from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from agents import Person, Wall, Exit
from grid import StaticField


class CrowdSimulatorModel(Model):

    def __init__(self, grid_width: int, grid_height: int) -> None:
        super().__init__()
        self.grid = SingleGrid(grid_width, grid_height, False)
        self.schedule = RandomActivation(self)

        self.grid.place_agent(Exit(1, self), (0, 0))
        self.grid.place_agent(Exit(2, self), (grid_width - 1, grid_height - 1))

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

        self.static_field = StaticField(self.grid)

    def step(self) -> None:
        self.schedule.step()
