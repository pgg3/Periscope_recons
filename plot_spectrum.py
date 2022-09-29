import pandas as pd
from matplotlib import pyplot as plt
from plot_utils import read_data

DATA_PATH = "DATA"
DATA_LABEL = "1234"

if __name__ == "__main__":

    data, time, none_data, none_time = read_data(DATA_LABEL, DATA_PATH)

    plt.specgram(data, Fs=30, NFFT=8, noverlap=4, mode="magnitude", scale="dB")
    plt.title("Data")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    plt.show()

    plt.specgram(none_data, Fs=30, NFFT=8, noverlap=4, mode="magnitude", scale="dB")
    plt.title("None")
    plt.ylabel("Frequency")
    plt.xlabel("Time(s)")
    plt.show()