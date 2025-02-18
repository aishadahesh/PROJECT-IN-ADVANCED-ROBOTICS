from ultralytics import YOLO
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import cv2
import numpy as np
import time

# Load YOLOv8s model for detection
model_yolo = YOLO('yolov8s.pt')

# Build MobileNetV2 model for health assessment
base_model = MobileNetV2(weights='imagenet', include_top=False)
model_health = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dense(128, activation='relu'),
    Dense(3, activation='softmax')  
])
model_health.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Preprocessing function
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))
    normalized_frame = resized_frame / 255.0
    return normalized_frame.reshape(1, 224, 224, 3)

# Function to detect plants using the drone's camera and record video
def detect_and_monitor(drone):
    print("[INFO] Starting plant detection on drone camera...")

    frame_width, frame_height = 960, 720  # Default Tello resolution
    video_filename = f"tello_record_{int(time.time())}.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec
    out = cv2.VideoWriter(video_filename, fourcc, 30.0, (frame_width, frame_height))

    print(f"[INFO] Recording started: {video_filename}")

    while True:
        frame = drone.get_frame_read().frame
        if frame is None:
            print("[ERROR] Failed to capture frame from drone.")
            continue

        frame = cv2.resize(frame, (frame_width, frame_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detection
        yolo_results = model_yolo(frame)
        annotated_frame = yolo_results[0].plot()

        # Health assessment
        processed_frame = preprocess_frame(frame)
        health_results = model_health.predict(processed_frame)

        # Annotate with health results
        cv2.putText(annotated_frame, f"Health: {health_results.argmax()}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display and save video
        cv2.imshow("Plant Recognition and Monitoring", annotated_frame)
        out.write(annotated_frame)  # Save frame to video file

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"[INFO] Recording saved as: {video_filename}")
    out.release()
    cv2.destroyAllWindows()
