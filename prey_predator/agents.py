from typing import TYPE_CHECKING

from mesa import Agent
from prey_predator.random_walk import RandomWalker

if TYPE_CHECKING:
    from model import WolfSheep
    from mesa.space import Coordinate


class Sheep(RandomWalker):
    """A sheep that walks araound, reproduces (asexually) and gets eaten."""

    model: "WolfSheep"
    pos: "Coordinate"

    def __init__(
        self, unique_id: int, model: "WolfSheep", moore: bool, energy: int = 0
    ):
        """
        unique_id (int) : agent id.
        model (WolfSheep) : environment model.
        moore (bool): If True, may move in all 8 directions.
            Otherwise, only up, down, left, right.
        energy : agent's initial energy.
        """

        super().__init__(unique_id, model, moore=moore)
        self.energy = energy

    def step(self):
        """Executes a single step of the sheep agent.

        Perfom a random move. Then, eating grass is enabled and there
        is any fully grown grass on the position, eat it.
        Reproduce with a random chance of sheep_reproduce,
        giving half of its energy to its child.
        """

        self.random_move()

        # If eating grass is enabled, consume 1 energy for the random move
        # and try to eat grass
        if self.model.grass:
            self.energy -= 1
            for agent in self.model.grid.get_cell_list_contents([self.pos]):
                if isinstance(agent, GrassPatch) and agent.fully_grown:
                    agent.fully_grown = False
                    self.energy += self.model.sheep_gain_from_food
                    break
            if self.energy <= 0:
                self.model.kill(self)
                return

        # Reproduce randomly and split the energy with the offspring
        if self.random.random() < self.model.sheep_reproduce and self.energy > 1:
            self.model.add_sheep(*self.pos, self.energy // 2)
            self.energy -= self.energy // 2


class Wolf(RandomWalker):
    """A wolf that walks around, reproduces (asexually) and eats sheep."""

    model: WolfSheep
    pos: Coordinate

    def __init__(self, unique_id: int, model: WolfSheep, moore: bool, energy: int = 0):
        """
        unique_id (int) : agent id.
        model (WolfSheep) : environment model.
        moore (bool): If True, may move in all 8 directions.
            Otherwise, only up, down, left, right.
        energy : agent's initial energy.
        """
        super().__init__(unique_id, model, moore=moore)
        self.energy = energy

    def step(self):
        """Executes a single step of the wolf agent.

        Perfom a random move. Then, if there are any sheep on the position,
        eat one of them. Reproduce with a random chance of wolf_reproduce,
        giving half of its energy to its child.
        """
        # Move and consume 1 energy
        self.random_move()
        self.energy -= 1

        # Eat sheep if there are any in the wolf's current position
        # Only the first sheep found is eaten
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if isinstance(agent, Sheep):
                self.energy += self.model.wolf_gain_from_food
                self.model.kill(agent)
                break
        if self.energy <= 0:
            self.model.kill(self)
            return

        # Reproduce randomly and split the energy with the offspring
        if self.random.random() < self.model.wolf_reproduce and self.energy > 1:
            self.model.add_wolf(*self.pos, self.energy // 2)
            self.energy -= self.energy // 2


class GrassPatch(Agent):
    """A patch of grass that grows at a fixed rate and it is eaten by sheep."""

    model: WolfSheep
    pos: Coordinate

    def __init__(
        self, unique_id: int, model: WolfSheep, fully_grown: bool, countdown: int
    ):
        """
        grown: (boolean) Whether the patch of grass is fully grown or not
        countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)

        self.countdown = countdown
        self.fully_grown = fully_grown

    def step(self):
        """Grows the grass if it's not fully grown.

        Perform a step for the grass. If it is already grown, nothing is done.
        Otherwise, reduce the countdown by 1 unit. The grass will be grown when
        the countdown becomes zero.
        """
        if self.fully_grown:
            return

        self.countdown -= 1
        if self.countdown <= 0:
            self.countdown = self.model.grass_regrowth_time
            self.fully_grown = True
