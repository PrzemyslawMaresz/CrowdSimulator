from mesa import Agent
import math


class Person(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
        self.move()

    @staticmethod
    def distance_to_exit(pos):
        x1, y1 = pos
        x2, y2 = 0, 0
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def move(self) -> None:
        print(self.pos)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        distance = self.distance_to_exit(self.pos)
        for cell in possible_steps:
            if self.model.grid.is_cell_empty(cell):
                new_distance = self.distance_to_exit(cell)
                if new_distance < distance:
                    new_position = cell
                    self.model.grid.move_agent(self, new_position)
                    break


class Wall(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Exit(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
