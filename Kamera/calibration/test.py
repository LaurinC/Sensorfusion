import cv2 as cv
import os
import numpy as np
from utils import load_coeffs, load_from_folder



if __name__ == '__main__':
    name = 'wide_lense'
    # load calibration coefficients
    coeffs = load_coeffs(name)
    # undistort test image
    images = load_from_folder(f'images/{name}/')
    for img in images:
        udst = cv.undistort(img, coeffs['mtx'], coeffs['dist'], None, coeffs['newmtx'])
        cv.imshow('undistorted', udst)
        cv.waitKey(-1)
        cv.destroyAllWindows()
        break
