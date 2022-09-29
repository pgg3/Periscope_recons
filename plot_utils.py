import pandas as pd


def read_data(data_label, data_path):
    data_file = "{}-data.txt".format(data_label)
    full_data_name = data_path + "/" + data_file
    data = pd.read_csv(full_data_name, header=None)
    data_np = data.values
    data_np = data_np.reshape(data_np.shape[0], )
    data_np = data_np * (5.0 / 1023.0)

    time_file = "{}-time.txt".format(data_label)
    full_time_name = data_path + "/" + time_file
    time = pd.read_csv(full_time_name, header=None)
    time_np = time.values
    time_np = time_np.reshape(time_np.shape[0], )
    time_np = (time_np - time_np[0]) / 1000.0

    none_data_name = data_path + "/none-data.txt"
    none_data = pd.read_csv(none_data_name, header=None)
    none_data_np = none_data.values
    none_data_np = none_data_np.reshape(none_data_np.shape[0], )
    none_data_np = none_data_np * (5.0 / 1023.0)

    none_time_name = data_path + "/none-time.txt"
    none_time = pd.read_csv(none_time_name, header=None)
    none_time_np = none_time.values
    none_time_np = none_time_np.reshape(none_time_np.shape[0], )
    none_time_np = (none_time_np - none_time_np[0]) / 1000.0

    return data_np, time_np, none_data_np, none_time_np
