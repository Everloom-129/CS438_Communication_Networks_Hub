import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image

def show_image_with_grid(image_path, grid_spacing_x=50, grid_spacing_y=50, output_folder='heatmap'):
    # Load the image using PIL (Python Imaging Library)
    image = Image.open(image_path)
    img_array = np.array(image)

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Display the image on the axis
    ax.imshow(img_array)

    # Set the grid spacing (you can adjust these values to change the grid size)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(grid_spacing_x))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(grid_spacing_y))

    # Customize the grid appearance
    ax.grid(which='major', color='grey', linestyle='--', linewidth=1, alpha=0.1)

    # Save the output image and text file
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    plt.savefig(output_image_path)

    width, height = image.size
    aspect_ratio = width / height

    with open(os.path.join(output_folder, 'img_size.txt'), 'a') as f:
        f.write(f"Image: {output_image_path}\n")
        f.write(f"Size: {width} x {height}\n")
        f.write(f"Aspect Ratio: {aspect_ratio}\n\n")
    plt.show()

def main():
    image_list = [
        "AP_info\F0.png",
        "AP_info\F1.png",
        "AP_info\F2.png",
        "AP_info\F3.png",
        "AP_info\F4.png",
    ]

    # selected_floor = int(input("Enter the floor number to be printed (0-4): "))
    # if 0 <= selected_floor < len(image_list):
    selected_floor = 0
    while selected_floor <5:
        show_image_with_grid(image_list[selected_floor])
        selected_floor += 1

if __name__ == "__main__":
    main()
