from prey_predator.model import WolfSheep
import matplotlib.pyplot as plt
from tqdm import tqdm


def run_model(**model_kwargs):
    model = WolfSheep(**model_kwargs)
    pbar = tqdm(range(100_000), position=1, leave=False, desc='Running model', unit='steps')
    for _ in pbar:
        model.step()
    df = model.datacollector.get_model_vars_dataframe()
    return df.reset_index(names="step")


def main():
    params = dict(
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

    df = run_model(**params)
    plt.plot(df['Sheep'], label='Sheep', c='tab:blue')
    plt.plot(df['Wolves'], label='Wolves', c='tab:orange')

    plt.grid()
    plt.legend()
    plt.show()
    


if __name__ == "__main__":
    main()
