import cv2
import serial
import numpy as np

ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, timeout=1000)
prev_direction = "w"
next_direction = ""
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
            if cx < 280:
                next_direction = "a"
                print("Turn Left")
            if cx < 390 and cx > 290:
                next_direction = "w"
                print("On Track!")
            if cx >= 390:
                next_direction = "d"
                print("Turn Right")
            if next_direction != prev_direction:
                # send direction in serial port
                ser.write(next_direction.encode())
                prev_direction = next_direction

            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    else:
        print("I don't see the line")
        ser.write("s".encode())
    cv2.drawContours(frame, c, -1, (0, 255, 0), 1)
    #    cv2.imshow("Mask", threshold)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(15) & 0xff == ord('q'):  # 1 is the time in ms
        break
cap.release()
cv2.destroyAllWindows()

