from collections import defaultdict

from mesa.visualization.modules import CanvasGrid


class CanvasSecondGrid(CanvasGrid):

    def __init__(self,
                 portrayal_method,
                 grid_width,
                 grid_height,
                 canvas_width=500,
                 canvas_height=500):
        super().__init__(portrayal_method, grid_width, grid_height, canvas_width, canvas_height)

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.grid2.width):
            for y in range(model.grid2.height):
                cell_objects = model.grid2.get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    portrayal = self.portrayal_method(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state
