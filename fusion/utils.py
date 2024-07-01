import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


"""
Functions neeeded for loading camera parameters and
projecting radar points into camera coordinate system
"""

def load_coeffs(name : str) -> dict:
    return dict(np.load(f'fusion/coefficients/{name}.npz'))

def project_points(data : dict, cam_mtx : np.ndarray) -> np.ndarray:
    # 1. create point matrix
    # initialize
    num_obj = data['header']['objects']
    points = data['detected_points']
    point_mtx = np.zeros((3, num_obj))
    # fill matrix (y from radar is z in camera coordinates)
    point_mtx[0, :] = np.array([coords['x'] for coords in points.values()]) # X
    point_mtx[1, :] = np.array([coords['z'] for coords in points.values()]) # Y
    point_mtx[2, :] = np.array([coords['y'] for coords in points.values()]) # Z
    v = np.array([coords['v'] for coords in points.values()])
    # 2. project points (X,Y,Z) -> (u,v,Z)
    proj = (cam_mtx @ point_mtx) # (X,Y,Z) -> (u',v',Z)
    proj[:2, :] /= point_mtx[2,:] # (u',v',Z) -> (u,v,Z)
    # 3. add velocity values
    proj = np.vstack((proj, v))
    # 3. remove points not displayable inside image
    valid = proj[:, np.all((proj[:3,:]>=0)&(proj[0,:]<800)&(proj[1,:]<600) ,axis=0)]
    print(valid)
    return valid

"""
Random functions needed in conversion of tlv packages

copied from pymmw: https://github.com/m6c7l/pymmw/blob/master/source/lib/utility.py
"""

def intify(value, base = 16, size = 2):
    if type(value) not in (tuple, list, bytes,):
        value = (value,)
    if (type(value) in (bytes,) and base == 16) or (type(value) in (list, tuple,)):
        return sum([item * ((base ** size) ** i) for i, item in enumerate(value)]) 
    else:
        return sum([((item // 16) * base + (item % 16)) * ((base**size) ** i) for i, item in enumerate(value)])

def q_to_dec(value, n):
    return value / (1 << n)

def q_to_db(value):
    return q_to_dec(value, 9) * 6

"""
Main plot as matplotlib and opencv version
"""

def display_fusion(img : np.ndarray, points : np.ndarray):
    # TODO: display velocity as label over projected points
    fig, ax = plt.subplots(figsize=(10,6))
    fig.suptitle('Projection Visualization')
    ax.imshow(img)
    sc = ax.scatter(points[0, :], points[1, :], c = points[2, :], cmap = 'viridis', vmin = 0, vmax = 10)
    cbar = fig.colorbar(sc, shrink = 0.6)
    cbar.ax.set_ylabel('Z in [m]', rotation = 90)
    return fig

def label_image(img : np.ndarray, points : np.ndarray, scale : float = 0.4, color : tuple = (0,255,0)) -> np.ndarray:
    for i in range(points.shape[1]):
        # mark detected point, add depth value as label
        point = (int(points[0,i]),int(points[1,i]))
        img = cv.circle(img, point, 4, color, cv.FILLED)
        text=f'Z={points[2,i]:2.2f}'
        (w,h), __ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        img = cv.putText(img, text, (point[0]-w//2,point[1]-5), cv.FONT_HERSHEY_SIMPLEX, scale, color, 1)
        if points[3,i] > 0.01 or points[3,i] < 0.01:
            text=f'v={points[3,i]:2.2f}'
            (w,h), __ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.4, 1)
            img = cv.putText(img, text, (point[0]-w//2,point[1]+h+5), cv.FONT_HERSHEY_SIMPLEX, scale, color, 1)
    return img