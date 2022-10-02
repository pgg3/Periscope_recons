import pandas as pd


def read_data(data_label, data_path):
    data_file = "{}.txt".format(data_label)
    full_data_name = data_path + "/" + data_file
    data = pd.read_csv(full_data_name, header=None)
    data_np = data.values
    data_np = data_np.astype(float)
    data_np[:, 0] = data_np[:, 0] / 1000.0
    data_np[:, 1] = data_np[:, 1] * (5.0 / 1023.0)

    return data_np

def normalize_data(data):
    data[:, 1] = data[:, 1] - np.min(data[:, 1])
    data[:, 1] = data[:, 1] / np.max(data[:, 1])
    return data
