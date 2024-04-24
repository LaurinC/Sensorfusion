from interface.radar import Radar
from time import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display, clear_output
from collections import deque
import numpy as np

max_length = 50

# Initialize deques to store the values, with a maximum length of 50
v = deque(maxlen=max_length)
x = deque(maxlen=max_length)
y = deque(maxlen=max_length)
z = deque(maxlen=max_length)
colors = deque(maxlen=max_length)  # Store color for each point

# Create a figure and axis for the plot
fig = plt.figure(figsize=(12, 6))

# Subplot for 3D scatter
ax_3d = fig.add_subplot(121, projection='3d')
ax_3d.set_xlim([-5, 5])
ax_3d.set_ylim([0, 10])
ax_3d.set_zlim([-5, 5])
ax_3d.set_xlabel('X Axis')
ax_3d.set_ylabel('Y Axis')
ax_3d.set_zlabel('Z Axis')

# Subplot for 2D top-down view
ax_2d = fig.add_subplot(122)
ax_2d.set_xlim([-5, 5])
ax_2d.set_ylim([0, 10])
ax_2d.set_xlabel('X Axis')
ax_2d.set_ylabel('Y Axis')
ax_2d.set_title('Top-Down View (X-Y Plane)')

# Initial scatter plots
sc_3d = ax_3d.scatter([], [], [], c=[], marker='.')
sc_2d = ax_2d.scatter([], [], c=[], marker='.')

# Function to update the points on the scatter plots
def update_plot():
    global x, y, z, colors, sc_3d, sc_2d
    sc_3d._offsets3d = (x, y, z)
    sc_3d.set_color(colors)  # Update the colors with varying alphas
    sc_2d.set_offsets(np.column_stack([x, y]))
    sc_2d.set_color(colors)
    try:
        plt.draw()
        plt.pause(1/15)  # Pause to allow update to display
    except Exception as e:
        print(f"Error updating plot: {e}")

def update_colors():
    # Update colors, making older points more transparent and color-coding based on distance
    num_points = len(x)
    new_colors = np.zeros((num_points, 4))  # RGBA values
    max_distance = 10  # Assume maximum y value is 10 as per your axis limits

    for i in range(num_points):
        y_value = y[i]
        normalized_y = y_value / max_distance
        red = 1 - normalized_y
        green = normalized_y
        blue = 0
        alpha = i / num_points * 0.9 + 0.1
        new_colors[i] = [red, green, blue, alpha]

    return new_colors

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port': 'COM4',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': 'COM3',
        'data_baud': 921600
    }
    sensor = Radar(com)

    # test: reading a number of data packages
    buffer = []
    data = {}
    try:
        while True:
            buffer.append(sensor())
            data = buffer[-1]

            # Loop over each detected point and extract the values
            for key, point in data['detected_points'].items():
                v.append(point['v'])
                x.append(point['x'])
                y.append(point['y'])
                z.append(point['z'])
                
            colors = update_colors()  # Update color transparency
            update_plot()
            plt.show(block=False)
            if not plt.fignum_exists(fig.number):
                break
    except KeyboardInterrupt:
        plt.close()  # Close the plot when interrupted
