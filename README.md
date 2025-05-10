# 🔊 Hand Gesture System Control with Python

Control your system using **hand gestures** in real-time with this Python-based project using **OpenCV**, **MediaPipe**, and **pycaw**. This tool leverages your webcam to track hand landmarks and perform various tasks on the system.

---

## 📸 Features

- Real-time hand tracking via webcam
- Volume control using thumb-index finger distance
- Mute/unmute, screenshot, and desktop control gestures
- Visual volume percentage display
- System-level audio control (via `pycaw`)
- Basic cross-platform support (Windows recommended for full features)

---

## ✋ Supported Gestures

| Gesture                               | Action                |
|---------------------------------------|-----------------------|
| Thumb-index finger distance           | Adjust volume         |
| Thumb down (others up)                | Lock the system       |
| Thumb + pinky close                   | Mute/Unmute           |
| Thumb + middle finger touch           | Take a screenshot     |
| Victory (index + middle finger up)    | Launch Notepad        |
| Palm open (all fingers up)            | Switch desktop        |
| Yo gesture (index + pinky up)         | Voice message trigger |

---

## 🧠 Tech Stack

| Technology  | Role                                  |
|-------------|---------------------------------------|
| Python      | Main programming language             |
| OpenCV      | Webcam feed and image processing      |
| MediaPipe   | Hand landmark tracking                |
| pycaw       | Volume control on Windows             |
| pyttsx3     | Text-to-speech feedback               |
| pyautogui   | GUI automation                        |
| psutil      | Process and system monitoring         |
| Pillow      | Image handling and screenshot capture |

---

## 📂 Project Structure
```plaintext
hand-volume-control/
│
├── main.py                 # Main script for gesture control
├── HandTrackingModule.py   # Hand detection and gesture logic
├── MouseControl.py         # Experimental mouse gesture control
├── VirtualDraw.py          # Air drawing using finger gestures
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation
```
---

## 🚀 Getting Started

### 1. Clone the repository

git clone https://github.com/yourusername/hand-volume-control.git
cd hand-volume-control

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the project

python main.py

---
## 📌 Requirements

- Python 3.7 or higher
- Webcam (1080p recommended)
- Windows (for full `pycaw` compatibility)

---
## ⚙️ Configuration

You can customize or add new gestures inside the main.py loop:
- Modify landmark logic
- Map gesture to specific functions
- Add new gesture recognition patterns

---
## 👨‍💻 Author

**Yug Agarwal**
- 📧 [yugagarwal704@gmail.com](mailto:yugagarwal704@gmail.com)
- 🔗 GitHub – [@HelloYug](https://github.com/HelloYug)