from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


COLOR_WOLF = "#CC0000"
COLOR_SHEEP = "#483D8B"
COLOR_GRASS = "#7FFF00"


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLOR_SHEEP,
            "r": 0.3,
            "Layer": 2
        }
    elif type(agent) is Wolf:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLOR_WOLF,
            "r": 0.5,
            "Layer": 1
        }

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal = {
                "Shape": "rect",
                "Filled": "false",
                "Color": COLOR_GRASS,
                "w" : 0.9,
                "h" : 0.9,
                "Layer": 0
            }
        else:
            p = 1 - agent.countdown / agent.model.grass_regrowth_time
            portrayal = {
                "Shape": "rect",
                "Filled": "false",
                "Color": COLOR_GRASS,
                "w" : 0.7 * p,
                "h" : 0.7 * p,
                "Layer": 0
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
