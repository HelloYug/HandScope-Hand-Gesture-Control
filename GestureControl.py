import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import ImageGrab
from datetime import datetime
import os
import subprocess
import pyttsx3
import psutil
import pyautogui
import platform

# Camera setup
wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# Audio control setup
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
vol = cast(interface, POINTER(IAudioEndpointVolume))
volRange = vol.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
volPer = 0
colorVol = (255, 0, 0)
isMuted = False
gestureActive = False

# variables
lastScreenshotTime = 0
lastNotepadTime = 0
lastVoiceTime = 0
lastSwipeTime = 0  
swipeCooldown = 1  
thresholdSwipeDistance = 200
lastPlayPauseTime = 0
playPauseCooldown = 2 
thumbs_down_start_time = None  # Track the start time of the thumbs-down gesture
gesture_duration = 3  # Time in seconds for gesture to trigger lock

# Function to check if Notepad is running
def is_notepad_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'notepad.exe' in proc.info['name'].lower():
            return True
    return False

def lock_system():
    """Locks the system based on the operating system."""
    system_platform = platform.system()
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
    except Exception as e:
        print("System Error: System locking not supported on this OS.")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from webcam")
        break

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:

        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        if 250 < area < 1000:
            fingers = detector.fingersUp()
        
            # Thumb down (thumb is pointing down, other fingers are up)
            if fingers == [0, 1, 1, 1, 1]:  # Thumb down, others up
                if thumbs_down_start_time is None:
                    thumbs_down_start_time = time.time()  # Start timer
                elif time.time() - thumbs_down_start_time >= gesture_duration:
                    print("Locking system due to thumbs-down gesture...")
                    lock_system()  # Lock the system
                    break
            else:
                thumbs_down_start_time = None  # Reset timer if gesture is not held

            
            # Volume control
            length, img, lineInfo = detector.findDistance(4, 8, img)
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])

            volPer = 10 * round(volPer / 10)

            if fingers[0] ==1 and fingers[1] ==1 and fingers[2] ==1 and fingers[3] ==0 and fingers[4] ==1  and sum(fingers) == 4:
                pyautogui.hotkey ("fn","f4")

            # Adjust volume when the pinky finger is down
            if not fingers[4]:
                vol.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

            # Mute/unmute with thumb and pinky finger close
            TP_Length, img, _ = detector.findDistance(4, 20, img, draw=False)
            if TP_Length < 50:
                if not gestureActive:
                    try:
                        if not isMuted:
                            vol.SetMasterVolumeLevelScalar(0, None)
                            isMuted = True
                            print("Muted")
                        else:
                            vol.SetMasterVolumeLevelScalar(volPer / 100, None)
                            isMuted = False
                            print("Unmuted")
                    except Exception as e:
                        print(f"Error changing volume: {e}")
                    gestureActive = True
            else:
                gestureActive = False

            # Screenshot gesture: thumb and middle finger touch
            T_M_Length, img, _ = detector.findDistance(4, 12, img, draw=False)
            current_time = time.time()
            if T_M_Length < 30 and current_time - lastScreenshotTime >= 2:  # 2-second gap
                try:
                    screenshot = ImageGrab.grab()
                    screenshotFilename = datetime.now().strftime("%Y-%m-%d_%H;%M;%S.png")
                    screenshot.save(screenshotFilename)
                    print(f"Screenshot saved: {screenshotFilename}")
                    lastScreenshotTime = current_time
                except Exception as e:
                    print(f"Error capturing Screenshot: {e}")

            # Run Notepad : victory gesture
            if fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2:
                current_time = time.time()
                if not is_notepad_running() and current_time - lastNotepadTime >= 5:
                    subprocess.run(["notepad.exe"])
                    print("Notepad started")
                    lastNotepadTime = current_time

            # Desktop switching: Detect palm swipe (all fingers up)
            if all(fingers): 
                palmX = lmList[0][1] 

                if 'prevPalmX' in locals():
                    xDiff = palmX - prevPalmX  # Horizontal movement
                    if abs(xDiff) > thresholdSwipeDistance and current_time - lastSwipeTime >= swipeCooldown:
                        if xDiff > 0:  # Swipe Right
                            pyautogui.hotkey('win', 'ctrl', 'right')
                            print("Switched to desktop on the right")
                        elif xDiff < 0:  # Swipe Left
                            pyautogui.hotkey('win', 'ctrl', 'left')
                            print("Switched to desktop on the left")
                        lastSwipeTime = current_time

                prevPalmX = palmX  

            # Voice message: Yo gesture
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 and fingers[0] == 1:
                current_time = time.time()
                if current_time - lastVoiceTime >= 5:  # 5-second gap
                    engine = pyttsx3.init()
                    string = "Hello sir, how are you?"
                    engine.say(string)
                    print (f"Said '{string}'")
                    engine.runAndWait()
                    lastVoiceTime = current_time

            
    # UI elements for volume and FPS
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cVol = int(vol.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol Set: {int(cVol)}', (750, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

    # Camera window
    cv2.imshow("Gesture Control Project", img)

    # End program
    if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
        break

cap.release()
cv2.destroyAllWindows()
