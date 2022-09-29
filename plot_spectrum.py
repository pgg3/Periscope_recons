import pandas as pd
from matplotlib import pyplot as plt
from plot_utils import read_data

DATA_PATH = "./data/delay50"
DATA_LABEL = "1234"

if __name__ == "__main__":
    CMAP = "jet"

    data, none_data = read_data(DATA_LABEL, DATA_PATH)

    plt.specgram(data[:, 1], Fs=15, NFFT=16, noverlap=8, mode="magnitude", scale="dB", cmap=CMAP)
    plt.title("Data")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    plt.show()

    plt.specgram(none_data[:, 1], Fs=15, NFFT=16, noverlap=8, mode="magnitude", scale="dB", cmap=CMAP)
    plt.title("None")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    plt.show()