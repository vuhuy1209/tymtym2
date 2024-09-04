
from tkinter import Y
import numpy as np
import cv2
import time
import hand as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime=0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=1)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() # pham vi am luong tu -96.0 toi 0.0
print (volRange)
print (type(volRange))

minVol = volRange[0]
maxVol = volRange[1]



while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame,draw=False)

    if len(lmList) != 0 :
        x1, y1 = lmList[4][1], lmList[4][2] #toa do dau ngon cai
        x2, y2 = lmList[8][1], lmList[8][2] #toa do dau ngon tro
        #ve duong tron tren ngon cai và ngón trỏ
        cv2.circle(frame,(x1,y1),15,(255,0,255),-1)
        cv2.circle(frame,(x2,y2),15,(255,0,255),-1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(frame,(cx,cy),10,(255,0,255),-1)

        length = math.hypot((x1-x2),(y1-y2))
        #print(length)
        #do dai tay vao khoang 25-280
        #do dai khoang cach am luong -96 toi 0
        vol = np.interp(length,[25,280],[minVol,maxVol])
        volBar = np.interp(length,[25,280],[400,150])
        vol_tyle = np.interp(length,[25,280],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        if length <25 :
            cv2.circle(frame,(cx,cy),15,(0,255,255),-1)
        # ve hinh chu nhat
        cv2.rectangle(frame,(50,150),(100,400),(0,255,0),3)
        cv2.rectangle(frame,(50,int(volBar)),(100,400),(0,255,0),-1)
        cv2.putText(frame,f"{int(vol_tyle)} %", (40,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    #viết fps
    cTime= time.time()
    fps=1/(cTime - pTime)
    pTime = cTime
    #show lên
    cv2.putText(frame,f"FPS: {int(fps)}", (110,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow(" huy  ",frame)
    if cv2.waitKey(1) == ord("a"): #do tre 1/1000s an a se thoat
        break

cap.release()
cv2.destroyAllWindows()