## Color Ball Tracker using OpenCV

![output](https://github.com/user-attachments/assets/5b682757-9eae-4ff6-a2b6-00846f6a1fbf)


## 📝 Description  
This project uses **Python** and **OpenCV** to detect and track multiple colored balls in a prerecorded video.  
Bounding boxes and labels are drawn on each detected object in real-time, and the processed video is saved as an output file.

---

## 📦 Features
- 🟣🔵🟡 Tracks 3 colors: **Purple**, **Blue**, **Yellow**  
- 📁 Works on prerecorded video (no camera required)  
- 🖼 Draws bounding boxes and labels on detected balls  
- 💾 Saves the output as a new video file  

---

## 🚀 How to Run

### 1️⃣ Requirements
- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

📦 Install dependencies:
```bash
pip install opencv-python numpy
```

---

### 2️⃣ Run the Script
```bash
python marble_tracker.py
```
💡 Press **Q** to quit the video window anytime.

---

## 📁 Project Files

| File Name           | Description                          |
|---------------------|--------------------------------------|
| `marble_tracker.py` | Main Python script                   |
| `marbles.mp4`       | Input video used for tracking        |
| `output.avi`        | Output video with detected objects   |
| `result.png`        | Optional screenshot of final result  |

---

## 🎥 Output
- ✅ Processed video saved as `output.avi`
- 📦 Bounding boxes drawn around detected colored balls
- 🖼 Screenshot saved as `result.png`

---

## 💻 Code Snapshot

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("marbles.mp4")

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, fps, (width, height))

colors = {
    "Purple": {
        "lower": np.array([125, 50, 50]),
        "upper": np.array([155, 255, 255]),
        "box_color": (200, 0, 200)
    },
    "Blue": {
        "lower": np.array([90, 100, 50]),
        "upper": np.array([130, 255, 255]),
        "box_color": (255, 0, 0)
    },
    "Yellow": {
        "lower": np.array([20, 100, 100]),
        "upper": np.array([30, 255, 255]),
        "box_color": (0, 255, 255)
    }
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (width, height))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for name, props in colors.items():
        mask = cv2.inRange(hsv, props["lower"], props["upper"])
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), props["box_color"], 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, props["box_color"], 2)

    out.write(frame)
    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
