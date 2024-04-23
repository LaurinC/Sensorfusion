import numpy as np
import os
import cv2 as cv

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

def load_coeffs(name : str) -> dict:
    return np.load(f'coefficients/{name}.npz')