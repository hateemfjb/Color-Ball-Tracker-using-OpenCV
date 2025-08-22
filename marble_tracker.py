import cv2
import numpy as np

# Load the video file
cap = cv2.VideoCapture("marbles.mp4")

# Prepare to save the output video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, fps, (width, height))

# Define HSV ranges and BGR box colors
colors = {
    "Purple": {
        "lower": np.array([125, 50, 50]),
        "upper": np.array([155, 255, 255]),
        "box_color": (200, 0, 200)  # BGR for purple
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

# Process the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (width, height))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for name, props in colors.items():
        mask = cv2.inRange(hsv, props["lower"], props["upper"])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), props["box_color"], 2)
                cv2.putText(frame, f"{name} Ball", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, props["box_color"], 2)

    # Show result and write to output
    cv2.imshow("Ball Tracker", frame)
    out.write(frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()