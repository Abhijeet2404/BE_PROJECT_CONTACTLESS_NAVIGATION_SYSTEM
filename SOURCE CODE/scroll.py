import cv2
import numpy as np
import Tracking_module as htm
import time
import autopy
import pyautogui


wCam, hCam = 640, 480

pTime = 0
cTime = 0


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


detector = htm.handDetector(max_num_hands=1)

width_scr, height_scr = autopy.screen.size()
frame_size_reduction = 50

smoothening_fac = 10
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
        x1,y1 = (bbox[0]+bbox[2])//2,(bbox[1]+bbox[3])//2
      



    # check which finger are up
        fingers = detector.fingersUP()
        # print(fingers)
        cv2.rectangle(image,(frame_size_reduction, frame_size_reduction), (wCam-frame_size_reduction, hCam-frame_size_reduction),(255,255,255),2)
        x3 = np.interp(x1,(frame_size_reduction , wCam - frame_size_reduction) ,  (0 , width_scr ))
        y3 = np.interp(y1,(frame_size_reduction , hCam - frame_size_reduction) ,  (0 , height_scr ))
    # Only Index Finger is moving or not if Yes the map finger x and y coordinated for cursor x and y cordinates 
        if (fingers == [0,0,0,0,0]):
            # autopy.scroll(-100,)
         

            clocX =   (x3 )
            clocY =   (y3  )
            print(clocY)
            if (clocY <500 or clocY>600):
                pyautogui.scroll(int((540-clocY)))

            # plocY = 0
            # plocX = 0


      

    

    

    
    # fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)



    # display the captureing and hand tracking with ploted point over the hand
    cv2.imshow("image", image)
    cv2.waitKey(1)
