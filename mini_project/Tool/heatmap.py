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
    # create_heatmap("raw_data.csv", "floor_plan\Siebel-Floor-Plan-1.jpg", "heatmap\h1.png")

    # Read the preprocessed data CSV file
    preprocessed_data_file = "preprocessed_data.csv"
    data = pd.read_csv(preprocessed_data_file)

    # Define the dimensions of the floor plan
    floor_width = 100
    floor_height = 100

    # Define the resolution of the heatmap
    resolution = 1

    # Generate a grid of points for the entire floor plan
    x_points = np.arange(0, floor_width, resolution)
    y_points = np.arange(0, floor_height, resolution)

    # Generate the heatmap
    X, Y, Z = generate_heatmap(data, x_points, y_points)

    # Save the heatmap as a numpy array
    heatmap_file = "heatmap.npy"
    np.save(heatmap_file, Z)
    print(f"Heatmap saved to {heatmap_file}")

    # Plot the heatmap
    plt.imshow(Z, cmap='coolwarm', origin='lower', extent=[0, floor_width, 0, floor_height], aspect='auto')
    plt.colorbar(label='Signal Strength')
    plt.title('Wi-Fi Network Heatmap')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def create_heatmap(raw_data_path, floor_plan_path, heatmap_path):
    # Load Wi-Fi data
    wifi_data = pd.read_csv(raw_data_path)


    # Create an empty grid for the heatmap
    max_x = 10
    max_y = 10
    heatmap_data = np.zeros((max_x, max_y))


    # Fill the heatmap grid with signal strength data
    for index, row in wifi_data.iterrows():
        print(f"Index: {index}, x: {row['x']}, y: {row['y']} ss: {row['Signal Strength']}")
        x_index = row['x']
        y_index = row['y']
        heatmap_data[x_index, y_index] = row['Signal Strength']

    # # Set up the figure and axis
    # fig, ax = plt.subplots()

    # # Display the floor plan image
    # floor_plan = plt.imread(floor_plan_path)
    # ax.imshow(floor_plan, extent=[0, max_x, 0, max_y], aspect='auto')
    print("heatmap")
    # Create the heatmap
    heatmap = sns.heatmap(heatmap_data, cmap='coolwarm', alpha=0.5, annot=True, fmt='.0f', cbar=False)
    heatmap.get_figure().savefig(heatmap_path)
    # Save the heatmap to a file
    # plt.savefig(heatmap_path)

# Example usage



if __name__ == "__main__":
    main()
