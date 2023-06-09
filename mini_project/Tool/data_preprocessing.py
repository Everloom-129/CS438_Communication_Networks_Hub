import pandas as pd
import numpy as np
import sys
import os


# Global path variable
default_info_path = "AP_info/AP_info_" + "L1.csv"
raw_data_path = "raw_data/" + "eduroam" + "_raw_data_" + "L1.csv" # eduroam or illinois
preprocessed_path = "preprocessed_data/preprocessed_mean.csv"

def keep_current_mean(data):
    """
    Filters a DataFrame to keep only the connected wifi signal, then calculates the mean signal strength for each (x, y) pair.

    @param data: The pandas DataFrame to filter and calculate mean signal strength.

    @return: connected wifi
    """
    print("Recording the current connection")
    filtered_df = data[data["current BSSID"] == "1"].copy()
    if filtered_df.empty:
        return filtered_df
    filtered_df['Signal Strength'] = pd.to_numeric(filtered_df['Signal Strength'])
    mean_signal = filtered_df.groupby(['x', 'y'], as_index=False)['Signal Strength'].transform('mean')
    filtered_df['Signal Strength'] = mean_signal
    return filtered_df.drop_duplicates()

def single_ap(data, bssid):
    """
    Filters a DataFrame to keep only the rows where the 'BSSID' column matches the provided BSSID,
    then calculates the mean signal strength for each (x, y) pair. 
    The result is saved to a CSV file named after the BSSID.

    @param data: The pandas DataFrame to filter and calculate mean signal strength.
    @param bssid: The BSSID to filter by.

    @return: None
    """
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

    # Save the output image and text file
    output_folder = "preprocessed_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    data = data.dropna()
    print("start preprocessing data")
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
