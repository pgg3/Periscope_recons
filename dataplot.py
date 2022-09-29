from plot_utils import read_data
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = "./data/delay50"
DATA_LABEL = "1234"


if __name__ == "__main__":

    data, none_data = read_data(DATA_LABEL, DATA_PATH)

    plt.plot(data[:, 0], data[:, 1], label=DATA_LABEL)
    plt.plot(none_data[:, 0], none_data[:, 1], label="none")
    plt.legend()
    plt.show()
