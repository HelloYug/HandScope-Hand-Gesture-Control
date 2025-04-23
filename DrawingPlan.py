import cv2
import numpy as np
import HandTrackingModule as htm

# Camera settings
wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Create a blank canvas for drawing
canvas = np.zeros((hCam, wCam, 3), dtype=np.uint8)

# Colors for drawing
drawColor = (255, 0, 255)  # Purple
brushThickness = 15
eraserThickness = 50

# Initialize variables
xp, yp = 0, 0  # Previous points
detector = htm.handDetector(detectionCon=0.85, maxHands=1)

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

        # If only the index finger is up, draw
        if fingers[1] == 1 and sum(fingers) == 1:  # Only index finger is up
            x, y = lmList[8][1], lmList[8][2]  # Get index finger tip position

            if xp == 0 and yp == 0:  # If no previous points, set current as start
                xp, yp = x, y

            # Draw on the canvas
            cv2.line(canvas, (xp, yp), (x, y), drawColor, brushThickness)
            xp, yp = x, y

        # If all fingers are down, reset the starting point
        elif sum(fingers) == 0:
            xp, yp = 0, 0

        # Erase if both index and middle fingers are up
        if fingers[1] == 1 and fingers[2] == 1:
            x, y = lmList[8][1], lmList[8][2]  # Get index finger tip position
            cv2.circle(canvas, (x, y), eraserThickness, (0, 0, 0), cv2.FILLED)
            xp, yp = x, y

    # Combine the canvas and the camera feed
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    # Display the image
    cv2.imshow("Virtual Drawing", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
