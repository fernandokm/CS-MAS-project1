"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from typing import Optional
from random import Random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa import Agent
from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    random: Random

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height: int = 20,
        width: int = 20,
        initial_sheep: int = 100,
        initial_wolves: int = 50,
        sheep_reproduce: float = 0.04,
        wolf_reproduce: float = 0.05,
        wolf_gain_from_food: int = 20,
        grass: bool = True,
        grass_regrowth_time: int = 30,
        sheep_gain_from_food: int = 4,
        moore: bool = True,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep (int): Number of sheep to start with
            initial_wolves (int): Number of wolves to start with
            sheep_reproduce (float): Probability of each sheep reproducing each step
            wolf_reproduce (float): Probability of each wolf reproducing each step
            wolf_gain_from_food (int): Energy a wolf gains from eating a sheep
            grass (bool): Whether to have the sheep eat grass for energy
            grass_regrowth_time (int): How long it takes for a grass patch to regrow
                once it is eaten
            sheep_gain_from_food (int): Energy sheep gain from grass, if enabled.
            moore (bool): if True, may move in all 8 directions.
                Otherwise, only up, left, down and right.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.moore = moore

        # Create common model utils
        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for _ in range(initial_sheep):
            self.add_sheep()

        # Create wolves
        for _ in range(initial_wolves):
            self.add_wolf()

        # Create grass patches for all grid points
        for i in range(width):
            for j in range(height):
                self.add_grass(i, j)

    def kill(self, agent: Agent):
        """
        Remove an agent from model's the scheduler and the grid.

        Args:
            agent (Agent): agent to be removed.
        """
        self.schedule.remove(agent)
        self.grid.remove_agent(agent)

    def add_sheep(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        initial_energy: Optional[int] = None,
    ):
        """
        Create and add a sheep agent to the model, place it on the grid
        and add it to the model scheduler.

        Args:
            x (int, optional): agent x position.
                If None, random initialization in [0, grid.width).
            y (int, optional): agent y position.
                If None, random initialization in [0, grid.height).
            initial_energy (int, optional): Initial energy of the agent.
                If None, uniform random initialization in [0, 2*sheep_gain_from_food).
        """

        # Randomly set unspecified parameters
        if x is None or y is None:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        if initial_energy is None:
            initial_energy = self.random.randrange(0, 2 * self.sheep_gain_from_food)

        # Initialize sheep
        new_sheep = Sheep(self.next_id(), self, self.moore, initial_energy)
        self.grid.place_agent(new_sheep, (x, y))
        self.schedule.add(new_sheep)

    def add_wolf(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        initial_energy: Optional[int] = None,
    ):
        """
        Create and add a wolf agent to the model, place it on the grid
        and add it to the model scheduler.

        Args:
            x (int, optional): agent x position.
                If None, random initialization in [0, grid.width).
            y (int, optional): agent y position.
                If None, random initialization in [0, grid.height).
            initial_energy (int, optional): Initial energy of the agent.
                If None, uniform random initialization in [0, 2*wolf_gain_from_food).
        """

        # Randomly set unspecified parameters
        if x is None or y is None:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        if initial_energy is None:
            initial_energy = self.random.randrange(0, 2 * self.wolf_gain_from_food)

        # Initialize wolf
        new_wolf = Wolf(self.next_id(), self, self.moore, initial_energy)
        self.grid.place_agent(new_wolf, (x, y))
        self.schedule.add(new_wolf)

    def add_grass(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        fully_grown: Optional[bool] = None,
        countdown: Optional[int] = None,
    ):
        """
        Create and add a grass agent to the model, place it on the grid and
        add it to the model scheduler. It has two states: growing and fully grown.
        When growing, each step will reduce a unit of countdown variable.
        When countdown is negative, fully_grown is set to True.

        Args:
            x (int, optional): agent x position.
                If None, random initialization between [0, grid.width].
            y (int, optional): agent y position.
                If None, random initialization between [0, grid.height].
            fully_grown (bool, optional): if True, the grass will be set to
                already grown. If None, it is set randomly to True or False.
            countdown (int, optional): Steps necessary to grow. If None, it is
                set randomly to a range between [0, grass_regrowth_time).
        """

        # Randomly set unspecified parameters
        if x is None:
            x = self.random.randrange(self.grid.width)
        if y is None:
            y = self.random.randrange(self.grid.height)
        if fully_grown is None:
            fully_grown = self.random.randrange(2) == 1
        if countdown is None:
            if fully_grown:
                countdown = self.grass_regrowth_time
            else:
                countdown = self.random.randrange(0, self.grass_regrowth_time)

        # Initialze grass
        new_grass = GrassPatch(self.next_id(), self, fully_grown, countdown)
        self.grid.place_agent(new_grass, (x, y))
        self.schedule.add(new_grass)

    def step(self):
        """
        Performs a step of the model. It call the step() function of
        the scheduler and collect all data from datacollector.
        """
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count: int = 200):
        """
        Run the model for step_count steps.

        Args:
            step_count (int): Number of steps to run.
        """

        for _ in range(step_count):
            self.step()
