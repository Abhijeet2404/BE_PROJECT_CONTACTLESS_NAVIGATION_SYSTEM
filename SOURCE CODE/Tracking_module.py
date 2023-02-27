import cv2
import mediapipe as mp
import time



class handDectertor():
    def __init__(self,static_image_mode=False,max_num_hands=2,min_detection_confidence=0.8):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        min_detection_confidence = min_detection_confidence
       

        

        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode,self.max_num_hands,min_detection_confidence=0.5)
        self.mpDraw  = mp.solutions.drawing_utils


    def findHands(self,image, draw = True):
        RGB_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(RGB_image)

        print(self.result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)

        return image
                

    def findPosition(self, image, handNo=0, draw= True):

        lmlist = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int (lm.y *h)
                    lmlist.append([id,cx,cy])
                    if (draw):
                        cv2.circle(image, (cx,cy), 15, (255,0,255), cv2.FILLED)

        return lmlist;

                

   




def main():
 
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDectertor()

    while True:
        success, image = cap.read() 
        image = detector.findHands(image)
        lmlist = detector.findPosition(image)

        print ()
        
        
        
        
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