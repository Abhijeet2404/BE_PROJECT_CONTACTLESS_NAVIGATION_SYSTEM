import cv2
import numpy as np
import Tracking_module as htm
import time
import autopy


wCam, hCam = 640, 480

pTime = 0
cTime = 0


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


detector = htm.handDetector(max_num_hands=1)

width_scr, height_scr = autopy.screen.size()
frame_size_reduction = 50

smoothening_fac = 5
plocX, plocY = 0,0
clocX, clocY = 0,0

while True:
    success, image = cap.read()
    image  = detector.findHands(image=image)
    

    


    # find hand landmarks. (points)
    lmList, bbox = detector.findPosition(image)

    # print(lmList)

    # get the tip of the index and middle 
    if len(lmList) !=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]



    # check which finger are up
        fingers = detector.fingersUP()
        # print(fingers)
        cv2.rectangle(image,(frame_size_reduction, frame_size_reduction), (wCam-frame_size_reduction, hCam-frame_size_reduction),(255,255,255),2)

    # Only Index Finger is moving or not if Yes the map finger x and y coordinated for cursor x and y cordinates 

        if fingers[1] == 1 and fingers[2] ==0:
            
            x3 = np.interp(x1,(frame_size_reduction , wCam - frame_size_reduction) ,  (0 , width_scr ))
            y3 = np.interp(y1,(frame_size_reduction , hCam - frame_size_reduction) ,  (0 , height_scr ))

    # smoothen Values
            clocX = plocX + (x3 - plocX)/smoothening_fac
            clocY = plocY + (y3 - plocY)/smoothening_fac
    # Move mouse
            print(width_scr - clocX,clocY)
            autopy.mouse.move( width_scr - clocX,  clocY)
            cv2.circle(image,(x1,y1), 15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX,clocY
            
    # both Index and middle fingers are up : then excute the clicking operation
        if (fingers[1] == 1 and fingers[2] == 1):
            length,image,line_info=detector.findDistance(8,12,image)
            if (length < 40):
                cv2.circle(image,(line_info[4], line_info[5]), 15, (0,255,150), cv2.FILLED)
                autopy.mouse.click()

            # print(length)
            

    

    

    
    # fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)



    # display the captureing and hand tracking with ploted point over the hand
    cv2.imshow("image", image)
    cv2.waitKey(1)
