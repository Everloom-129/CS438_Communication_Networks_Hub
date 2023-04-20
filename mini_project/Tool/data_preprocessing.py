import pandas as pd
import numpy as np
import sys

def remove_outliers(data, column, threshold=2):
    mean = np.mean(data[column])
    std_deviation = np.std(data[column])
    filtered_data = data[(mean - threshold * std_deviation <= data[column]) & (data[column] <= mean + threshold * std_deviation)]
    return filtered_data

def main():
    if len(sys.argv) > 2:
        data_file = sys.argv[1]
        network_stats_file = sys.argv[2]
    else:
        network_stats_file = "preprocessed_data/network_stats.csv"
        print(" Read the collected data CSV file")
        data_file = "raw_data/raw_data.csv"
    data = pd.read_csv(data_file)

    data = data.drop_duplicates()
    data = data.dropna()
    data = remove_outliers(data, 'Signal Strength', threshold=2)

    # Calculate the average signal strength for each BSSID and the number of unique BSSIDs for each SSID
    bssid_stats = data.groupby(['SSID', 'BSSID'])['Signal Strength'].agg(['mean', 'count']).reset_index()
    
    # Compare the average signal strength and number of unique BSSIDs between the two SSIDs
    ssid_comparison = bssid_stats.groupby('SSID').agg({'BSSID': 'count', 'mean': 'mean'})

    # Save the BSSID statistics to a new CSV file
    bssid_stats_file = network_stats_file
    bssid_stats.to_csv(bssid_stats_file, index=False)
    print(f"BSSID statistics saved to {bssid_stats_file}")

    # Save the SSID comparison to a new CSV file
    ssid_comparison_file = "ssid_comparison.csv"
    ssid_comparison.to_csv(ssid_comparison_file, index=True)
    print(f"SSID comparison saved to {ssid_comparison_file}")

if __name__ == "__main__":
    main()
