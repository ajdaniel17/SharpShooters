import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY),5)
    circles=cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 50)# ret=[[Xpos,Ypos,Radius],...]
    if circles is not None:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")      
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame, center, 1, (0, 0, 255), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame, center, radius, (0, 255, 0), 3)
    else:
        print("No Circle!")
    cv2.imshow('video',frame)
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()