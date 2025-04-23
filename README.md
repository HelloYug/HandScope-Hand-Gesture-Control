## 🔊 Hand Gesture Volume Control with Python

This project uses **OpenCV**, **MediaPipe**, and **pycaw** to control your system's audio volume using **hand gestures**. It tracks hand landmarks using your webcam and adjusts volume based on the distance between your thumb and index finger.


## 📸 Features

- Real-time hand tracking using webcam
- Volume control using thumb-index distance
- Clean GUI with volume percentage display
- System-level audio control via `pycaw`
- Cross-platform compatibility (Windows recommended)

## Available Gestures

- Volume control using thumb-index distance
- Mute/unmute with thumb and pinky finger close
- Screenshot gesture: thumb and middle finger touch
- Run Notepad : victory gesture
- Desktop switching: Detect palm swipe (all fingers up)
- Voice message: Yo gesture

## 🧠 Tech Stack

| Technology      | Purpose                                  |
|------------------|------------------------------------------|
| Python           | Core programming language                |
| OpenCV           | Image processing and webcam feed         |
| MediaPipe        | Hand tracking and landmark detection     |
| pycaw            | System volume control (Windows only)     |
| pyttsx3          | Text-to-speech for feedback              |
| pyautogui        | Screen interaction (optional)            |
| psutil           | Process and system monitoring            |
| Pillow           | Screenshot or GUI-based tasks            |


## 📂 Project Structure

project-folder/
│
├── MouseControl.py           # Custom mouse movement control
├── VirtualDraw.py            # Custom Draw in the air  
├── HandTrackingModule.py     # Custom hand tracking logic using MediaPipe
├── main.py                   # Main script to run volume control
├── requirements.txt          # Python dependencies
└── README.md                 # You're here


## 🚀 Getting Started

### 1. Clone the repository

git clone https://github.com/yourusername/hand-volume-control.git
cd hand-volume-control

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the project

python main.py


## 📌 Requirements

- Python 3.7 or higher
- Webcam (preferably 720p or above)
- Windows (for full `pycaw` compatibility)


## ⚙️ Configuration (Optional)

- Run "main.py"
- make your custom gestures in main.py in the loop


## 🙌 Acknowledgements

- [MediaPipe](https://mediapipe.dev)
- [OpenCV](https://opencv.org)
- [pycaw](https://github.com/AndreMiras/pycaw)

---

## 👨‍💻 Author

**Yug Agarwal** – [@HelloYug](https://github.com/HelloYug)
**E-Mail:** - [yugagarwal704@gmail.com](mailto:yugagarwal704@gmail.com)