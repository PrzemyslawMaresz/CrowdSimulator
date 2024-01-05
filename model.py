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

        self.set_walls()
        self.set_agents()

        self.static_field = StaticField(self.grid)

    def step(self) -> None:
        self.schedule.step()

    def set_agents(self):
        unique_id = [i for i in range(1000)]
        # górne pokoje lewa strona
        self.__set_agents((40, 80), (30, 39), 75, unique_id)
        # górne pokoje prawa strona
        self.__set_agents((86, 123), (30, 39), 75, unique_id)
        # dolne pokoje
        self.__set_agents((40, 135), (13, 22), 200, unique_id)
        # sala wykładowa
        self.__set_agents((16, 32), (8, 21), 150, unique_id)

    def __set_agents(self, x_range: tuple[int, int], y_range: tuple[int, int], number_of_agents: int, unique_id: list[int]):
        i = number_of_agents
        while i > 0:
            x = self.random.randrange(x_range[0], x_range[1])
            y = self.random.randrange(y_range[0], y_range[1])
            if self.grid.is_cell_empty((x, y)):
                i -= 1
                agent = Person(unique_id.pop(), self)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))

    def set_walls(self):

        self.grid.place_agent(Exit(1, self), (82, 39))
        self.grid.place_agent(Exit(2, self), (83, 39))
        self.grid.place_agent(Exit(3, self), (84, 39))
        self.grid.place_agent(Exit(4, self), (147, 26))
        self.grid.place_agent(Exit(5, self), (147, 25))
        self.grid.place_agent(Exit(6, self), (147, 24))
        self.grid.place_agent(Exit(7, self), (24, 36))
        self.grid.place_agent(Exit(8, self), (25, 36))

        wall = Wall(0, self)

        liczba_pokoi_w_rzedzie = 17
        szerokosc_korytarza = 7
        wysokosc_sali = 10
        szerokosc_sali = 6
        # lewy_dolny_sali = 38,13
        i = 0

        # full size x
        doors_on_x_134 = [37, 36, 34, 33, 31, 30,27, 26, 25, 21, 20]
        doors_on_x_147 = [26, 25, 24]
        X_Door_corridor_top = []
        X_Door_corridor_down = []

        # x from to to 28
        # addtitionl y on y =23,28 form x 141 to 147
        doors_on_x_141 = [35, 34, 30, 29]

        ##
        ## MIDDLE WALLS
        ##
        for i in range(14):
            if i not in [6, 8, 9, 11, 10]:
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 3)
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 4)
            if i == 7:
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 5)
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 6)
            if i == 10:
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 2)
                X_Door_corridor_top.append(38 + szerokosc_sali * i + 3)

        for i in range(14):
            if i not in [2, 5, 7]:
                X_Door_corridor_down.append(38 + szerokosc_sali * i + 3)
                X_Door_corridor_down.append(38 + szerokosc_sali * i + 4)

        # jedna strona korytarza
        for nr_pokoju in range(liczba_pokoi_w_rzedzie):
            if nr_pokoju == 15:
                continue
            x = 38 + nr_pokoju * szerokosc_sali
            for wys in range(wysokosc_sali):
                y = 12 + wys
                print(x, y)
                if (x >= 150 or y >= 50):
                    print(f"za duze x: {x} y: {y}")
                    continue
                if x == 134:
                    continue
                if nr_pokoju in [2, 6, 7] and y in [20, 19]:
                    continue
                self.__place_wall(x, y, wall)

        # druga strona korytarza
        for nr_pokoju in range(liczba_pokoi_w_rzedzie):
            if nr_pokoju == 15:
                continue
            x = 38 + nr_pokoju * szerokosc_sali
            for wys in range(wysokosc_sali):
                y = 12 + wys + szerokosc_korytarza + wysokosc_sali
                print(x, y)
                if (x >= 150 or y >= 50):
                    print(f"za duze x: {x} y: {y}")
                    continue
                if x == 134:
                    continue
                if (y, nr_pokoju) in [(31, 1), (32, 1), (31, 3), (32, 3), (31, 6), (32, 6), (31, 12), (32, 12), (35, 9), (36, 9), (30, 10),
                                      (31, 10)]:
                    continue
                self.__place_wall(x, y, wall)

        # poziome
        for i in range(38, 135):
            y = 12
            x = i
            self.__place_wall(x, y, wall)

            y += wysokosc_sali
            if x not in X_Door_corridor_down:
                self.__place_wall(x, y, wall)

            y += szerokosc_korytarza
            if x not in X_Door_corridor_top:
                self.__place_wall(x, y, wall)

            y += wysokosc_sali
            self.__place_wall(x, y, wall)

        ##
        ## MIDDLE WALLS END
        ##

        ##
        ## RIGHT WALLS
        ##

        x = 134
        for wys in range(2 * wysokosc_sali + szerokosc_korytarza + 1):
            y = 12 + wys
            if y in doors_on_x_134:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 147
        for wys in range(2 * wysokosc_sali + szerokosc_korytarza + 1):
            y = 12 + wys
            if y in doors_on_x_147:
                continue
            if (x >= 150 or y >= 50):
                print(f"za duze x: {x} y: {y}")
                continue
            self.__place_wall(x, y, wall)

        x = 141
        for wys in range(wysokosc_sali + 2):
            y = 12 + wysokosc_sali + szerokosc_korytarza + wys - 1
            if y in doors_on_x_141:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 126
        for y in range(35, 39):
            self.__place_wall(x, y, wall)

        x = 131
        for y in range(30, 33):
            self.__place_wall(x, y, wall)

        # poziome
        for i in range(134, 148):
            y = 12
            x = i
            self.__place_wall(x, y, wall)

            y += wysokosc_sali
            y += szerokosc_korytarza
            y += wysokosc_sali
            self.__place_wall(x, y, wall)

        for i in range(141, 148):
            y = 28
            x = i
            self.__place_wall(x, y, wall)

            y = 33
            self.__place_wall(x, y, wall)

        for x in range(122, 134):
            y = 35
            if x > 125:
                self.__place_wall(x, y, wall)
            y = 32
            if x > 130:
                self.__place_wall(x, y, wall)

        ##
        ## RIGHT WALLS END
        ##

        ##
        ## LEFT WALLS
        ##

        ##
        ## LEWE DOLNE
        x = 7
        for wys in range(2 * wysokosc_sali + szerokosc_korytarza + 3):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 12
        for wys in range(wysokosc_sali + 7):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 32
        for wys in range(wysokosc_sali + 7):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 38
        for wys in range(10):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        for wys in range(5):
            y = 39 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

            ## LEWE GÓRNE
        x = 9
        for wys in range(6):
            y = 37 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        x = 22
        for wys in range(6):
            y = 37 + wys
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)
        x = 28
        for wys in range(23):
            y = 22 + wys
            if y in [24, 25, 30, 31, 33, 34]:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.__place_wall(x, y, wall)

        # poziome dolne

        for i in range(7, 39):
            y = 6
            x = i
            self.__place_wall(x, y, wall)

        for i in range(7, 39):
            y = wysokosc_sali + 12
            x = i
            if x in [9, 10, 15, 16, 35, 36]:
                continue
            self.__place_wall(x, y, wall)

        # poziome górne
        for i in range(10, 22):
            y = 42
            x = i
            self.__place_wall(x, y, wall)

        for i in range(28, 39):
            y = 44
            x = i
            self.__place_wall(x, y, wall)

        for i in range(7, 39):
            y = 36
            x = i
            if x in [7, 8, 9, 22, 23, 26, 27, 28]:
                self.__place_wall(x, y, wall)

        for x in range(29, 38):
            y = 36
            if x not in [30, 31]:
                self.__place_wall(x, y, wall)
            y = 32
            if x < 34:
                self.__place_wall(x, y, wall)
            y = 29
            if x not in [35, 36]:
                self.__place_wall(x, y, wall)

        for y in range(29, 36):
            x = 33
            self.__place_wall(x, y, wall)

        ##
        ## LEFT WALLS END
        ##

    def __place_wall(self, x: int, y: int, wall: Wall):
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(wall, (x, y))
