from ultralytics import YOLO
import os
import cv2
import pandas as pd
import numpy as np

# Modelle laden
object_model = YOLO("player_detection_model_yolo11.pt")

# Verzeichnisse
data_dir = "frames"
output_dir = "player_detection_results"
os.makedirs(output_dir, exist_ok=True)


# Bilder durchlaufen
for img_name in os.listdir(data_dir):
    img_path = os.path.join(data_dir, img_name)
    output_img_path = os.path.join(output_dir, img_name)

    if img_name.startswith('.') or not os.path.isfile(img_path) or not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    image = cv2.imread(img_path)
    height, width = image.shape[:2]

    # Objekterkennung
    detections = object_model(img_path, conf=0.5)[0]
    if not detections or detections.boxes is None:
        continue

    for box in detections.boxes:
        cls_id = int(box.cls.item())
        class_name = object_model.names[cls_id]
        conf = float(box.conf.item())

        # Bounding Box Koordinaten
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)

        # Zeichne Bounding Box
        color = (0, 255, 0)  # grün
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
        cv2.putText(image, f"{class_name} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Bild speichern
    cv2.imwrite(output_img_path, image)


print("✅ Alle Objekte wurden erkannt, Bounding Boxes gezeichnet und Spieler mit Pose-Estimation analysiert.")