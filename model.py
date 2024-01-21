from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from floors_setup import FirstFloor, SecondFloor


class CrowdSimulatorModel(Model):

    def __init__(self, grid_width: int, grid_height: int) -> None:
        super().__init__()
        self.grid = SingleGrid(grid_width, grid_height, False)
        self.grid2 = SingleGrid(grid_width, grid_height, False)

        self.schedule = RandomActivation(self)

        self.unique_id = [i for i in range(10000)]
        self.first_floor = FirstFloor(self, self.unique_id)
        self.second_floor = SecondFloor(self, self.unique_id)

    def step(self) -> None:
        if len(self.schedule.agents) == 0:
            self.running = False
        self.schedule.step()
