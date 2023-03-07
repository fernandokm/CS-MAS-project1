"""
Generalized behavior for random walking, one grid cell at a time.
"""

from mesa import Agent, Model


class RandomWalker(Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    """

    def __init__(self, unique_id: int, model: Model, moore=True):
        """
        unique_id (int) : agent id.
        model (Model): model in which the agent is placed
        moore (bool): If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
