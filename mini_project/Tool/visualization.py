import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

def plot_heatmap_on_floorplan(heatmap, floorplan_image):
    # Load the floor plan image
    floorplan = mpimg.imread(floorplan_image)

    # Normalize the heatmap values to a range of [0, 1]
    heatmap_normalized = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())

    # Create an RGBA heatmap with an alpha channel for transparency
    cmap = plt.get_cmap('coolwarm')
    heatmap_rgba = cmap(heatmap_normalized)
    heatmap_rgba[..., -1] = heatmap_normalized

    # Overlay the heatmap on the floor plan
    plt.imshow(floorplan, aspect='auto')
    plt.imshow(heatmap_rgba, aspect='auto', alpha=0.7, origin='lower')

    # Add colorbar and labels
    cbar = plt.colorbar()
    cbar.set_label('Signal Strength')
    plt.title('Wi-Fi Network Heatmap on CS_Building Floor Plan')
    plt.axis('off')

    # Save the visualization as an image file
    output_image = "visualization.png"
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {output_image}")

    # Show the visualization
    plt.show()

def main():
    # Load the heatmap numpy array
    heatmap_file = "heatmap.npy"
    heatmap = np.load(heatmap_file)

    # Specify the floor plan image file
    floorplan_image = "floorplan.png"

    # Plot the heatmap on the floor plan
    plot_heatmap_on_floorplan(heatmap, floorplan_image)

if __name__ == "__main__":
    main()
