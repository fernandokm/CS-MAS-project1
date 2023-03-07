from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Slider, Checkbox

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
            "Layer": 2,
        }
    elif type(agent) is Wolf:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": COLOR_WOLF,
            "r": 0.5,
            "Layer": 1,
        }

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal = {
                "Shape": "rect",
                "Filled": "false",
                "Color": COLOR_GRASS,
                "w": 0.9,
                "h": 0.9,
                "Layer": 0,
            }
        else:
            p = 1 - agent.countdown / agent.model.grass_regrowth_time
            portrayal = {
                "Shape": "rect",
                "Filled": "false",
                "Color": COLOR_GRASS,
                "w": 0.7 * p,
                "h": 0.7 * p,
                "Layer": 0,
            }

    return portrayal


model_params = {
    "width": 20,
    "height": 20,
    "grass": Checkbox("Eat grass", value=True),
    "initial_sheep": Slider(
        "Initial sheep", value=100, min_value=0, max_value=400, step=1
    ),
    "initial_wolves": Slider(
        "Initial wolves", value=50, min_value=0, max_value=400, step=1
    ),
    "sheep_reproduce": Slider(
        "Sheep reproduction rate",
        value=0.04,
        min_value=0,
        max_value=1,
        step=0.01,  # type: ignore
    ),
    "wolf_reproduce": Slider(
        "Wolf reproduction rate",
        value=0.05,
        min_value=0,
        max_value=1,
        step=0.01,  # type: ignore
    ),
    "wolf_gain_from_food": Slider(
        "Wolf gain from food", value=20, min_value=0, max_value=30, step=1
    ),
    "grass_regrowth_time": Slider(
        "Grass regrowth time", value=30, min_value=0, max_value=60, step=1
    ),
    "sheep_gain_from_food": Slider(
        "Sheep gain from food", value=4, min_value=0, max_value=30, step=1
    ),
}

canvas_element = CanvasGrid(
    wolf_sheep_portrayal, model_params["width"], model_params["height"], 500, 500
)
chart_element = ChartModule(
    [
        {"Label": "Wolves", "Color": COLOR_WOLF},
        {"Label": "Sheep", "Color": COLOR_SHEEP},
        {"Label": "Fully grown grass", "Color": COLOR_GRASS},
    ]
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
