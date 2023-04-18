import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

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

if __name__ == "__main__":
    main()
