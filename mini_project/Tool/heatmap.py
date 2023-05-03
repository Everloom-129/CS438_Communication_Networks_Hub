import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

import seaborn as sns



def generate_heatmap(data, x_points, y_points):
    x = data['x_coordinate']
    y = data['y_coordinate']
    signal_strength = data['signal_strength_normalized']

    # Create a grid of points for the entire floor plan
    X, Y = np.meshgrid(x_points, y_points)

    # Interpolate the signal strength using Radial Basis Function (RBF)
    rbf = Rbf(x, y, signal_strength, function='multiquadric', smooth=1)
    Z = rbf(X, Y)

    return X, Y, Z

def main():
    print("generating the heatmap...")
    # todo: "test_coord.csv" for coordinates we want to test
    create_heatmap("raw_data//raw_data.csv", "floor_plan\Siebel-Floor-Plan-1.jpg", "heatmap\h1.png", "test_coord.csv")

    # # Read the preprocessed data CSV file
    # preprocessed_data_file = "preprocessed_data.csv"
    # data = pd.read_csv(preprocessed_data_file)

    # # Define the dimensions of the floor plan
    # floor_width = 100
    # floor_height = 100

    # # Define the resolution of the heatmap
    # resolution = 1

    # # Generate a grid of points for the entire floor plan
    # x_points = np.arange(0, floor_width, resolution)
    # y_points = np.arange(0, floor_height, resolution)

    # # Generate the heatmap
    # X, Y, Z = generate_heatmap(data, x_points, y_points)

    # # Save the heatmap as a numpy array
    # heatmap_file = "heatmap.npy"
    # np.save(heatmap_file, Z)
    # print(f"Heatmap saved to {heatmap_file}")

    # # Plot the heatmap
    # plt.imshow(Z, cmap='coolwarm', origin='lower', extent=[0, floor_width, 0, floor_height], aspect='auto')
    # plt.colorbar(label='Signal Strength')
    # plt.title('Wi-Fi Network Heatmap')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    # plt.show()


def create_heatmap(raw_data_path, floor_plan_path, heatmap_path, test_coord_path):
    # Load Wi-Fi data
    wifi_data = pd.read_csv(raw_data_path)
    test_coord = pd.read_csv(test_coord_path)
    
    # Calculate grid size based on the number of unique latitude and longitude values
    num_lat = len(wifi_data['Latitude'].unique())
    num_lon = len(wifi_data['Longitude'].unique())

    # Create an empty grid for the heatmap
    heatmap_data = np.zeros((num_lat, num_lon))


    # Fill the heatmap grid with signal strength data
    for index, row in wifi_data.iterrows():
        lat_index = np.where(wifi_data['Latitude'].unique() == row['Latitude'])[0][0]
        lon_index = np.where(wifi_data['Longitude'].unique() == row['Longitude'])[0][0]
        heatmap_data[lat_index, lon_index] = row['Signal Strength']

    # Set up the figure and axis
    fig, ax = plt.subplots()

    # Display the floor plan image
    floor_plan = plt.imread(floor_plan_path)
    ax.imshow(floor_plan, extent=[0, num_lon, 0, num_lat], aspect='auto')

    # Create the heatmap
    sns.heatmap(heatmap_data, cmap='coolwarm', alpha=0.5, annot=True, fmt='.0f', cbar=False)

    # Save the heatmap to a file
    plt.savefig(heatmap_path)

# Example usage



if __name__ == "__main__":
    main()
