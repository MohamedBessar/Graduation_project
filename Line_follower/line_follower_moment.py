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
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            slope = cy / cx
            print("CX : " + str(cx) + "  CY : " + str(cy))
            print("Slope: " + str(slope))
            #             if cx >= 380 or cx <237 :
            #                 print("Turn Left")
            #             if cx < 380 and cx > 250 :
            #                 print("On Track!")
            #             if cx <=40 :
            #                 print("Turn Right")
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    else:
        print("I don't see the line")
    cv2.drawContours(frame, c, -1, (0, 255, 0), 1)
    cv2.imshow("Mask", threshold)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(15) & 0xff == ord('q'):  # 1 is the time in ms
        break
cap.release()
cv2.destroyAllWindows()