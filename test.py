from fusion.fusion import Fusion
from fusion.utils import display_fusion

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port': '/dev/ttyUSB0',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': '/dev/ttyUSB1',
        'data_baud': 921600
    }
    fusion = Fusion(com, 'wide_lense1')

    while True:
        udst, points = fusion()
        fig = display_fusion(udst, points)
        while not fig.waitforbuttonpress(): pass
        
        break
