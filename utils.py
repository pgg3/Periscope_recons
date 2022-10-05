import os
import tikzplotlib

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

# CAND_COS = [0, 0.7526, 0.4961, 0.3560, 1, 0.9162]
# CAND_SIN = [1, 0.6585, 0.8682, 0.9345, 0, 0.4581]
L_X = [0, 1, 2]
L_Y = [0, 1, 2, 3]
V_P = 1.32
X_STEP = 1.6
Y_STEP = 1.4
def calc_dist_mat():
    L_X_len = len(L_X)
    L_Y_len = len(L_Y)
    dist_mat = np.zeros((L_Y_len, L_X_len))
    for i_x in range(L_X_len):
        for i_y in range(L_Y_len):
            dist_mat[i_y, i_x] = np.sqrt((L_X[i_x]*X_STEP)**2 + (L_Y[i_y]*Y_STEP)**2)
    return dist_mat


def v_to_z(v, gamma1=0.33, gamma2=3.35, max_value=None, zmin=0.06):
    if max_value is None:
        max_value = np.max(v, axis=0)
    norm_v = v / max_value
    term1 = 1 - norm_v * 0.6
    term1 = 2 * gamma1 / term1
    term2 = term1 - 4 + gamma2
    z = zmin / term2
    return z


def read_data(data_label, data_path):
    data_file = "{}.txt".format(data_label)
    full_data_name = data_path + "/" + data_file
    data = pd.read_csv(full_data_name, header=None)
    data_np = data.values
    data_np = data_np.astype(float)
    data_np[:, 0] = data_np[:, 0] / 1000.0
    data_np[:, 1] = data_np[:, 1] * (5.0 / 1023.0)

    return data_np


def lift_data(reverse_data, num_peaks=4):
    low_enve_idx = find_peaks(-reverse_data[:, 1])[0]
    low_enve = reverse_data[low_enve_idx, :]
    high_enve_idx = find_peaks(reverse_data[:, 1])[0]
    high_enve = reverse_data[high_enve_idx, :]

    low_enve_min_peaks_idx = find_peaks(-low_enve[:, 1], distance=5)[0]
    low_enve_min_peaks = low_enve[low_enve_min_peaks_idx, :]
    high_enve_max_peaks_idx = find_peaks(high_enve[:, 1], distance=5)[0]
    high_enve_max_peaks = high_enve[high_enve_max_peaks_idx, :]

    high_peaks_idx = np.argsort(high_enve_max_peaks[:, 1])[-num_peaks:]
    high_peaks_idx = high_enve_max_peaks_idx[high_peaks_idx]
    real_high_peaks_idx = high_enve_idx[high_peaks_idx]
    real_high_peaks_idx = np.sort(real_high_peaks_idx)
    # min_data = np.min(reverse_data[:real_high_peaks_idx[-1], 1])
    # reverse_data[:, 1] = reverse_data[:, 1] - min_data
    reverse_data -= np.min(high_enve[:, 1])
    reverse_data[reverse_data < 0] = 0
    # plt.figure(figsize=(10, 5))
    # plt.title("Lift Data")
    # plt.xlabel("Time(s)")
    # plt.ylabel("Volt(V)")
    # plt.plot(reverse_data[:, 0], reverse_data[:, 1], label="Reverse Data")
    # plt.plot(low_enve[:, 0], low_enve[:, 1], label="Low Envelope")
    # plt.plot(high_enve[:, 0], high_enve[:, 1], label="High Envelope")
    # plt.plot(low_enve_min_peaks[:, 0], low_enve_min_peaks[:, 1], "x", label="Low Peaks")
    # plt.plot(high_enve_max_peaks[:, 0], high_enve_max_peaks[:, 1], "x", label="High Peaks")
    # plt.legend()
    # plt.show()
    # a = 1

    # four_low_enve_max_peaks = np.argsort(high_enve_max_peaks[:, 1])[-num_peaks:]
    # four_low_enve_max_peaks = high_enve_max_peaks_idx[four_low_enve_max_peaks]
    # four_low_enve_max_peaks = low_enve_idx[four_low_enve_max_peaks]
    # four_low_enve_max_peaks_idx = np.sort(four_low_enve_max_peaks)
    # for high_peak_idx in range(len(four_low_enve_max_peaks_idx)):
    #     high_peak_data_idx = four_low_enve_max_peaks_idx[high_peak_idx]
    #     if high_peak_idx == 0:
    #         patch_reverse = reverse_data[:high_peak_data_idx, :]
    #         min_data = np.min(patch_reverse[:, 1])
    #         reverse_data[:high_peak_data_idx, 1] -= min_data
    #     else:
    #         patch_reverse = reverse_data[four_low_enve_max_peaks_idx[high_peak_idx - 1]:high_peak_data_idx,
    #                         :]
    #         min_data = np.min(patch_reverse[:, 1])
    #         if high_peak_idx == len(four_low_enve_max_peaks_idx) - 1:
    #             reverse_data[four_low_enve_max_peaks_idx[high_peak_idx - 1]:, 1] -= min_data
    #         else:
    #             reverse_data[four_low_enve_max_peaks_idx[high_peak_idx - 1]:high_peak_data_idx, 1] -= min_data
    # reverse_zero_data_less = np.where(reverse_data[:, 1] < 0)
    # reverse_data[reverse_zero_data_less, 1] = 0
    return reverse_data


def plot_all_file(dist_path=None):
    if dist_path is None:
        raise ValueError("Please specify the path of the files")
    file_list = os.listdir(dist_path)
    all_data = []
    data_labels = []
    for each_file in file_list:
        data_labels.append(each_file[:-4])
        each_data = read_data(each_file[:-4], dist_path)
        all_data.append(each_data)
    plt.figure(figsize=(10, 5))
    plt.title("All Data")
    plt.xlabel("Time(s)")
    plt.ylabel("Volt(V)")
    for i in range(len(all_data)):
        plt.plot(all_data[i][:, 0], all_data[i][:, 1], label=data_labels[i])
    plt.legend()
    plt.show()


def extract_enve_and_seg(data, num_peaks=4):

    high_enve_idx = find_peaks(data[:, 1], distance=1)[0]
    high_enve = data[high_enve_idx, :]
    high_peaks_idx = find_peaks(high_enve[:, 1], distance=5)[0]
    high_peaks = high_enve[high_peaks_idx, :]
    high_peaks_need = np.argsort(high_peaks[:, 1])[-num_peaks:]
    real_high_peaks_idx = high_peaks_idx[high_peaks_need]
    real_high_peaks_idx = np.sort(real_high_peaks_idx)
    seg_data = high_enve[real_high_peaks_idx[0]-1:real_high_peaks_idx[-1]+2, :]

    return seg_data


def return_theta_confidence(key_pair):
    one_mat = np.ones((key_pair.shape[0], 1))

    z1 = np.polyfit(key_pair[:, 0], key_pair[:, 1], 5)
    p1 = np.poly1d(z1)
    y_val = p1(key_pair[:, 0])
    time_last = key_pair[-1, 0]
    prolong_time = np.arange(0, 1.2*time_last, 0.01)
    prolong_y = p1(prolong_time)

    last_idx = int(key_pair[-1, 0] / 0.01)
    touch_time_idx = np.argmin(prolong_y[last_idx:])
    touch_time = prolong_time[touch_time_idx+last_idx]

    # plt.figure(figsize=(10, 5))
    # plt.title("Distance")
    # plt.xlabel("Time(s)")
    # plt.ylabel("$z(t)$(cm)")
    # plt.scatter(key_pair[:, 0], key_pair[:, 1], label="Raw Data", marker="x", color="red")
    # plt.plot(prolong_time, prolong_y, label="Prolonged Curve")
    # plt.plot(touch_time, prolong_y[touch_time_idx+last_idx], "^", label="Touch Time")
    # plt.legend()
    # tikzplotlib.save("distance.tex")
    # plt.show()

    move_dist = touch_time * V_P

    dist_mat = calc_dist_mat()
    dist_error = np.abs(dist_mat - move_dist)
    sum_error = np.sum(dist_error)

    confidence_mat = 1 - dist_error / sum_error
    move_idx = np.argmax(confidence_mat)
    move_x, move_y = np.unravel_index(move_idx, (4, 3))

    # fig, ax = plt.subplots()
    # im = ax.imshow(confidence_mat)
    # ax.set_xticks(np.arange(confidence_mat.shape[1]))
    # ax.set_yticks(np.arange(confidence_mat.shape[0]))
    # for i in range(confidence_mat.shape[0]):
    #     for j in range(confidence_mat.shape[1]):
    #         text = ax.text(j, i, "{:.3f}".format(confidence_mat[i, j]),
    #                        ha="center", va="center", color="w")
    # ax.set_title("Confidence Matrix")
    # fig.tight_layout()
    # tikzplotlib.save("confidence.tex")
    # plt.show()
    return move_x, move_y


