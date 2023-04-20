import pandas as pd
import numpy as np
import sys

def remove_outliers(data, column, threshold=2):
    mean = np.mean(data[column])
    std_deviation = np.std(data[column])
    filtered_data = data[(mean - threshold * std_deviation <= data[column]) & (data[column] <= mean + threshold * std_deviation)]
    return filtered_data

def main():
    # Check if a file name was provided as a command line argument
    if len(sys.argv) > 2:
        data_file = sys.argv[1]
        network_stats_file = sys.argv[2]
    else:
        network_stats_file = "network_stats.csv"

        print(" Read the collected data CSV file")
        data_file = "raw_data.csv"
    data = pd.read_csv(data_file)

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Remove any rows with missing values
    data = data.dropna()

    # Remove outliers in 'Signal Strength' using a Z-score threshold of 2
    data = remove_outliers(data, 'Signal Strength', threshold=2)

    # Normalize the 'Signal Strength' column to a range of [0, 1]
    data['Signal Strength_normalized'] = (data['Signal Strength'] - data['Signal Strength'].min()) / (data['Signal Strength'].max() - data['Signal Strength'].min())

    # Filter the data to exclude 'eduroam' SSID
    data_filtered = data[data['SSID'] != 'eduroam']

    # Group the data by SSID and compute the average and standard deviation of the signal strength
    network_stats = data_filtered.groupby('SSID')['Signal Strength'].agg(['mean', 'std'])

    # Save the preprocessed data to a new CSV file
    preprocessed_data_file = "preprocessed_data.csv"
    data.to_csv(preprocessed_data_file, index=False)
    print(f"Preprocessed data saved to {preprocessed_data_file}")

    # Save the network statistics to a new CSV file
    network_stats.to_csv(network_stats_file, index=True)
    print(f"Network statistics saved to {network_stats_file}")

if __name__ == "__main__":
    main()
