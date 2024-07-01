import cv2 as cv
from .radar import Radar
from .utils import load_coeffs, project_points

class Fusion():
    def __init__(self, radar_config : dict, params : str, downsample : int = 2):
        # setup camera
        self.params = load_coeffs(params)
        self.mtx = self.params['mtx_rad']
        self.mtx[:2,2] /= downsample
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1200 // downsample)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600 // downsample)
        # setup radar
        self.radar = Radar(radar_config)

    def __call__(self):
        print('Cap')
        # get image from camera, undistort
        ret, img = self.cap.read()
        print('udst')
        if not ret: print('Error accessing camera'); return
        udst = cv.undistort(img, self.params['mtx'], self.params['dist'])
        # get radar data, project to camera coordinate system
        print('radar')
        radar_data = self.radar()
        print('project')
        points = project_points(radar_data, self.mtx)
        return udst, points
    
    def __del__(self):
        self.radar.close()
        self.cap.release()
