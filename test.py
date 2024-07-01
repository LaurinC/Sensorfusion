from fusion.fusion import Fusion
from fusion.utils import display_fusion

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port': 'COM4',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': 'COM3',
        'data_baud': 921600
    }
    fusion = Fusion(com, 'wide_lense1')