import cv2
import numpy as np
import Tracking_module as htm
import time
import autopy
import pyautogui


class Gesture_controller:
    def __init__(self):
        self.wCam, self.hCam = 640, 480
        self.pTime = 0
        self.cTime = 0
        self.width_scr, self.height_scr = autopy.screen.size()

      
        self.frame_size_reduction_w = 80
        self.frame_size_reduction_h = 150

        self.detector = htm.handDetector(max_num_hands=1)


        self.smoothening_fac = 5 
        self.plocX, self.plocY = 0,0
        self.clocX, self.clocY = 0,0



        """"
            index = 1
            index and mid = 2
            fist = 3
        """







    def classification(self,fingers):
        result = -1

        if fingers == [0,1,0,0,0]:
            result = 1

        if fingers == [0,1,1,0,0]:
            result = 2

        if fingers == [0,0,0,0,0]:
            result = 3

        return result

        



    def execution(self,image,list,bbox,result,x1,y1):
        
        x3 = np.interp(x1,(self.frame_size_reduction_w , self.wCam - self.frame_size_reduction_w) ,  (0 , self.width_scr ))
        y3 = np.interp(y1,(self.frame_size_reduction_h , self.hCam - self.frame_size_reduction_h) ,  (0 , self.height_scr ))
            
        if result == 1:
            
            self.clocX = self.plocX + (x3 - self.plocX)/self.smoothening_fac
            self.clocY = self.plocY + (y3 - self.plocY)/self.smoothening_fac
            autopy.mouse.move( self.width_scr - self.clocX,  self.clocY)
            self.plocX, self.plocY = self.clocX,self.clocY


        if result == 2:
            lmList = list
            length,image,line_info=self.detector.findDistance(8,12,image)
            if (length < 40):
                # cv2.circle(image,(line_info[4], line_info[5]), 10, (0,255,150), cv2.FILLED)
                autopy.mouse.click()
                cv2.waitKey(5)

        if result == 3:
            self.clocY =   (y3  )
            # print(clocY)
            if (self.clocY <500 or self.clocY>600):
                pyautogui.scroll(int((540-self.clocY)))






    def main(self):
        cap = cv2.VideoCapture(0)
        cap.set(3,self.wCam)
        cap.set(4,self.hCam)
        
        while True:
            success, image = cap.read()
            image  = self.detector.findHands(image=image)
            lmList, bbox = self.detector.findPosition(image)


            if len(lmList) !=0:
                x1,y1 = lmList[8][1:]
                x2,y2 = lmList[12][1:]



                fingers = self.detector.fingersUP()

                result = self.classification(fingers)

                print(result)

                self.execution(image,lmList,bbox,result,x1,y1)

            self.cTime = time.time()
            fps = 1/(self.cTime - self.pTime)
            self.pTime = self.cTime
            cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            cv2.rectangle(image,(self.frame_size_reduction_w, self.frame_size_reduction_h), (self.wCam-self.frame_size_reduction_w, self.hCam-self.frame_size_reduction_h),(255,255,255),2)




            # display the captureing and hand tracking with ploted point over the hand
            cv2.imshow("image", image)
            cv2.waitKey(1)



def driver():
    controller = Gesture_controller()
    controller.main()



driver()




            

        








        
