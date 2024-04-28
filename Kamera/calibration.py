import numpy as np
import cv2 as cv
import os
from argparse import ArgumentParser, Namespace
from utils import load_from_folder, save_coeffs

"""Functions for grabbing calibration images (user still needs to manually select valid ones)
and finding camera matrix and distortion coefficients
"""

def grab_images(args : Namespace):
    # check if output directory exists
    if not os.path.exists(f'images/{args.out}'): os.makedirs(f'images/{args.out}')
    # initialize camera and set image size (this takes a while)
    cap = cv.VideoCapture(1)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
    # image indice
    i = 0
    # wait for user
    _ = input('Ready? ')
    while True:
        # read image
        ret, img = cap.read()
        # check for valid frame
        if not ret: break
        # show video stream
        cv.imshow('Stream', img)
        # save image
        cv.imwrite(f'images/{args.out}/{i+1}.jpg', img)
        i += 1
        # wait one second
        k = cv.waitKey(1000)
        # check if user wants to cancel or all images are captured
        if k == 27 or i == args.num_imgs: break
    cv.destroyAllWindows() 

def calibrate(args : Namespace):
    # termination criteria for cornerSubPix()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare Object points
    objp = np.zeros((args.cols*args.rows, 3), np.float32)
    objp[:,:2] = np.mgrid[0:args.rows,0:args.cols].T.reshape(-1, 2)
    # 3d points in world
    objpoints = []
    # 2d points in image plane
    imgpoints = []
    # load calibration images
    images = load_from_folder(f'images/{args.inp}')
    for image in images:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (args.rows,args.cols), None)
        if ret == True:
            objpoints.append(objp)
            corners_fine = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners_fine)
    # assumption: distorted image has same dimensions as calibration images
    # get camera matrix from object, image points
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # get refined camera matrix, cuts all invalid pixels from image and resizes to input
    newmtx, _ = cv.getOptimalNewCameraMatrix(mtx, dist, gray.shape[::-1], args.alpha, gray.shape[::-1])
    # save coefficients
    save_coeffs(args.out, {
        'mtx' : mtx,
        'newmtx' : newmtx,
        'dist' : dist,
        'rvecs' : rvecs,
        'tvecs' : tvecs
    })

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-out', help = 'Name of output directory', default = 'wide_lense')
    parser.add_argument('-mode', help = 'Choose function to run', default = 'calibrate', choices = ['calibrate','grab'])
    # arguments for grab_images
    parser.add_argument('--num_imgs', help = 'Amount of images to capture', default = 25)
    # arguments for calibrate
    parser.add_argument('--inp', help = 'Folder with input images', default = 'wide_lense')
    parser.add_argument('--rows', help = 'Number of rows in checkerboard pattern', default = 8)
    parser.add_argument('--cols', help = 'Number of cols in checkerboard pattern', default = 6)
    parser.add_argument('--alpha', help = 'Crop images ? 1.0 : 0.0', default = 1.0)
    args = parser.parse_args()

    if args.mode == 'calibrate':
        calibrate(args)
    else:
        grab_images(args)

    
    








