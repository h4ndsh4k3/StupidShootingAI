import numpy as np
import cv2
import time
import pyfirmata

def calculateDistance(x):
    return abs((x / (450/180))- 180)


def mainloop():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)


    board = pyfirmata.Arduino('COM3') #plugged in via USB, serial com at rate 9600
    iter = pyfirmata.util.Iterator(board)
    iter.start()

    servo = board.get_pin("d:{}:s".format(9)) #connecting to a servo on port 9

    lastValue = 0

    while(True):
        ret, frame = cap.read()#frame size: 640x480

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            #print("x: {}, y: {}, w: {}, h: {}".format(x, y, w, h))
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            distance = int(calculateDistance(x))
            print(distance)
            if (lastValue == 0 or lastValue != distance):
                lastValue = distance
                servo.write(distance)




        cv2.imshow("poop", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if(__name__ == '__main__'):
    mainloop()
