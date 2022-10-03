import os
import json
import numpy as np
import cvxpy as cp
from utils import v_to_z
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
DIST_PATH = "./dist_data"
from plot_utils import read_data

VOLT_THRD = 0.2
ZMIN = 0.06
ALL_MAX = -1


if __name__ == '__main__':
    if not os.path.exists("./figures"):
        os.mkdir("./figures")

    v = np.arange(0.1, 3, 0.1)
    v = v[:, np.newaxis]
    z = v_to_z(v)
    plt.figure(figsize=(10, 5))
    plt.title("V to Z(example)")
    plt.xlabel("Voltage(V)")
    plt.ylabel("Distance(cm)")
    plt.plot(v, z)
    plt.show()

    file_list = os.listdir(DIST_PATH)
    dist_value_list = []
    volt_value_list = []
    for each_file in file_list:
        each_data = read_data(each_file[:-4], DIST_PATH)
        dist_value_list.append(each_file[:-4])
        each_data[:, 1] = -each_data[:, 1]
        enve_data = find_peaks(each_data[:, 1], distance=4)[0]
        enve_data = each_data[enve_data, :]

        peaks_data = find_peaks(enve_data[:, 1], distance=10)[0]
        peaks_data = enve_data[peaks_data, :]

        diff_peaks_data = np.diff(peaks_data[:, 1])
        diff_peaks_data = diff_peaks_data[:, np.newaxis]
        diff_peaks_data = np.concatenate((peaks_data[1:, :1], diff_peaks_data), axis=1)
        volt_value = np.where(diff_peaks_data[:, 1] > VOLT_THRD)[0][0]
        volt_value = diff_peaks_data[volt_value, 1]
        volt_value_list.append(volt_value)


        if each_file[:-4] == "0CM":
            ALL_MAX = np.max(diff_peaks_data[:, 1])

    dist_value_list = [float(dist[:-2]) + ZMIN for dist in dist_value_list]
    dist_value_list = np.array(dist_value_list)
    volt_value_list = np.array(volt_value_list)

    gamma1 = cp.Variable()
    gamma1.value = 0.33
    gamma2 = cp.Variable()
    gamma2.value = 3.35
    norm_volt= volt_value_list / ALL_MAX
    term1 = 1 - norm_volt * 0.6
    term1 = 2.0 * gamma1 / term1
    term2 = term1 - 4 + gamma2
    proption = ZMIN / dist_value_list
    error = cp.sum(cp.abs(proption - term2))
    prob = cp.Problem(cp.Minimize(error), [term2 >= 0, 2*gamma1-4 + gamma2 >= 0])
    prob.solve(warm_start=True)
    print("gamma1: ", gamma1.value)
    print("gamma2: ", gamma2.value)

    v = np.arange(0.1, 3, 0.05)
    v = v[:, np.newaxis]
    z = v_to_z(v, gamma1=gamma1.value, gamma2=gamma2.value, max_value=ALL_MAX)
    plt.figure(figsize=(8, 5))
    plt.title("V to Z(calibrated)")
    plt.xlabel("Voltage(V)")
    plt.ylabel("Distance(cm)")
    plt.ylim(0, 6)
    plt.xlim(0, 3)
    plt.plot(v, z, label="Analytic result")
    plt.scatter(volt_value_list, dist_value_list, marker="x", color="red", label="Mesurement result")
    plt.legend()
    plt.savefig("./figures/calibrated.svg")
    plt.show()


    if not os.path.exists("./res"):
        os.mkdir("./res")
    para = dict()
    para["gamma1"] = gamma1.value.tolist()
    para["gamma2"] = gamma2.value.tolist()
    para["max_value"] = ALL_MAX

    open_file = open("./res/para.json", "w")
    json.dump(para, open_file)
    open_file.close()

