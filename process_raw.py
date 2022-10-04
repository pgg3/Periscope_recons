import os
import json
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from utils import v_to_z, read_data

DATA_PATH = "./raw_data"
DATA_LEN = 1500
DATA_RANGE = np.arange(0, DATA_LEN)
CAND_COS = [0, 0.7526, 0.4961, 0.3560, 1, 0.9162]
CAND_SIN = [1, 0.6585, 0.8682, 0.9345, 0, 0.4581]


if __name__ == '__main__':
    file_open = open("./res/para.json", "r")
    PARA  = json.load(file_open)
    file_open.close()

    file_list = os.listdir(DATA_PATH)

    for each_file in file_list:
        each_data = read_data(each_file[:-4], DATA_PATH)
        each_data = each_data[DATA_RANGE, :]
        each_data[:, 1] = -each_data[:, 1]

        enve_data = find_peaks(each_data[:, 1], distance=1)[0]
        enve_data = each_data[enve_data, :]
        # plt.figure(figsize=(10, 5))
        # plt.title("Envelop of {}".format(each_file[:-4]))
        # plt.plot(each_data[:, 0], each_data[:, 1], label="raw data")
        # plt.plot(enve_data[:, 0], enve_data[:, 1], label="envelop")
        # # plt.plot(peaks_data[:, 0], peaks_data[:, 1], label="peaks")
        # plt.legend()
        # plt.show()

        if not os.path.exists("./figures/envelop"):
            os.mkdir("./figures/envelop")

        peaks_data_idx = find_peaks(enve_data[:, 1], distance=7)[0]
        peaks_data = enve_data[peaks_data_idx, :]

        four_max = np.argsort(peaks_data[:, 1])[-4:]
        four_max = peaks_data_idx[four_max]
        four_max = np.sort(four_max)
        #
        four_max_data = enve_data[four_max[0]-1:four_max[-1]+2, :]

        seg_max_peaks = find_peaks(four_max_data[:, 1], distance=3)[0]
        seg_min_peaks = find_peaks(-four_max_data[:, 1], distance=3)[0]
        seg_all_peaks = np.sort(np.concatenate((seg_max_peaks, seg_min_peaks)))
        plt.figure(figsize=(10, 5))
        plt.title("Envelop of {}".format(each_file[:-4]))
        # plt.plot(each_data[:, 0], each_data[:, 1], label="raw data")
        # plt.plot(enve_data[:, 0], enve_data[:, 1], label="envelop")
        # plt.scatter(peaks_data[:, 0], peaks_data[:, 1], marker="x", color="red", label="peaks")
        plt.plot(four_max_data[:, 0], four_max_data[:, 1], marker="x", color="green", label="four max")
        plt.scatter(four_max_data[seg_all_peaks, 0], four_max_data[seg_all_peaks, 1], marker="^", color="red", label="four max")
        plt.legend()
        plt.show()



        min_min_peak = np.argmin(four_max_data[seg_min_peaks, 1])
        four_max_data[:, 1] -= np.min(four_max_data[:, 1]) - 0.2

        calc_four = four_max_data[1:-1, :]
        z_four = v_to_z(calc_four[:, 1:], gamma1=PARA["gamma1"], gamma2=PARA["gamma2"])
        z_time = calc_four[:, :1] - calc_four[:1, :1]

        plt.figure(figsize=(10, 6))
        plt.plot(z_time, z_four,label=each_file[:-4])
        plt.xlabel("Time (s)")
        plt.ylabel("Z (cm)")
        plt.legend()
        plt.title("Z vs Time")
        plt.show()


















