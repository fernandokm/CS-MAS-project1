from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = 0

    def __init__(self, unique_id, model, moore, energy=0):
        super().__init__(unique_id, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """

        self.random_move()

        if self.model.grass:
            self.energy -= 1
            for agent in self.model.grid.get_cell_list_contents([self.pos]):
                if isinstance(agent, GrassPatch) and agent.fully_grown:
                    agent.fully_grown = False
                    self.energy += self.model.sheep_gain_from_food
                    break
            if self.energy == 0:
                self.model.kill(self)

        if self.random.random() < self.model.sheep_reproduce:
            self.model.add_sheep(*self.pos)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, model, moore, energy=None):
        super().__init__(unique_id, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # ... to be completed


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed

    def step(self):
        pass
        # ... to be completed
