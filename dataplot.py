from plot_utils import read_data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_PATH = "./data"
# NON_DATA = ["none", "none-1"]
NON_DATA = []
DATA_LABELS = [

    "1234",
    # "1234-1",
    # "1234-2",
    # "2345",
    # "2345-1",
    # "2345-2",
]

DATA_RANGE = np.arange(0, 1500)
# DATA_RANGE = np.arange(20, 200)


if __name__ == "__main__":
    # plt.ylim(2, 4)
    for no_data_lab in NON_DATA:
        none_data = read_data(no_data_lab, DATA_PATH)
        plt.plot(none_data[DATA_RANGE, 0], none_data[DATA_RANGE, 1], label=no_data_lab, alpha=0.3)

    for each_lab in DATA_LABELS:
        data = read_data(each_lab, DATA_PATH)
        plt.plot(data[DATA_RANGE, 0], data[DATA_RANGE, 1], label=each_lab)

    plt.legend()
    plt.show()
