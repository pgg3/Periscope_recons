import os

import numpy as np
import cvxpy as cp

from utils import read_data, lift_data, v_to_z
from matplotlib import pyplot as plt
from scipy.signal import find_peaks


def calculate_gamma(dist_path=None, ZMIN=0.06, PLOT=True):
    if dist_path is None:
        raise ValueError("Please specify the path of distance file")
    file_list = os.listdir(dist_path)
    all_data = []
    data_labels = []
    max_volt = -1
    for each_file in file_list:
        if each_file[:-4] == "0CM":
            zero_data = read_data(each_file[:-4], dist_path)
            reverse_zero_data = zero_data
            reverse_zero_data[:, 1] = -reverse_zero_data[:, 1]
            reverse_zero_data = lift_data(reverse_zero_data, num_peaks=4)
            high_enve_idx = find_peaks(reverse_zero_data[:, 1], distance=1)[0]
            high_enve = reverse_zero_data[high_enve_idx, :]
            high_enve_max_peaks_idx = find_peaks(high_enve[:, 1], distance=10)[0]
            high_enve_max_peaks = high_enve[high_enve_max_peaks_idx, :]
            four_max_volt = np.sort(high_enve_max_peaks[:, 1])[-4:]
            max_volt = np.max(four_max_volt)
        else:
            data_labels.append(each_file[:-4])
            each_data = read_data(each_file[:-4], dist_path)
            all_data.append(each_data)

    data_max_volt_list = []
    data_idx = 0
    for each_data in all_data:
        reverse_data = np.copy(each_data)
        reverse_data[:, 1] = -reverse_data[:, 1]
        reverse_data = reverse_data[:int(0.6* len(reverse_data)), :]
        reverse_lift_data = lift_data(reverse_data, num_peaks=1)
        max_volt_idx = np.argmax(reverse_lift_data[:, 1])
        high_enve_idx = find_peaks(reverse_lift_data[300:max_volt_idx, 1], distance=1)[0]
        high_enve = reverse_lift_data[high_enve_idx+300, :]
        base_volt = np.min(high_enve)
        data_max_volt = reverse_lift_data[max_volt_idx, 1] - base_volt
        data_max_volt_list.append(data_max_volt)
        data_idx += 1

    # data_max_volt_list.append(max_volt)
    # data_labels.append("0CM")
    data_max_volt_list = np.array(data_max_volt_list)
    data_labels = [float(dist[:-2]) + ZMIN for dist in data_labels]
    data_labels = np.array(data_labels)

    gamma1 = cp.Variable()
    gamma1.value = 0.1386
    gamma2 = cp.Variable()
    gamma2.value = 3.7226
    norm_volt = data_max_volt_list / max_volt
    term1 = 1 - norm_volt * 0.6
    term1 = 2.0 * gamma1 / term1
    term2 = term1 - 4 + gamma2
    proption = ZMIN / data_labels
    error = cp.sum(cp.abs(proption - term2))
    prob = cp.Problem(cp.Minimize(error), [term2 >= 0, 2 * gamma1 - 4 + gamma2 >= 0])
    prob.solve(warm_start=True)
    # print("gamma1: ", gamma1.value)
    # print("gamma2: ", gamma2.value)

    if PLOT:
        v = np.arange(0.1, 4, 0.05)
        v = v[:, np.newaxis]
        z = v_to_z(v, gamma1=gamma1.value, gamma2=gamma2.value, max_value=max_volt)
        plt.figure(figsize=(8, 5))
        plt.title("V to Z(calibrated)")
        plt.xlabel("Voltage(V)")
        plt.ylabel("Distance(cm)")
        plt.ylim(0, 6)
        plt.xlim(0, 4)
        plt.plot(v, z, label="Analytic result")
        plt.scatter(data_max_volt_list, data_labels, marker="x", color="red", label="Mesurement result")
        plt.scatter(max_volt, 0.06, marker="x", color="red")
        plt.legend()
        plt.savefig("./figures/calibrated.svg")
        plt.show()

    return gamma1.value, gamma2.value
