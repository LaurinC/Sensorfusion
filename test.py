from fusion.fusion import Fusion
from cv2 import waitKey, imshow, destroyAllWindows, namedWindow

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port': '/dev/ttyUSB0',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': '/dev/ttyUSB1',
        'data_baud': 921600
    }
    fusion = Fusion(com, 'wide_lense1', downsample=1)

    namedWindow('Sensorfusion')

    while waitKey(33) != 27:
        img = fusion()
        imshow('Sensorfusion', img)
    destroyAllWindows()