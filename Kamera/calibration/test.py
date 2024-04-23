import cv2 as cv
from utils import load_coeffs

if __name__ == '__main__':
    # load calibration coefficients    
    coeffs = load_coeffs('wide_lense')

    # configurate video capture
    cap = cv.VideoCapture(1, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FPS, 20)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


    # display undistored image
    while True:
        ret, img = cap.read()
        if not ret: break

        udst = cv.undistort(img, coeffs['mtx'], coeffs['dist'], None, coeffs['newmtx'])

        cv.imshow("grab", udst)
        c = cv.waitKey(1)
        if c == 27: break

    cv.destroyAllWindows()