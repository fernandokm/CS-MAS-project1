from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


COLOR_WOLF = "#AA0000"
COLOR_SHEEP = "#666666"


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": "blue",
            "r": 0.5,
            "Layer": 2,
        }
    elif type(agent) is Wolf:
        portrayal = {
            "Wolf": "circle",
            "Filled": "true",
            "Color": "red",
            "r": 0.5,
            "Layer": 1,
        }

    elif type(agent) is GrassPatch:
        portrayal = {
            "Grass": "square",
            "Filled": "true",
            "Color": "green",
            "r": 0.3,
            "Layer": 0,
        }

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": COLOR_WOLF}, {"Label": "Sheep", "Color": COLOR_SHEEP}]
)

model_params = {
    # ... to be completed
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
