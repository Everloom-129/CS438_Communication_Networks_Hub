import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import seaborn as sns
from PIL import Image
import sys

floor_plan_path     = "AP_info\F1.png"
default_data_path   = "preprocessed_data\preprocessed_mean.csv"
default_output_path = "heatmap\heatmap_F1.png"


def generate_heatmap(data, x_points, y_points):
    if data.empty:
        print("Error: No data points found. Please ensure the input file has valid data.")
        return None, None, None
    x = data['x']
    y = data['y']
    signal_strength = data['Signal Strength']

    # Create a grid of points for the entire floor plan
    X, Y = np.meshgrid(x_points, y_points)

    # Interpolate the signal strength using Radial Basis Function (RBF)
    rbf = Rbf(x, y, signal_strength, function='multiquadric', smooth=1, epsilon=0.5)
    Z = rbf(X, Y)

    return X, Y, Z


def main():
    # Read the raw data CSV file
    if len(sys.argv) == 2:
        bssid = sys.argv[1]
        mac_data_file = f"preprocessed_data\{bssid}.csv"
        heatmap_path = f"heatmap\heatmap_{bssid}.png"
    else:
        mac_data_file = default_data_path
        heatmap_path = default_output_path
    
    data = pd.read_csv(mac_data_file)
    
    # Load the floor plan image using PIL (Python Imaging Library)
    floor_plan_image = Image.open(floor_plan_path)
    floor_plan_array = np.array(floor_plan_image)

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Define the dimensions of the floor plan
    floor_width, floor_height = floor_plan_image.size
    aspect_ratio = floor_width / floor_height


    # Define the resolution of the heatmap
    resolution = 1

    # Generate a grid of points for the entire floor plan
    x_points = np.arange(0, floor_width, resolution)
    y_points = np.arange(0, floor_height, resolution)

    # Mark each (x,y) coordinate
    ax.scatter(data["x"], data["y"], s=1, c='purple')

    # Generate the heatmap
    X, Y, Z = generate_heatmap(data, x_points, y_points)
    print("X,Y,Z : ",X,Y,Z)
    # Check if heatmap data is generated
    if X is None or Y is None or Z is None:
        print("Heatmap not generated due to empty data.")
        return

    # Display the floor plan image on the axis
    ax.imshow(floor_plan_array, origin="lower", extent=[0, floor_width, 0, floor_height], aspect='auto')

    # Plot the heatmap on top of the floor plan image
    heatmap = ax.imshow(Z, cmap='jet', alpha=0.5, origin='lower', extent=[0, floor_width, 0, floor_height], aspect='auto')
    
    
    plt.colorbar(heatmap, label='Signal_Strength')
    plt.title('Wi-Fi Network Heatmap')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # Invert the Y-axis to make (0, 0) be the top-left corner
    ax.invert_yaxis()

    # Save the heatmap to a file
    plt.savefig(heatmap_path)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
