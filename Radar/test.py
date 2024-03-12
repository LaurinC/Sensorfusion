from interface.radar import Radar
from time import time

"""
Small test script for showcasing interface (and its problems)

Requires Demo Firmware to be flashed beforehand
"""

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port' : 'COM4',
        'conf_baud' : 115200,
        'conf_to' : 0.01,
        'data_port' : 'COM5',
        'data_baud' : 921600
    }
    sensor = Radar(com)

    # test: reading 3 data packages
    data = []
    for i in range(3):
        start = time()
        data.append(sensor())
        print(f'{time() - start}s')
    
    print(data[-1])