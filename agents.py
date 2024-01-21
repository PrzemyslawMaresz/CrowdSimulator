from mesa import Agent
from grid import StaticField


class Person(Agent):

    def __init__(self, unique_id, model, static_field: StaticField, floor_num: int):
        super().__init__(unique_id, model)
        self.floor_num = floor_num
        self.grid = model.grid if floor_num == 1 else model.grid2
        self.static_field = static_field

    def step(self) -> None:
        self.move()

    def move(self) -> None:
        possible_steps = self.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        possible_steps = [step
                          for step in possible_steps
                          if self.grid.is_cell_empty(step)
                          or isinstance(self.grid.get_cell_list_contents(step)[0], Exit)
                          or isinstance(self.grid.get_cell_list_contents(step)[0], EnterStairs)]
        if possible_steps:
            x, y, field_value = self.static_field.find_direction(possible_steps)
            cell_content = self.grid._grid[x][y]
            if field_value == 0:
                if type(cell_content).__name__ == "Exit":
                    self.remove_agent()
                else:
                    self.change_floor(x, y)

            else:
                self.grid.move_agent(self, (x, y))

    def remove_agent(self) -> None:
        self.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def change_floor(self, x: int, y: int) -> None:
        destination = (x, y)
        grid = self.model.first_floor.grid
        if grid.is_cell_empty(destination):
            self.grid.remove_agent(self)
            self.floor_num = 1
            self.grid = grid
            self.static_field = self.model.first_floor.static_field
            grid.place_agent(self, destination)


class Wall(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Exit(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class EnterStairs(Agent):
    def __init__(self, unique_id, model, floor_num: int, destination: (int, int)):
        super().__init__(unique_id, model)
        self.floor_num = floor_num
        self.destination = destination


class ExitStairs(Agent):
    def __init__(self, unique_id, model, floor_num: int):
        super().__init__(unique_id, model)
        self.floor_num = floor_num
