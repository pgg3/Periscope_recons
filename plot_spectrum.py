import os
import pandas as pd
from matplotlib import pyplot as plt
from utils import read_data

DATA_PATH = "./data"
DATA_LABEL = "2345"

if __name__ == "__main__":
    if not os.path.exists("./figures/specgram"):
        os.mkdir("./figures/specgram")
    CMAP = "jet"

    data = read_data(DATA_LABEL, DATA_PATH)

    plt.specgram(data[:, 1], Fs=60, NFFT=64, noverlap=32, mode="magnitude", scale="dB", cmap=CMAP)
    plt.title("Data")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    plt.savefig("./figures/specgram/{}.svg".format(DATA_LABEL))
    plt.show()

    # none_data = read_data("none-1", DATA_PATH)
    # plt.specgram(none_data[:, 1], Fs=25, NFFT=32, noverlap=20, mode="magnitude", scale="dB", cmap=CMAP)
    # plt.title("None")
    # plt.ylabel("Frequency")
    # plt.xlabel("Time(s)")
    # plt.show()