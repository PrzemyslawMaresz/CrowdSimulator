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
                          if self.model.grid.is_cell_empty(step)]
        if possible_steps:
            print(possible_steps)
            best_step = self.model.static_field.find_direction(possible_steps)
            self.model.grid.move_agent(self, best_step)


class Wall(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Exit(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
