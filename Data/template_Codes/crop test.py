import cv2
import numpy

cap = cv2.VideoCapture(0)

_, frame1 = cap.read()

while cap.isOpened():
    frame2 = frame1[frame1.shape[0]//2 -100: frame1.shape[0]//2+100, frame1.shape[1]//2 -100: frame1.shape[1]//2+100]
    cv2.imshow("frame1",frame1)
    cv2.imshow("frame2",frame2)

    if cv2.waitKey(40) == 27:
        break