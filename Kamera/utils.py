import numpy as np
import os
import cv2 as cv
import json

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

def save_coeffs(name : str, coeffs : dict):
    # dump as npz
    np.savez(f'coefficients/{name}.npz', **coeffs)

    # dump in human readable format
    json_coeffs = {
        'mtx' : coeffs['mtx'],
        'mtx_rad' : coeffs['mtx_rad'],
        'newmtx' : coeffs['newmtx'],
        'dist' : coeffs['dist'],
    }
    json_coeffs = {key : value.tolist() if isinstance(value, np.ndarray) else value for key, value in json_coeffs.items()}
    with open(f'coefficients/{name}.json', 'w') as f:
        json.dump(json_coeffs, f, indent=3)

def load_coeffs(name : str) -> dict:
    return dict(np.load(f'coefficients/{name}.npz'))

def project_points(data : dict, calib_params : dict) -> np.ndarray:
    # 1. create point matrix
    # initialize
    num_obj = data['header']['objects']
    points = data['detected_points']
    point_mtx = np.zeros((3, num_obj))
    cam_mtx = calib_params['mtx_rad']
    # fill matrix (y from radar is z in camera coordinates)
    point_mtx[0, :] = np.array([coords['x'] for coords in points.values()]) # X
    point_mtx[1, :] = np.array([coords['z'] for coords in points.values()]) # Y
    point_mtx[2, :] = np.array([coords['y'] for coords in points.values()]) # Z
    # 2. project points (X,Y,Z) -> (u,v,Z)
    proj = (cam_mtx @ point_mtx) # (X,Y,Z) -> (u',v',Z)
    proj[:2, :] /= point_mtx[2,:] # (u',v',z') -> (u,v,Z)
    return proj