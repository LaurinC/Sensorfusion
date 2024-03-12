import numpy as np
import cv2 as cv
import os

"""@package docstring
Functions for calculating Camera Matrix, Distortion Coefficients and Refined Matrix
for undistorting Images

Calibration images need to be of the same size and feature a Checker Board from different angles
There should be at least 9 images
"""

def load_from_folder(path : str) -> list:
    """Loads all images from specified folder
    @param path : path to folder containing ONLY images
    @return images : list of images in BGR Format
    """
    filenames = os.listdir(path)
    images = []
    for filename in filenames:
        images.append(cv.imread(os.path.join(path, filename)))
    return images

def calibrate(path : str, alpha : int = 0, save : bool = False):
    """Calculates camera Matrix, refined matrix and distortion coefficients
    @param path  : path to the folder with calibration images
    @param alpha : alpha parameter for cv.getOptimalNewCameraMatrix
    @param save  : save coefficients (True) or return (False)  
    """
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # termination criteria for cornerSubPix()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare Object points
    objp = np.zeros((6*7, 3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1, 2)
    
    objpoints = []
    imgpoints = []
    # load calibration images
    images = load_from_folder(path)
    for image in images[:10]:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (7,6), None)
        if ret == True:
            objpoints.append(objp)
            corners_fine = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners_fine)
    # assumption: distorted image has same dimensions as calibration images
    # get camera matrix from object, image points
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # get refined camera matrix, cuts all unvalid pixels from image and resizes to input
    newmtx, _ = cv.getOptimalNewCameraMatrix(mtx, dist, gray.shape[::-1], alpha, gray.shape[::-1])
    if save: 
        # save coefficients 
        name = path.split('/')[1]
        np.savez(f'./coefficients/calibration_{name}.npz', mtx = mtx, dist = dist, newmtx = newmtx)
    else: return mtx, dist, newmtx

if __name__ == '__main__':
    # sample for usage of functions
    save = True
    if save: 
        # calibrate, save and load
        folder = 'test'
        calibrate(f'./{folder}', save = True)
        coeffs = np.load(f'./coefficients/calibration_{folder}.npz')
        print(coeffs['mtx'])
        print(coeffs['dist'])
        print(coeffs['newmtx'])
    else:
        # calibrate, direct usage and undistort image
        
        # get matrix, distortion coeffs and refined matrix
        mtx, dist, newmtx = calibrate('./test')
        # load test image
        image = cv.imread('./test/left12.jpg')
        # undistort 
        dst = cv.undistort(image, mtx, dist, None, newmtx)
        # display undistorted image
        cv.imshow('undistorted', dst)
        cv.waitKey(-1)
        cv.destroyAllWindows()

    
    








