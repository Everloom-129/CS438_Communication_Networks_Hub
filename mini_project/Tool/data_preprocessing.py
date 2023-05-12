import pandas as pd
import numpy as np
import sys


# Global path variable
default_info_path = "AP_info/AP_info_" + "L3.csv"
raw_data_path = "raw_data/" + "illinois" + "_raw_data_" + "L3.csv" # eduroam or illinois
preprocessed_path = "preprocessed_data/preprocessed_mean.csv"

def remove_outliers(data, column, threshold=2):
    mean = np.mean(data[column])
    std_deviation = np.std(data[column])
    filtered_data = data[(mean - threshold * std_deviation <= data[column]) & (data[column] <= mean + threshold * std_deviation)]
    return filtered_data

def keep_current_mean(data):
    print("keep current")
    filtered_df = data[data["current BSSID"] == "1"].copy()
    if filtered_df.empty:
        return filtered_df
    filtered_df['Signal Strength'] = pd.to_numeric(filtered_df['Signal Strength'])
    mean_signal = filtered_df.groupby(['x', 'y'], as_index=False)['Signal Strength'].transform('mean')
    filtered_df['Signal Strength'] = mean_signal
    return filtered_df.drop_duplicates()

def single_ap(data, bssid):
    # print("single")
    filtered_df = data[data["BSSID"] == bssid].copy()
    if filtered_df.empty:
        return filtered_df
    filtered_df['Signal Strength'] = pd.to_numeric(filtered_df['Signal Strength'])
    mean_signal = filtered_df.groupby(['x', 'y'], as_index=False)['Signal Strength'].transform('mean')
    filtered_df['Signal Strength'] = mean_signal

    bssid_filename = bssid.replace(":", "-")
    bssid_data = filtered_df.drop_duplicates()
    bssid_data.to_csv(f"preprocessed_data/{bssid_filename}.csv", index = False)
    return



def main():
    if len(sys.argv) > 2:
        data_file = sys.argv[1]
        AP_info_path = sys.argv[2]
    else:
        AP_info_path = default_info_path
        data_file = raw_data_path
    data = pd.read_csv(data_file)

    data = data.dropna()
    # data = remove_outliers(data, 'Signal Strength', threshold=2)
    mean_data = keep_current_mean(data)
    
    BSSID_data = pd.read_csv(AP_info_path)["BSSID-MAC"]
    for bssid in BSSID_data:
        single_ap(data, bssid)

    try:
        mean_data.to_csv(preprocessed_path, index=False)
    except:
        print("failed to save to file")

    
if __name__ == "__main__":
    main()
