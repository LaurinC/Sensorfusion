from fusion.fusion import Fusion
import cv2 as cv

if __name__ == '__main__':
    # options for com ports
    com = {
        'conf_port': '/dev/ttyUSB0',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': '/dev/ttyUSB1',
        'data_baud': 921600
    }
    fusion = Fusion(com, 'wide_lense3', downsample=2)

    cv.namedWindow('Sensorfusion', cv.WINDOW_NORMAL)
    cv.setWindowProperty('Sensorfusion', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    while cv.waitKey(33) != 27:
        img = fusion()
        cv.imshow('Sensorfusion', img)
    cv.destroyAllWindows()