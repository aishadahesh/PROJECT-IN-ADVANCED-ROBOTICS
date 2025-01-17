from ultralytics import YOLO
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import cv2

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

# Live detection and monitoring
def detect_and_monitor(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print("Press 'q' to quit the live feed.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detection
        yolo_results = model_yolo(frame)
        annotated_frame = yolo_results[0].plot()

        # Health assessment
        processed_frame = preprocess_frame(frame)
        health_results = model_health.predict(processed_frame)

        # Annotate with health results
        cv2.putText(annotated_frame, f"Health: {health_results.argmax()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Plant Recognition and Monitoring", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the system
detect_and_monitor()
