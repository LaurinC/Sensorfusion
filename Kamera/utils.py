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
        'newmtx' : coeffs['newmtx'],
        'dist' : coeffs['dist'],
    }
    json_coeffs = {key : value.tolist() if isinstance(value, np.ndarray) else value for key, value in json_coeffs.items()}
    with open(f'coefficients/{name}.json', 'w') as f:
        json.dump(json_coeffs, f, indent=3)

def load_coeffs(name : str) -> dict:
    return dict(np.load(f'coefficients/{name}.npz'))