from mesa import Agent


class Person(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
        self.move()

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        possible_steps = [step
                          for step in possible_steps
                          if self.model.grid.is_cell_empty(step)
                          or isinstance(self.model.grid.get_cell_list_contents(step)[0], Exit)]
        if possible_steps:
            x, y, field_value = self.model.static_field.find_direction(possible_steps)
            if field_value == 0:
                self.remove_agent()
            else:
                self.model.grid.move_agent(self, (x, y))

    def remove_agent(self) -> None:
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)


class Wall(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Exit(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
