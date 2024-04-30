import cv2 as cv
import numpy as np
from utils import load_coeffs, project_points
import matplotlib.pyplot as plt


if __name__ == '__main__':
    

    data = {
        'header': {
            'objects': 2, 
        },
        'detected_points': 
        {
            '0,0': 
            {
                'v': 0.0, 
                'x': -0.25,
                'y': 1.18, 
                'z': 0.07
            },
            '1,1': 
            {
                'v': 0.0, 
                'x': -0.39,
                'y': 0.85, 
                'z': -0.03
            },
        }
    }

    # project points to image plane
    coeffs = load_coeffs('wide_lense')
    points = project_points(data, coeffs)

    cap = cv.VideoCapture(2, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FPS, 20)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

    # discard images until camera is initiated
    while True:
        ret, img = cap.read()
        if not ret: break

        cv.imshow("grab", img)
        c = cv.waitKey(1)
        if c == 27: break
    cv.destroyAllWindows()

    # BGR2RGB
    img = img[...,::-1]

    # display point over image
    plt.figure(figsize=(10, 6))
    plt.suptitle('Projection Visualization')
    plt.imshow(img)
    plt.scatter(points[0, :], points[1, :], c = points[2, :], cmap = 'viridis', vmin = 0, vmax = 10)
    cbar = plt.colorbar(shrink = 0.6)
    cbar.ax.set_ylabel('Z in [m]', rotation = 90)
    plt.show()