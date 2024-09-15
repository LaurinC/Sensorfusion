from cv2 import undistort, VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from .radar import Radar
from .utils import load_coeffs, project_points, label_image

class Fusion():
    def __init__(self, radar_config : dict, params : str, downsample : int = 2):
        # setup camera
        self.params = load_coeffs(params)
        self.mtx = self.params['mtx_rad']
        self.mtx[:2,2] /= downsample
        self.cap = VideoCapture(0)
        self.cap.set(CAP_PROP_FRAME_HEIGHT, 1200 // downsample)
        self.cap.set(CAP_PROP_FRAME_WIDTH, 1600 // downsample)
        # setup radar
        self.radar = Radar(radar_config)

    def __call__(self):
        # get image from camera, undistort
        ret, img = self.cap.read()
        if not ret: print('Error accessing camera'); return
        udst = undistort(img, self.params['mtx'], self.params['dist'])
        # get radar data, project onto image plane
        radar_data = self.radar()
        points = project_points(radar_data, self.mtx, t = (0.,0.045))
        return label_image(udst, points)
    
    def __del__(self):
        self.radar.close()
        self.cap.release()