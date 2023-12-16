from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from model import CrowdSimulatorModel


def agent_portrayal(agent):
    if type(agent).__name__ == "Person":
        return {"Shape": "circle", "Filled": "true", "Layer": 0, "Color": "red", "r": 0.5}
    elif type(agent).__name__ == "Wall":
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "black", "w": 0.9, "h": 0.9}
    else:
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "green", "w": 0.9, "h": 0.9}


grid = CanvasGrid(agent_portrayal, 50, 50, 700, 700)
server = ModularServer(CrowdSimulatorModel, [grid], "Crowd Simulation", {"grid_width": 50, "grid_height": 50})
server.port = 8521
server.launch()
