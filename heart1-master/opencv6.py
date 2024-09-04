import cv2
import time
import os
import mediapipe as mp
import time
import hand as htm

pTime=0
cap=cv2.VideoCapture(0)

FolderPath="Fingers"
lst=os.listdir(FolderPath)
lst_2=[]


for i in lst:
    image=cv2.imread(f"{FolderPath}/{i}")
    print(f"{FolderPath}/{i}")
    lst_2.append(image)

detector= htm.handDetector(detectionCon=1)
fingerid = [4,8,12,16,20]

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    print(lmList)

    if len(lmList) != 0:
        fingers=[]

        # viet cho ngon cai
        if lmList[fingerid[0]][1] > lmList[fingerid[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # viet cho 4 ngon dai
        for id in range(1,5):
            if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)
        songontay = fingers.count(1)
        print(songontay)

        h, w, c = lst_2[songontay-1].shape
        frame[0:h,0:w]= lst_2[songontay-1]
    
    # hien so ngon tay
        cv2.rectangle(frame,(0,150),(100,300),(0,255,0),-1) # ve khung chu nhat
        cv2.putText(frame,str(songontay),(3,280),cv2.FONT_HERSHEY_SIMPLEX,5,(255,0,0),3)


    #viết fps
    cTime= time.time()
    fps=1/(cTime - pTime)
    pTime = cTime
    #show lên
    cv2.putText(frame,f"FPS: {int(fps)}", (110,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("video",frame)
    if cv2.waitKey(1)== ord("a"):
        break



cap.release()
cv2.destroyAllWindows()
