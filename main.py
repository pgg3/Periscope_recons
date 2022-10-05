import os
import json
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

from calculate_gamma import calculate_gamma
from utils import plot_all_file, read_data, lift_data, extract_enve_and_seg, v_to_z, return_theta_confidence


# Path of distance file:
DIST_PATH = "./dist_data"
RAW_PATH = "./raw_data"

PLOT_DATA = True

if __name__ == '__main__':
    # Calibrate the value of gamma1, gamma2
    if PLOT_DATA:
        plot_all_file(DIST_PATH)
    gamma1, gamma2 = calculate_gamma(dist_path=DIST_PATH, PLOT=PLOT_DATA)
    para = dict()
    para["gamma1"] = gamma1.tolist()
    para["gamma2"] = gamma2.tolist()
    open_file = open("./res/para.json", "w")
    json.dump(para, open_file)
    open_file.close()

    # Process the raw data
    if PLOT_DATA:
        plot_all_file(RAW_PATH)
    file_path = os.listdir(RAW_PATH)
    all_key_pairs = []
    move_length = []
    for each_file in file_path:
        key_pairs = []
        each_move_length = []
        each_data = read_data(each_file[:-4], RAW_PATH)
        reverse_data = np.copy(each_data)
        reverse_data[:, 1] = -reverse_data[:, 1]
        lifted_data = lift_data(reverse_data, num_peaks=4)
        enve_seg = extract_enve_and_seg(lifted_data, num_peaks=4)
        data_enve = enve_seg[:, 1:]
        z_trace = v_to_z(data_enve, gamma1, gamma2)
        z = np.concatenate([enve_seg[:,:1], z_trace], axis=1)
        z_peaks = find_peaks(-z[:, 1], distance=5)[0]
        for each_peak in range(len(z_peaks)-1):
            this_peak_idx = z_peaks[each_peak]
            next_peak_idx = z_peaks[each_peak + 1]
            this_key_pair = np.copy(z[this_peak_idx:next_peak_idx+1, :])
            this_key_pair[:, 0] = this_key_pair[:, 0] - this_key_pair[0, 0]
            key_pairs.append(this_key_pair)
            move_x, move_y = return_theta_confidence(this_key_pair)
            each_move_length.append([move_x, move_y])

        all_key_pairs.append(key_pairs)
        move_length.append(each_move_length)









