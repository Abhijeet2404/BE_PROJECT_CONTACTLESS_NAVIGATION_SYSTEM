import cv2
import mediapipe as mp
import numpy as np
import time
import math



class handDetector():
    def __init__(self,static_image_mode=False,max_num_hands=2,min_detection_confidence=0.8):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        min_detection_confidence = min_detection_confidence
       

        

        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode,self.max_num_hands,min_detection_confidence=0.5)
        self.mpDraw  = mp.solutions.drawing_utils

        self.tipIds = [4,8,12,16,20]


    def findHands(self,image, draw = True):
        RGB_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(RGB_image)

        # print(self.result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)

        return image
                

    def findPosition(self, image, handNo=0, draw= True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int (lm.y *h)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([id,cx,cy])
                    if (draw):
                        cv2.circle(image, (cx,cy), 5, (255,0,255), cv2.FILLED)
            xmin, xmax = min(xList),max(xList)
            ymin, ymax = min(yList),max(yList)
            bbox = xmin,ymin,xmax,ymax
            if draw:
                cv2.rectangle(image,(xmin-20,ymin-20), (xmax+20,ymax+20), (0,255,0))

                

        return self.lmList,bbox;


    def fingersUP(self):
        fingers = []
       
        if (self.lmList[self.tipIds[0]][1]  >  self.lmList[self.tipIds[0]-1][1]):
            fingers.append(1)

        else:
            fingers.append(0)

        for id in range(1,5): 
        
            if (self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0);


        return fingers
    
    def findDistance(self,p1,p2,image,draw=True,r=15,t=3):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        cx,cy = (x1+x2) //2, (y1 + y2) // 2

        if draw:
            cv2.line(image,(x1,y1),(x2,y2),(255,0,255), t)
            cv2.circle(image,(x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(image,(x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(image,(cx,cy),r,(155,255,155),cv2.FILLED)

        dist = math.hypot(x2-x1,y2-y1)

        return dist,image,[x1,y1,x2,y2,cx,cy]



                

   




def main():
 
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, image = cap.read() 
        image = detector.findHands(image)
        lmlist = detector.findPosition(image)

        # print ()
        
        
        
        
        #calculate fps and display it: 
        cTime = time.time()
        fps  = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        #display the live tracking of the hands

        cv2.imshow("Image",image)
        cv2.waitKey(1)



if __name__ =="__main__":
    main()






















print("hello world")