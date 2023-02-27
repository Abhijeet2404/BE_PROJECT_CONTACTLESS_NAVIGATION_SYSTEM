import cv2
import mediapipe as mp
import time



cap = cv2.VideoCapture(0)


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw  = mp.solutions.drawing_utils


pTime = 0
cTime = 0


while True:
    success, image = cap.read()

    RGB_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    result = hands.process(RGB_image)

    print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int (lm.y *h)
                cv2.circle(image, (cx,cy), 15, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps  = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)


    cv2.imshow("Image",image)
    cv2.waitKey(1)


print("hello world")