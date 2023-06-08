import socket
import cv2
import time
import numpy as np
from tensorflow.keras.models import load_model


#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('', 5000))
# s.listen(5)
# print("Server is running now")
# # #s.connect(("192.168.1.58", 5000))
# clientsocket, address = s.accept()
# while True:
#     print(s.recv(1024).decode("utf-8 "))


human_face=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the saved model
model = load_model('face_lock.h5')

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create a dictionary to map class indices to labels
class_labels = {0: "Mohamed", 1: "Random People"}

flag = True
counter = 0

while flag:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=human_face.detectMultiScale(gray,1.3,8)
    if faces.all():
        # Resize the frame to 224x224 (the input size of the model)
        resized = cv2.resize(frame, (224, 224))
        normalized = resized / 255.0

        # Reshape the image to be a 4D tensor with shape (batch_size, height, width, channels)
        reshaped = np.reshape(normalized, (1, 224, 224, 3))

        # Make a prediction on the reshaped image
        predictions = model.predict(reshaped)
        class_index = predictions[0]
        if predictions[0] > 0.84:
            class_label = "Mohamed"
            print(predictions[0])
           # clientsocket.send("Mohamed".encode("utf-8"))
            #s.close()
            flag = False
        else:
            class_label = "Random"
            print(predictions[0])
           # clientsocket.send("Random".encode("utf-8"))

            if counter != 3:
                counter += 1
                time.sleep(3.0)
            else:
                #clientsocket.send("Random".encode("utf-8"))
                #s.close()

                continue
    else:
        print("Please stand up in front of the camera")

    # Normalize the pixel values to be between 0 and 1

    # Draw the class label on the frame

    #cv2.putText(frame, class_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


