import os
import pandas as pd
import tikzplotlib
from matplotlib import pyplot as plt
from utils import read_data

DATA_PATH = "./data"
DATA_LABEL = "1234"

if __name__ == "__main__":
    if not os.path.exists("./figures/specgram"):
        os.mkdir("./figures/specgram")
    CMAP = "jet"

    data = read_data(DATA_LABEL, DATA_PATH)

    plt.figure(figsize=(10, 4))
    plt.specgram(data[:, 1], Fs=30, NFFT=32, noverlap=16, mode="magnitude", scale="dB", cmap=CMAP)
    plt.title("Data")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    # plt.colorbar()
    plt.tight_layout()
    tikzplotlib.save("test.tex")
    # plt.savefig("./figures/specgram/{}.svg".format(DATA_LABEL))

    plt.show()

    # none_data = read_data("none-1", DATA_PATH)
    # plt.specgram(none_data[:, 1], Fs=25, NFFT=32, noverlap=20, mode="magnitude", scale="dB", cmap=CMAP)
    # plt.title("None")
    # plt.ylabel("Frequency")
    # plt.xlabel("Time(s)")
    # plt.show()