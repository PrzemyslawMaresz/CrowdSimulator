from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from view_elements import ViewModifier
from model import CrowdSimulatorModel


def agent_portrayal(agent):
    if type(agent).__name__ == "Person":
        return {"Shape": "circle", "Filled": "true", "Layer": 0, "Color": "red", "r": 0.5}
    elif type(agent).__name__ == "Wall":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "black", "w": 0.9, "h": 0.9}
    else:
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "lightgreen", "w": 0.9, "h": 0.9}


view_modifier = ViewModifier()

grid = CanvasGrid(agent_portrayal, 150, 50, 1500, 500)
server = ModularServer(CrowdSimulatorModel, [grid, view_modifier], "Crowd Simulation", {"grid_width": 150, "grid_height": 50})
server.port = 8521
server.launch()
