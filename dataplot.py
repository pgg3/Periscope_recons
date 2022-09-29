from plot_utils import read_data
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = "./data"
DATA_LABEL = "1234"


if __name__ == "__main__":

    data, time, none_data, none_time = read_data(DATA_LABEL, DATA_PATH)

    plt.plot(time, data, label=DATA_LABEL)
    plt.plot(none_time, none_data, label="none")
    plt.legend()
    plt.show()
