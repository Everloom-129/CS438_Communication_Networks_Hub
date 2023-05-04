import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import seaborn as sns
from PIL import Image

def generate_heatmap(data, x_points, y_points):
    x = data['x']
    y = data['y']
    signal_strength = data['Signal_Strength']

    # Create a grid of points for the entire floor plan
    X, Y = np.meshgrid(x_points, y_points)

    # Interpolate the signal strength using Radial Basis Function (RBF)
    rbf = Rbf(x, y, signal_strength, function='multiquadric', smooth=1)
    Z = rbf(X, Y)

    return X, Y, Z

def main():
    # Read the raw data CSV file
    raw_data_file = "raw_data.csv"
    data = pd.read_csv(raw_data_file)

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

    # Load the floor plan image using PIL (Python Imaging Library)
    floor_plan_path = "AP_info\F1.png"
    floor_plan_image = Image.open(floor_plan_path)
    floor_plan_array = np.array(floor_plan_image)

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Display the floor plan image on the axis
    ax.imshow(floor_plan_array, extent=[0, floor_width, 0, floor_height], aspect='auto')

    # Plot the heatmap on top of the floor plan image
    heatmap = ax.imshow(Z, cmap='coolwarm', alpha=0.5, origin='lower', extent=[0, floor_width, 0, floor_height], aspect='auto')
    plt.colorbar(heatmap, label='Signal Strength')
    plt.title('Wi-Fi Network Heatmap')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # Save the heatmap to a file
    heatmap_path = "heatmap\heatmap_F1.png"
    plt.savefig(heatmap_path)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
