import os
import numpy as np
from scipy.signal import find_peaks
from plot_utils import read_data
import matplotlib.pyplot as plt

DATA_PATH = "./raw_data"
DATA_RANGE = np.arange(0, 2000)

if __name__ == '__main__':
    file_list = os.listdir(DATA_PATH)

    for each_file in file_list:
        each_data = read_data(each_file[:-4], DATA_PATH)
        each_data = each_data[DATA_RANGE, :]

        local_mins = find_peaks(-each_data[:, 1])[0]

        if not os.path.exists("./figures/envelop"):
            os.mkdir("./figures/envelop")

        plt.plot(each_data[:, 0], each_data[:, 1], label=each_file[:-4])
        plt.plot(each_data[local_mins, 0], each_data[local_mins, 1], label=each_file[:-4]+"_enve")
        plt.legend()
        plt.savefig("./figures/envelop/{}.svg".format(each_file[:-4]))
        plt.show()

        envelop = each_data[local_mins, :]
        peaks_env = np.argsort(-envelop[:, 1])[-4:]
        # peaks_env = find_peaks(-envelop[:, 1], height=-2.9)[0]
        plt.plot(envelop[:, 0], envelop[:, 1], label=each_file[:-4])
        plt.scatter(envelop[peaks_env, 0], envelop[peaks_env, 1], marker="x", label=each_file[:-4] + "_peaks", color="red")
        plt.savefig("./figures/envelop/{}_peaks.svg".format(each_file[:-4]))
        plt.show()
        # plt.scatter(envelop[peaks_env, 0], envelop[peaks_env, 1], "x", label=each_file[:-4]+"_peaks")
        # plt.legend()
        # plt.savefig("./figures/envelop/{}_peaks.svg".format(each_file[:-4]))
        # plt.show()




