import pandas as pd
import numpy as np
import sys

def remove_outliers(data, column, threshold=2):
    mean = np.mean(data[column])
    std_deviation = np.std(data[column])
    filtered_data = data[(mean - threshold * std_deviation <= data[column]) & (data[column] <= mean + threshold * std_deviation)]
    return filtered_data

def keep_current_mean(data):
    print("keep current")
    filtered_df = data[data["current BSSID"] == "1"]
    filtered_df['Signal Strength'] = pd.to_numeric(filtered_df['Signal Strength'])
    mean_signal = filtered_df.groupby(['x', 'y'], as_index=False)['Signal Strength'].transform('mean')
    filtered_df['Signal Strength'] = mean_signal
    return filtered_df.drop_duplicates()

def single_ap(data, bssid):
    print("single")
    filtered_df = data[data["BSSID"] == bssid]
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

    # # Calculate the average signal strength for each BSSID and the number of unique BSSIDs for each SSID
    # bssid_stats = data.groupby(['SSID', 'BSSID'])['Signal Strength'].agg(['mean', 'count']).reset_index()
    
    # # Compare the average signal strength and number of unique BSSIDs between the two SSIDs
    # ssid_comparison = bssid_stats.groupby('SSID').agg({'BSSID': 'count', 'mean': 'mean'})

    # # Save the BSSID statistics to a new CSV file
    # bssid_stats_file = network_stats_file
    # bssid_stats.to_csv(bssid_stats_file, index=False)
    # print(f"BSSID statistics saved to {bssid_stats_file}")

    # # Save the SSID comparison to a new CSV file
    # ssid_comparison_file = "ssid_comparison.csv"
    # ssid_comparison.to_csv(ssid_comparison_file, index=True)
    # print(f"SSID comparison saved to {ssid_comparison_file}")

if __name__ == "__main__":
    main()
