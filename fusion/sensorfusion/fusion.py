import cv2 as cv
from .radar import Radar
from .utils import load_coeffs, project_points

class Fusion():
    def __init__(self, radar_config : dict, params : str):
        # setup radar
        self.radar = Radar(radar_config)
        # setup camera
        self.params = load_coeffs(params)
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)

    def __call__(self):
        # get image from camera, undistort
        ret, img = self.cap.read()
        if not ret: print('Error accessing camera'); return
        udst = cv.undistort(img, self.params['mtx'], self.params['dist'])
        # get radar data, project to camera coordinate system
        points = project_points(self.radar(), self.params)
        return udst, points
    
    def __del__(self):
        self.radar.close()
        self.cap.release()
