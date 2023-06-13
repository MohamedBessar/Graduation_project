import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Convert the frame from the BGR color space to the HSV color space

    # Create a binary mask of the pixels in the image that fall within the color range
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

    # Find the contours of the line
    contours, hierarchy = cv2.findContours(threshold, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        # Assuming you have already obtained the contour in the variable 'c'
        c = max(contours, key=cv2.contourArea)
        # Fit a line to the contour points
        [vx, vy, x, y] = cv2.fitLine(c,cv2.DIST_L2, 0, 0.01, 0.01)
        # Compute the slope of the line
        slope = vy / vx

        print("CX : " + str(vx) + "  CY : " + str(vy))
        print("Slope: " + str(slope))
    cv2.drawContours(frame, c, -1, (0, 255, 0), 1)
    cv2.imshow("Mask", threshold)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(20) & 0xff == ord('q'):  # 1 is the time in ms
        break
cap.release()
cv2.destroyAllWindows()