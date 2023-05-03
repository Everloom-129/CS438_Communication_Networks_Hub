import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image

# Load the image using PIL (Python Imaging Library)



image = Image.open("AP_info\F1.png")
img_array = np.array(image)

# Create a new figure and axis
fig, ax = plt.subplots()

# Display the image on the axis
ax.imshow(img_array)

# Set the grid spacing (you can adjust these values to change the grid size)
grid_spacing_x = 50
grid_spacing_y = 50

# Create grid lines using ticker.MultipleLocator
ax.xaxis.set_major_locator(ticker.MultipleLocator(grid_spacing_x))
ax.yaxis.set_major_locator(ticker.MultipleLocator(grid_spacing_y))

# Customize the grid appearance
# ax.grid(which='major', color='blue', linestyle='--', linewidth=1, alpha=0.5)

# Show the plot with the grid overlaid on the image
plt.show()
