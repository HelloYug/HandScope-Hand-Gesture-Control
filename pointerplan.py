import cv2
import numpy as np
import ctypes
import HandTrackingModule as htm
import time

# Camera settings
wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.85, maxHands=1)

# Mouse movement and click
def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)  # Move cursor to x, y position

def left_click():
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up

def right_click():
    ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)  # Right mouse button down
    ctypes.windll.user32.mouse_event(10, 0, 0, 0, 0)  # Right mouse button up

# Initialize variables
xp, yp = 0, 0  # Previous points for smooth movement
frameRate = 5  # Control the cursor speed

while True:
    # Capture frame from the camera
    success, img = cap.read()
    if not success:
        print("Failed to capture image from the camera.")
        break

    # Flip the image for natural interaction
    img = cv2.flip(img, 1)

    # Detect hand and get landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Check which fingers are up
        fingers = detector.fingersUp()

        # If index finger is up, move the cursor
        if fingers[1] == 1 and sum(fingers) == 1:  # Only index finger is up
            x, y = lmList[8][1], lmList[8][2]  # Get index finger tip position

            # Smooth movement: Adjust cursor movement based on the frame rate
            if xp == 0 and yp == 0:
                xp, yp = x, y
            move_mouse(int(x / wCam * 1920), int(y / hCam * 1080))  # Scale to screen size
            xp, yp = x, y

        # Left click gesture (index and thumb touching)
        elif fingers[1] == 1 and fingers[0] == 1 and sum(fingers) == 2:
            left_click()
            time.sleep(0.5)  # Prevent multiple clicks too quickly

        # Right click gesture (index and thumb near each other)
        elif fingers[1] == 1 and fingers[0] == 0 and sum(fingers) == 1:
            # Check if thumb and index finger distance is small (for right-click)
            thumb_tip_x, thumb_tip_y = lmList[4][1], lmList[4][2]
            distance = np.hypot(thumb_tip_x - lmList[8][1], thumb_tip_y - lmList[8][2])
            if distance < 30:  # Adjust this threshold for right-click
                right_click()
                time.sleep(0.5)

    # Display the camera window with landmarks (optional)
    cv2.imshow("Cursor Control", img)

    # Exit the program with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
