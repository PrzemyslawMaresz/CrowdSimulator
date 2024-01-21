from floor import Floor


def agent_setup_1(floor):
    # górne pokoje lewa strona
    floor.place_agents((40, 80), (30, 39), 75)
    # górne pokoje prawa strona
    floor.place_agents((86, 123), (30, 39), 75)
    # dolne pokoje
    floor.place_agents((40, 135), (13, 22), 200)
    # sala wykładowa
    floor.place_agents((16, 32), (8, 21), 150)


def exit_setup_1(floor):
    floor.place_exit(82, 39)
    floor.place_exit(83, 39)
    floor.place_exit(84, 39)
    floor.place_exit(147, 26)
    floor.place_exit(147, 25)
    floor.place_exit(147, 24)
    floor.place_exit(24, 36)
    floor.place_exit(25, 36)
    floor.place_exit(24, 36)
    floor.place_exit(26, 36)


class FirstFloor(Floor):
    def __init__(self, model, agent_unique_id):
        super().__init__(model, agent_unique_id, 1)

    def set_agents(self):
        agent_setup_1(self)

    def set_exits(self):
        exit_setup_1(self)

    def set_walls(self):
        self.set_stairs_first_floor()
        self.set_walls_first_floor()


class SecondFloor(Floor):

    def __init__(self, model, agent_unique_id):
        super().__init__(model, agent_unique_id, 2)

    def set_agents(self):
        agent_setup_1(self)

    def place_exits(self):
        exit_setup_1(self)

    def set_walls(self):
        self.set_stairs_second_floor()
        self.set_walls_second_floor()
