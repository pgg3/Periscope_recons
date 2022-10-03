import os
import numpy as np
from scipy.signal import find_peaks
from plot_utils import read_data
import matplotlib.pyplot as plt

DATA_PATH = "./raw_data"
DATA_LEN = 2000
OMIT_LEN = 800
STAB_LEN = 1200
DATA_RANGE = np.arange(0, DATA_LEN)
NOR_RANGE = np.arange(OMIT_LEN, STAB_LEN)


if __name__ == '__main__':
    file_list = os.listdir(DATA_PATH)

    for each_file in file_list:
        each_data = read_data(each_file[:-4], DATA_PATH)
        each_data = each_data[DATA_RANGE, :]
        each_data[:, 1] = -each_data[:, 1]

        # nor_data = each_data[NOR_RANGE, :]
        # print(np.mean(nor_data[:, 1]))

        enve_data = find_peaks(each_data[:, 1])[0]
        enve_data = each_data[enve_data, :]

        if not os.path.exists("./figures/envelop"):
            os.mkdir("./figures/envelop")

        plt.figure(figsize=(10, 5))
        plt.title(each_file[:-4])
        plt.plot(each_data[:, 0], each_data[:, 1], label=each_file[:-4])
        plt.plot(enve_data[:, 0], enve_data[:, 1], label=each_file[:-4]+"_enve")
        plt.legend()
        plt.savefig("./figures/envelop/{}.svg".format(each_file[:-4]))
        plt.show()

        nor_data = each_data[NOR_RANGE, :]
        print(np.mean(nor_data[:, 1]))


        # peaks_env = find_peaks(enve_data[:, 1])[0]
        # # peaks_env = find_peaks(-envelop[:, 1], height=-2.9)[0]
        # plt.title(each_file[:-4])
        # plt.plot(enve_data[:, 0], enve_data[:, 1], label=each_file[:-4])
        # plt.scatter(enve_data[peaks_env, 0], enve_data[peaks_env, 1], marker="x", label=each_file[:-4] + "_peaks", color="red")
        # plt.savefig("./figures/envelop/{}_peaks.svg".format(each_file[:-4]))
        # plt.show()






