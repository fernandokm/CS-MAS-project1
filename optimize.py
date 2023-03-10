import optuna
from prey_predator.model import WolfSheep
from prey_predator.agents import Wolf, Sheep


def run_model_until_collapse(timeout: int, **model_kwargs):
    """Runs the model until either the wolf of sheep population collapses.

    Args:
        timeout (int): maximum number of steps

    Returns:
        Step count plus the standard deviation in the populations of sheep and wolves
    """
    model = WolfSheep(**model_kwargs)
    step = -1
    for step in range(timeout):
        model.step()
        wolf_count = model.schedule.get_breed_count(Wolf)
        sheep_count = model.schedule.get_breed_count(Sheep)
        if min(wolf_count, sheep_count) == 0 or max(wolf_count, sheep_count) > 400:
            break
    df = model.datacollector.get_model_vars_dataframe()
    std = 0
    if step > 0:
        std = df["Wolves"].std(ddof=1) + df["Sheep"].std(ddof=1)
    return step + 1 + std


def objective(trial: optuna.Trial, timeout=100_000) -> float:
    params = dict(
        height=20,
        width=20,
        initial_sheep=trial.suggest_int("initial_sheep", 0, 400),
        initial_wolves=trial.suggest_int("initial_wolves", 0, 400),
        sheep_reproduce=trial.suggest_float("sheep_reproduce", 0, 1),
        wolf_reproduce=trial.suggest_float("wolf_reproduce", 0, 1),
        wolf_gain_from_food=trial.suggest_int("wolf_gain_from_food", 1, 50),
        grass=trial.suggest_categorical("grass", [False, True]),
        grass_regrowth_time=trial.suggest_int("grass_regrowth_time", 1, 50),
        sheep_gain_from_food=trial.suggest_int("sheep_gain_from_food", 1, 50),
        moore=trial.suggest_categorical("moore", [False, True]),
    )
    times = []
    for _ in range(3):
        times.append(run_model_until_collapse(timeout=timeout, **params))
    return sum(times) / len(times)


def main():
    initial_params = dict(
        height=20,
        width=20,
        initial_sheep=54,
        initial_wolves=22,
        sheep_reproduce=0.1,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=True,
        grass_regrowth_time=15,
        sheep_gain_from_food=4,
        moore=True,
    )

    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.TPESampler(multivariate=True),
        pruner=optuna.pruners.HyperbandPruner(),
    )
    study.enqueue_trial(initial_params)
    study.optimize(objective, n_trials=200)

    print(study.best_params)


if __name__ == "__main__":
    main()
