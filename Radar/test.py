from interface.radar import Radar
from time import time
import matplotlib.pyplot as plt

"""
This script is a small test script for showcasing the interface of a radar sensor.
It demonstrates how to use the interface to read data from the radar sensor.

Before running this script, make sure to flash the Demo Firmware on the radar sensor.

The script performs the following steps:
1. Initializes the communication ports for the radar sensor.
2. Creates an instance of the Radar class using the specified communication ports.
3. Reads 3 data packages from the radar sensor and stores them in a list.
4. Prints the time taken to read each data package.
5. Prints the last data package read from the radar sensor.
"""

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port' : 'COM4',
        'conf_baud' : 115200,
        'conf_to' : 0.01,
        'data_port' : 'COM3',
        'data_baud' : 921600
    }
    sensor = Radar(com)

    # test: reading a number of data packages
    data = []
    for i in range(10):
        print(data[-1] if data else 'No data')