import optuna
from prey_predator.model import WolfSheep
from prey_predator.agents import Wolf, Sheep


def run_model_until_collapse(timeout: int, lb : int = 0, up : int = 400, **model_kwargs) -> float:
    """Runs the model until either the wolf of sheep population collapses.

    Args:
        timeout (int): maximum number of steps
        lb (int) : lower bound to break the simulation
        up (int) : upper bound to break the simulation
        model_kwargs : model args

    Returns:
        obj_val (float): Step count plus the standard deviation in the populations of sheep and wolves
    """
    model = WolfSheep(**model_kwargs)
    step = -1
    for step in range(timeout):
        model.step()

        #collect the data of populations
        wolf_count = model.schedule.get_breed_count(Wolf)
        sheep_count = model.schedule.get_breed_count(Sheep)
        
        # threshold to break the simulation
        if min(wolf_count, sheep_count) <= lb or max(wolf_count, sheep_count) > up:
            break

    df = model.datacollector.get_model_vars_dataframe()
    std = 0
    if step > 0:
        #std of both populations
        std = df["Wolves"].std(ddof=1) + df["Sheep"].std(ddof=1)

    return step + 1 + std


def objective(trial: optuna.Trial, trial_ranges, timeout : int = 100_000, samples : int = 3) -> float:
    """
    Objective function to be optimized. Takes a trial and simulate it with suggested parameters. Run the simulation 'samples' times and return the mean.

    Args:
        trial (optuna.Trial): Object from Optuna to perform suggestions
        timeout (int) : number of steps to break a simulation
        samples (int) : number of simulations to be executed

    Returns:
        obj_val (float) : the mean of running 'samples' simulations
    """

    params = {
        "height": trial_ranges["height"],
        "width": trial_ranges["width"],
        "initial_sheep": trial.suggest_int("initial_sheep", *trial_ranges["initial_sheep"]),
        "initial_wolves": trial.suggest_int("initial_wolves", *trial_ranges["initial_wolves"]),
        "sheep_reproduce": trial.suggest_float("sheep_reproduce", *trial_ranges["sheep_reproduce"]),
        "wolf_reproduce": trial.suggest_float("wolf_reproduce", *trial_ranges["wolf_reproduce"]),
        "wolf_gain_from_food": trial.suggest_int("wolf_gain_from_food", *trial_ranges["wolf_gain_from_food"]),
        "grass": trial.suggest_categorical("grass", trial_ranges["grass"]),
        "grass_regrowth_time": trial.suggest_int("grass_regrowth_time", *trial_ranges["grass_regrowth_time"]),
        "sheep_gain_from_food": trial.suggest_int("sheep_gain_from_food", *trial_ranges["sheep_gain_from_food"]),
        "moore": trial.suggest_categorical("moore", trial_ranges["moore"]),
    }
    
    times = []
    for _ in range(samples):
        times.append(run_model_until_collapse(timeout=timeout, **params))
    return sum(times) / len(times)
