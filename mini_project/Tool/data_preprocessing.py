import pandas as pd
import numpy as np

def remove_outliers(data, column, threshold=2):
    mean = np.mean(data[column])
    std_deviation = np.std(data[column])
    filtered_data = data[(mean - threshold * std_deviation <= data[column]) & (data[column] <= mean + threshold * std_deviation)]
    return filtered_data

def main():
    # Read the collected data CSV file
    data_file = "collected_data.csv"
    data = pd.read_csv(data_file)

    # Remove duplicate rows based on 'timestamp', 'x_coordinate', 'y_coordinate', 'bssid'
    data = data.drop_duplicates(subset=['timestamp', 'x_coordinate', 'y_coordinate', 'bssid'])

    # Remove any rows with missing values
    data = data.dropna()

    # Remove outliers in 'signal_strength' using a Z-score threshold of 2
    data = remove_outliers(data, 'signal_strength', threshold=2)

    # Normalize the 'signal_strength' column to a range of [0, 1]
    data['signal_strength_normalized'] = (data['signal_strength'] - data['signal_strength'].min()) / (data['signal_strength'].max() - data['signal_strength'].min())

    # Save the preprocessed data to a new CSV file
    preprocessed_data_file = "preprocessed_data.csv"
    data.to_csv(preprocessed_data_file, index=False)
    print(f"Preprocessed data saved to {preprocessed_data_file}")

if __name__ == "__main__":
    main()
