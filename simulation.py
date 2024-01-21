from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from CanvasSecondGridVisualization import CanvasSecondGrid

from view_elements import ViewModifier
from model import CrowdSimulatorModel


def agent_portrayal(agent):
    if type(agent).__name__ == "Person":
        return {"Shape": "circle", "Filled": "true", "Layer": 0, "Color": "red", "r": 0.5}
    elif type(agent).__name__ == "Wall":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "black", "w": 0.9, "h": 0.9}
    elif type(agent).__name__ == "Exit":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "lightgreen", "w": 0.9, "h": 0.9}
    elif type(agent).__name__ == "EnterStairs":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "darkgray", "w": 0.9, "h": 0.9}
    elif type(agent).__name__ == "ExitStairs":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "lightgray", "w": 0.9, "h": 0.9}


view_modifier = ViewModifier()

grid = CanvasGrid(agent_portrayal, 150, 50, 1200, 400)
grid2 = CanvasSecondGrid(agent_portrayal, 150, 50, 1200, 400)

server = ModularServer(CrowdSimulatorModel, [grid, grid2, view_modifier], "Crowd Simulation", {"grid_width": 150, "grid_height": 50})
server.port = 8521
server.launch()
