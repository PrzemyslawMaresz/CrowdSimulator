from __future__ import annotations
from mesa.space import SingleGrid
import random


class StaticField:

    def __init__(self, grid: SingleGrid, floor_num: int):
        self.grid = grid
        self.floor_num = floor_num
        self.field: list[list[Cell]] = []
        self.exits_coordinates: list[(int, int)] = []

        self.__set_cells()
        self.__calculate_static_field()

        self.save_field_values()

    def find_direction(self, neighbours: list[(int, int)]) -> (int, int, float):
        directions = [neighbour for neighbour in neighbours]
        min_value = self.get_field_value(min(directions, key=self.get_field_value))
        (x, y) = random.choice([direction
                                for direction in directions
                                if self.get_field_value(direction) == min_value])
        return x, y, min_value

    def get_field_value(self, coordinates: (int, int)) -> float:
        x, y = coordinates
        return self.field[x][y].field_value

    def save_field_values(self):
        file_name = 'static_field1.txt' if self.floor_num == 1 else 'static_field2.txt'
        with open(file_name, 'w') as f:
            for y in range(self.grid.height - 1, -1, -1):
                for x in range(self.grid.width):
                    value = self.field[x][y].field_value
                    formatted_value = "{:.1f}".format(value)
                    if formatted_value == 'inf':
                        formatted_value = '####'
                    l = len(formatted_value)
                    if l < 5:
                        formatted_value += ' ' * (5 - l)
                    print(formatted_value, end=' ', file=f)
                print(file=f)

    def __set_cells(self):

        for x in range(self.grid.width):
            self.field.append([])
            for y in range(self.grid.height):
                cell_content = self.grid._grid[x][y]

                if type(cell_content).__name__ == "EnterStairs" or type(cell_content).__name__ == "Exit":
                    initial_field_value = 0
                else:
                    initial_field_value = float('inf')

                cell = Cell((x, y), initial_field_value, self.__is_obstacle(cell_content), self.__is_exit(cell_content))
                self.field[x].append(cell)
                if self.__is_exit(cell_content):
                    self.exits_coordinates.append((x, y))

    def __calculate_static_field(self):
        queue = []
        for (x, y) in self.exits_coordinates:
            self.__set_not_visited()
            exit_cell = self.field[x][y]
            queue.append(exit_cell)
            exit_cell.was_visited = True

            while queue:
                cell = queue.pop(0)
                neighbourhood = self.__get_empty_neighbourhood(cell.coordinates)
                neighbours_values = []
                for neighbour in neighbourhood:
                    if cell.is_neighbour_diagonal(neighbour):
                        move_value = 1.4
                    else:
                        move_value = 1.0
                    neighbours_values.append(neighbour.field_value + move_value)
                    if not neighbour.was_visited:
                        queue.append(neighbour)
                        neighbour.was_visited = True
                if not cell.is_exit:
                    cell.field_value = min(neighbours_values)

    def __get_empty_neighbourhood(self, coordinates: (int, int)) -> list[Cell]:
        cell_x, cell_y = coordinates
        neighbourhood = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = cell_x + i
                y = cell_y + j
                if self.grid.out_of_bounds((x, y)) or (i == 0 and j == 0):
                    continue
                cell = self.field[x][y]
                if not cell.is_obstacle:
                    neighbourhood.append(cell)
        return neighbourhood

    def __set_not_visited(self):
        for row in self.field:
            for cell in row:
                cell.was_visited = False

    def __is_obstacle(self, cell_content):
        match type(cell_content).__name__:
            case "Wall":
                return True
            case "ExitStairs":
                return True
            case _:
                return False

    def __is_exit(self, cell_content):
        match type(cell_content).__name__:
            case "Exit":
                return True
            case "EnterStairs":
                return True
            case _:
                return False


class Cell:
    def __init__(
            self,
            coordinates: (int, int) = None,
            field_value: float = None,
            is_obstacle: bool = False,
            is_exit: bool = False
    ):
        self.coordinates = coordinates
        self.field_value = field_value
        self.was_visited = False
        self.is_obstacle = is_obstacle
        self.is_exit = is_exit

    def is_neighbour_diagonal(self, other: Cell) -> bool:
        return (abs(self.coordinates[0] - other.coordinates[0]) == 1
                and
                abs(self.coordinates[1] - other.coordinates[1]) == 1)
