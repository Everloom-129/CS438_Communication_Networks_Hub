import pandas as pd
import numpy as np
import sys

# we turn off one of the panda warning to avoid annoying buggy words
# the index method we take don't harm to the data integrity 
# pd.options.mode.chained_assignment = None


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
    return filtered_df.drop_duplicates()



def main():
    if len(sys.argv) > 2:
        data_file = sys.argv[1]
        network_stats_file = sys.argv[2]
    else:
        data_file = "raw_data/illinois_net_raw_data.csv"
    data = pd.read_csv(data_file)

    data = data.dropna()
    # data = remove_outliers(data, 'Signal Strength', threshold=2)
    mean_data = keep_current_mean(data)
    
    BSSID_data = pd.read_csv("AP_info/AP_info.csv")["BSSID MAC"]
    for bssid in BSSID_data:
        bssid_data = single_ap(data, bssid)
        bssid_filename = bssid.replace(":", "_")
        bssid_data.to_csv(f"raw_data/{bssid_filename}.csv", index = False)

    try:
        mean_data.to_csv("raw_data/preprocessed_mean.csv", index=False)
    except:
        print("failed to save to file")

    
if __name__ == "__main__":
    main()
