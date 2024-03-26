from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2 as cv
import numpy as np

"""
Example script for getting bounding boxes from YOLOv8

Should camera interface be infinite loop or one-shot?
"""

def one_shot(cap : cv.VideoCapture, model : YOLO) -> dict | None:
    # grab image from camera
    ret, img = cap.read()
    if ret is False: return None
    # TODO: undistort image

    # get yolo prediction
    results = model.predict(img, verbose = False)
    # annotate image with results
    coords = []
    for r in results:
        annotator = Annotator(img)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            coords.append(b.numpy().astype(np.uint16))
            c = box.cls
            # label with distance, veloctiy, ... could be added here
            # TODO: 
            label = f'{model.names[int(c)]}'
            annotator.box_label(b, label)
    annotated = {
        'img' : annotator.result(),
        'xyxy' : coords
    }
    return annotated

if __name__ == '__main__':
    # initialize object detection model
    model = YOLO('yolov8n.pt')
    # init camera
    cap = cv.VideoCapture(0)
    # capture loop
    while True:
        annotated = one_shot(cap, model)
        if annotated is not None:
            # display annotated image
            cv.imshow('Detection', annotated['img'])
            # check for loop end
            key = cv.waitKey(1) 
            if key & 0xFF == 27: break
    # cleanup
    cap.release()
    cv.destroyAllWindows()