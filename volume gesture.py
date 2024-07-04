import cv2
import mediapipe as mp
import time

import numpy as np

import handtrackingmodule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime = 0


detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumerange = volume.GetVolumeRange()


minvol = volumerange[0]
maxvol = volumerange[1]

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        print(lmlist[4], lmlist[8])

        x1,y1 = lmlist[4][1], lmlist[4][2]
        x2,y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1 + x2) // 2, (y1 + y2) //2

        cv2.circle(img, (x1, y1), 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0),3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length,[50,250],[minvol,maxvol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
