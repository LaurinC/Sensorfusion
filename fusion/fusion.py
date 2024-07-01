import cv2 as cv
from .radar import Radar
from .utils import load_coeffs, project_points

class Fusion():
    def __init__(self, radar_config : dict, params : str):
        # setup camera
        self.params = load_coeffs(params)
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
        # setup radar
        self.radar = Radar(radar_config)

    def __call__(self):
        print('Capture')
        # get image from camera, undistort
        ret, img = self.cap.read()
        print('Undistort')
        if not ret: print('Error accessing camera'); return
        udst = cv.undistort(img, self.params['mtx'], self.params['dist'])
        print('Radar')
        radar_data = self.radar()
        print('Project')
        # get radar data, project to camera coordinate system
        points = project_points(radar_data, self.params)
        return udst, points
    
    def __del__(self):
        self.radar.close()
        self.cap.release()
