import random
from agents import Person, Wall, Exit, EnterStairs, ExitStairs
from grid import StaticField


class Floor:

    def __init__(self, model,agent_unique_id: list[int], floor_num: int):
        self.model = model
        self.agent_unique_id = agent_unique_id
        self.floor_num = floor_num
        self.grid = model.grid if floor_num == 1 else model.grid2
        self.set_exits()
        self.set_walls()
        self.static_field = StaticField(self.grid, self.floor_num)
        self.set_agents()

    def set_agents(self):
        pass

    def set_exits(self):
        pass

    def set_walls(self):
        pass

    def place_agents(self, x_range: tuple[int, int], y_range: tuple[int, int], number_of_agents: int):
        i = number_of_agents
        while i > 0:
            x = random.randrange(x_range[0], x_range[1])
            y = random.randrange(y_range[0], y_range[1])
            if self.grid.is_cell_empty((x, y)):
                i -= 1
                agent = Person(self.agent_unique_id.pop(), self.model, self.static_field ,self.floor_num)
                self.model.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))

    def place_wall(self, x: int, y: int):
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(Wall(1, self.model), (x, y))

    def place_exit(self, x: int, y: int):
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(Exit(1, self.model), (x, y))

    def place_enter_stairs(self, x: int, y: int, floor_num: int, destination_x: int, destination_y: int):
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(EnterStairs(1, self.model, floor_num, (destination_x, destination_y)), (x, y))

    def place_exit_stairs(self, x: int, y: int, floor_num: int):
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(ExitStairs(1, self.model, floor_num), (x, y))

    def set_walls_second_floor(self):
        self.set_walls_first_floor()

    def set_walls_first_floor(self):

        liczba_pokoi_w_rzedzie = 17
        szerokosc_korytarza = 7
        wysokosc_sali = 10
        szerokosc_sali = 6
        # lewy_dolny_sali = 38,13
        i = 0

        # full size x
        doors_on_x_134 = [37, 36, 34, 33, 31, 30, 27, 26, 25, 21, 20]
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
                if (x >= 150 or y >= 50):
                    continue
                if x == 134:
                    continue
                if nr_pokoju in [2, 6, 7] and y in [20, 19]:
                    continue
                self.place_wall(x, y)

        # druga strona korytarza
        for nr_pokoju in range(liczba_pokoi_w_rzedzie):
            if nr_pokoju == 15:
                continue
            x = 38 + nr_pokoju * szerokosc_sali
            for wys in range(wysokosc_sali):
                y = 12 + wys + szerokosc_korytarza + wysokosc_sali
                if (x >= 150 or y >= 50):
                    continue
                if x == 134:
                    continue
                if (y, nr_pokoju) in [(31, 1), (32, 1), (31, 3), (32, 3), (31, 6), (32, 6), (31, 12), (32, 12), (35, 9), (36, 9), (30, 10),
                                      (31, 10)]:
                    continue
                self.place_wall(x, y)

        # poziome
        for i in range(38, 135):
            y = 12
            x = i
            self.place_wall(x, y)

            y += wysokosc_sali
            if x not in X_Door_corridor_down:
                self.place_wall(x, y)

            y += szerokosc_korytarza
            if x not in X_Door_corridor_top:
                self.place_wall(x, y)

            y += wysokosc_sali
            self.place_wall(x, y)

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
            self.place_wall(x, y)

        x = 147
        for wys in range(2 * wysokosc_sali + szerokosc_korytarza + 1):
            y = 12 + wys
            if y in doors_on_x_147:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        x = 141
        for wys in range(wysokosc_sali + 2):
            y = 12 + wysokosc_sali + szerokosc_korytarza + wys - 1
            if y in doors_on_x_141:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        x = 126
        for y in range(35, 39):
            self.place_wall(x, y)

        x = 131
        for y in range(30, 33):
            self.place_wall(x, y)

        # poziome
        for i in range(134, 148):
            y = 12
            x = i
            self.place_wall(x, y)

            y += wysokosc_sali
            y += szerokosc_korytarza
            y += wysokosc_sali
            self.place_wall(x, y)

        for i in range(141, 148):
            y = 28
            x = i
            self.place_wall(x, y)

            y = 33
            self.place_wall(x, y)

        for x in range(122, 134):
            y = 35
            if x > 125:
                self.place_wall(x, y)
            y = 32
            if x > 130:
                self.place_wall(x, y)

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
            self.place_wall(x, y)

        x = 12
        for wys in range(wysokosc_sali + 7):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        x = 32
        for wys in range(wysokosc_sali + 7):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        x = 38
        for wys in range(10):
            y = 6 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        for wys in range(5):
            y = 39 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

            ## LEWE GÓRNE
        x = 9
        for wys in range(6):
            y = 37 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        x = 22
        for wys in range(6):
            y = 37 + wys
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)
        x = 28
        for wys in range(23):
            y = 22 + wys
            if y in [24, 25, 30, 31, 33, 34]:
                continue
            if (x >= 150 or y >= 50):
                continue
            self.place_wall(x, y)

        # poziome dolne

        for i in range(7, 39):
            y = 6
            x = i
            self.place_wall(x, y)

        for i in range(7, 39):
            y = wysokosc_sali + 12
            x = i
            if x in [9, 10, 15, 16, 35, 36]:
                continue
            self.place_wall(x, y)

        # poziome górne
        for i in range(10, 22):
            y = 42
            x = i
            self.place_wall(x, y)

        for i in range(28, 39):
            y = 44
            x = i
            self.place_wall(x, y)

        for i in range(7, 39):
            y = 36
            x = i
            if x in [7, 8, 9, 22, 23, 26, 27, 28]:
                self.place_wall(x, y)

        for x in range(29, 38):
            y = 36
            if x not in [30, 31]:
                self.place_wall(x, y)
            y = 32
            if x < 34:
                self.place_wall(x, y)
            y = 29
            if x not in [35, 36]:
                self.place_wall(x, y)

        for y in range(29, 36):
            x = 33
            self.place_wall(x, y)

        self.place_wall(24, 36)
        self.place_wall(25, 36)
        self.place_wall(147, 24)
        self.place_wall(147, 25)
        self.place_wall(147, 26)

    def set_stairs_first_floor(self):
        # prawe schody
        for x in range(143, 147):
            y = 21
            self.place_exit_stairs(x, y, self.floor_num)

        for x in range(139, 147):

            y = 21
            self.place_wall(x, y)

            if x > 142:
                continue
            y = 17
            self.place_wall(x, y)

        for y in range(18, 21):
            x = 139
            self.place_wall(x, y)
            x = 142
            self.place_wall(x, y)

        # lewe schody
        for x in range(19, 22):
            y = 36
            self.place_exit_stairs(x, y, self.floor_num)

        for x in range(13, 19):
            y = 36
            self.place_wall(x, y)
            y = 38
            self.place_wall(x, y)

        for y in range(36, 38):
            x = 13
            self.place_wall(x, y)
            x = 18
            self.place_wall(x, y)

        # środkowe schody

        for y in range(32, 36):
            x = 83
            self.place_wall(x, y)

        for x in range(81, 83):
            y = 35
            self.place_exit_stairs(x, y, self.floor_num)

    def set_stairs_second_floor(self):
        # prawe schody
        for x in range(143, 147):
            y = 20
            self.place_enter_stairs(x, y, self.floor_num, x, y)

        for x in range(139, 147):

            if x > 142:
                y = 19
                self.place_exit_stairs(x, y, self.floor_num)
                continue
            y = 21
            self.place_wall(x, y)

            y = 17
            self.place_wall(x, y)

        for y in range(18, 21):
            x = 139
            self.place_wall(x, y)
            x = 142
            self.place_wall(x, y)

        # lewe schody

        for x in range(19, 22):
            y = 37
            self.place_enter_stairs(x, y, self.floor_num, x, y)
            y = 38
            self.place_exit_stairs(x, y, self.floor_num)

        for x in range(13, 19):
            y = 36
            self.place_wall(x, y)
            y = 38
            self.place_wall(x, y)

        for y in range(36, 38):
            x = 13
            self.place_wall(x, y)
            x = 18
            self.place_wall(x, y)

        # środkowe schody

        for y in range(32, 37):
            x = 83
            self.place_wall(x, y)

        for x in range(81, 83):
            y = 34
            self.place_enter_stairs(x, y, self.floor_num, x, y)
            y = 33
            self.place_exit_stairs(x, y, self.floor_num)
