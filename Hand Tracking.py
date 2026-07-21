import cv2
from cvzone.HandTrackingModule import HandDetector 
import mouse
import numpy as np
import threading
import time

detector = HandDetector(detectionCon=0.9,maxHands=1)

#PID
Kp = 0.3
Kd = 0.1

cap=cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(3,cam_w)
cap.set(4,cam_h)

frameR = 100
l_delay=0
r_delay=0


def l_clk_delay():
    global l_delay
    global l_clk_thread
    time.sleep(1)
    l_delay = 0
    l_clk_thread = threading.Thread(target=l_clk_delay)

def r_clk_delay():
    global r_delay
    global r_clk_thread
    time.sleep(1)
    r_delay = 0
    r_clk_thread = threading.Thread(target=r_clk_delay)

l_clk_thread = threading.Thread(target= l_clk_delay)
r_clk_thread = threading.Thread(target= r_clk_delay)

curr_x, curr_y = cam_w // 2, cam_h // 2
prev_error_x, prev_error_y = 0, 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    cv2.rectangle(img, (frameR, frameR), (cam_w - frameR, cam_h - frameR), (255, 0, 255, 2))

    if hands:
        lmlist = hands[0]['lmList']
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        mid_x, mid_y = lmlist[12][0], lmlist[12][1]

        cv2.circle(img, (ind_x, ind_y), 5,(0,255,255), 2)
        fingers=detector.fingersUp(hands[0])
  

        if fingers[1]==1 and fingers[2]==0 and fingers[0]==1:
            
            conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0,1440)))
            conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0,900)))
            
            #Pid - Kp
            error_x = conv_x - curr_x
            error_y = conv_y - curr_y
            deriv_x = error_x - prev_error_x
            deriv_y = error_y - prev_error_y

            curr_x += int(Kp * error_x + Kd * deriv_x)
            curr_y += int(Kp * error_y + Kd * deriv_y)

            mouse.move(curr_x, curr_y)

            prev_error_x = error_x
            prev_error_y = error_y

        if fingers[1]==1 and fingers[2]==1 and fingers[0]==1:
            if abs(ind_x-mid_x) < 25:
                #left
                if l_delay==0 and fingers[4] ==0:
                    mouse.click(button="left")
                    l_delay =1
                    l_clk_thread.start()
                #right
                if r_delay==0 and fingers[4] ==1:
                    mouse.click(button="right")
                    r_delay =1
                    r_clk_thread.start()


    cv2.imshow("Camera", img)
    cv2.waitKey(1)



