import time
import tkinter as tk
from tkinter import messagebox
import threading
from interface.radar import Radar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Radar setup
com = {
    'conf_port': 'COM4',
    'conf_baud': 115200,
    'conf_to': 0.01,
    'data_port': 'COM3',
    'data_baud': 921600
}
sensor = Radar(com)

# GUI setup
window = tk.Tk()
window.title("Radar Plot GUI")

# Matplotlib figure setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()  # Interactive mode on

# Plot container
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Pause functionality using threading Event
pause_event = threading.Event()

def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()  # Resume the thread
    else:
        pause_event.set()  # Pause the thread

pause_button = tk.Button(window, text="Pause/Resume", command=toggle_pause)
pause_button.pack()

# Quit button
def quit_program():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.quit()
        window.destroy()

quit_button = tk.Button(window, text="Quit", command=quit_program)
quit_button.pack()

# Plot update function
def update_plot():
    while True:
        pause_event.wait()  # This will block when the event is cleared (paused)
        data = sensor()
        detected_points = data['detected_points']

        x_coords = [coords['x'] for coords in detected_points.values()]
        y_coords = [coords['y'] for coords in detected_points.values()]
        z_coords = [coords['z'] for coords in detected_points.values()]

        
        ax.clear()
        ax.scatter(x_coords, y_coords, z_coords, c='r', marker='o')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        
        # Set axis limits
        ax.set_xlim([-5, 5])
        ax.set_ylim([0, 10])
        ax.set_zlim([-5, 5])

        canvas.draw()

# Start the update plot loop in a separate thread
update_plot_thread = threading.Thread(target=update_plot)
update_plot_thread.daemon = True
update_plot_thread.start()

# Start the tkinter event loop
window.mainloop()
