"""import cv2
from ultralytics import YOLO

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO("runs/detect/ergo_switch/weights/best.pt")


# -------------------------------
# DEFINE ROIs
# -------------------------------
ROIS = {
    "switch": (180, 50, 280, 400),

    "button1": (240, 100, 150, 100),
    "button2": (240, 200, 150, 100),
    "button3": (240, 300, 150, 100),

    "symbol1": (290, 120, 50, 50),
    "symbol2": (290, 220, 50, 50),
    "symbol3": (300, 320, 50, 50),
}


# -------------------------------
# CHECK POINT INSIDE ROI
# -------------------------------
def inside_roi(cx, cy, roi):
    x, y, w, h = roi
    return x < cx < x + w and y < cy < y + h


# -------------------------------
# MAIN PROCESS FUNCTION
# -------------------------------
def process_frame(frame, selected_type):

    results = model(frame, imgsz=640, conf=0.6)

    annotated = results[0].plot()

    # ---------------- DETECTIONS ----------------
    detections = []

    if results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()

        for box, cls, conf in zip(boxes, classes, confs):
            x1, y1, x2, y2 = box

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            name = model.names[int(cls)]

            detections.append({
                "name": name,
                "cx": cx,
                "cy": cy,
                "conf": conf
            })

    # ---------------- ROI ASSIGNMENT (FIXED) ----------------
    roi_status = {key: None for key in ROIS.keys()}
    roi_conf = {key: 0 for key in ROIS.keys()}

    for det in detections:
        name = det["name"]
        cx = det["cx"]
        cy = det["cy"]
        conf = det["conf"]

        for key, roi in ROIS.items():
            if not inside_roi(cx, cy, roi):
                continue

            # SWITCH ROI
            if key == "switch" and "Switch" in name:
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            # BUTTON ROIs
            elif "button" in key and "Button" in name:
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            # SYMBOL ROIs (STRICT MATCH)
            elif key == "symbol1" and name == "Symbol1":
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            elif key == "symbol2" and name == "Symbol2":
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            elif key == "symbol3" and name == "Symbol3":
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

    # ---------------- EXPECTED ----------------
    switch_expected = f"{selected_type.capitalize()}_Switch"
    button_expected = f"{selected_type.capitalize()}_Button"

    # ---------------- VALIDATION ----------------
    final = "OK"

    if roi_status["switch"] != switch_expected:
        final = "NG"

    for b in ["button1", "button2", "button3"]:
        if roi_status[b] != button_expected:
            final = "NG"

    if roi_status["symbol1"] != "Symbol1":
        final = "NG"

    if roi_status["symbol2"] != "Symbol2":
        final = "NG"

    if roi_status["symbol3"] != "Symbol3":
        final = "NG"

    # ---------------- DRAW ROIs ----------------
    for key, (x, y, w, h) in ROIS.items():

        detected_class = roi_status[key]

        color = (0, 0, 255)  # default RED

        if key == "switch" and detected_class == switch_expected:
            color = (0, 255, 0)

        elif "button" in key and detected_class == button_expected:
            color = (0, 255, 0)

        elif key == "symbol1" and detected_class == "Symbol1":
            color = (0, 255, 0)

        elif key == "symbol2" and detected_class == "Symbol2":
            color = (0, 255, 0)

        elif key == "symbol3" and detected_class == "Symbol3":
            color = (0, 255, 0)

        # Draw ROI
        cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)

        # Label
        label = f"{key}: {detected_class if detected_class else 'None'}"

        cv2.putText(
            annotated,
            label,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    # ---------------- DEBUG PRINT ----------------
    print("ROI STATUS:", roi_status)

    return annotated, roi_status, final"""


import cv2
import numpy as np
from ultralytics import YOLO

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO("runs/detect/ergo_switch/weights/best.pt")


# -------------------------------
# DEFINE ROIs
# -------------------------------
ROIS = {
    "switch": (180, 50, 280, 400),

    "button1": (240, 100, 150, 100),
    "button2": (240, 200, 150, 100),
    "button3": (240, 300, 150, 100),

    "symbol1": (290, 120, 50, 50),
    "symbol2": (290, 220, 50, 50),
    "symbol3": (300, 320, 50, 50),
}


# -------------------------------
# TEMPLATE MATCH FUNCTION
# -------------------------------
def template_match(roi_img, template_path, threshold=0.65):

    template = cv2.imread(template_path)

    if template is None:
        print(f"Template not found: {template_path}")
        return False, 0

    # Resize ROI to template size
    roi_resized = cv2.resize(
        roi_img,
        (template.shape[1], template.shape[0])
    )

    # Convert to gray
    roi_gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Match
    result = cv2.matchTemplate(
        roi_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    score = result[0][0]

    return score >= threshold, score


# -------------------------------
# CHECK POINT INSIDE ROI
# -------------------------------
def inside_roi(cx, cy, roi):
    x, y, w, h = roi
    return x < cx < x + w and y < cy < y + h


# -------------------------------
# MAIN PROCESS FUNCTION
# -------------------------------
def process_frame(frame, selected_type):

    results = model(frame, imgsz=640, conf=0.6)

    annotated = results[0].plot()

    # ---------------- DETECTIONS ----------------
    detections = []

    if results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()

        for box, cls, conf in zip(boxes, classes, confs):

            x1, y1, x2, y2 = box

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            name = model.names[int(cls)]

            detections.append({
                "name": name,
                "cx": cx,
                "cy": cy,
                "conf": conf
            })

    # ---------------- ROI STATUS ----------------
    roi_status = {key: None for key in ROIS.keys()}
    roi_conf = {key: 0 for key in ROIS.keys()}

    for det in detections:

        name = det["name"]
        cx = det["cx"]
        cy = det["cy"]
        conf = det["conf"]

        for key, roi in ROIS.items():

            if not inside_roi(cx, cy, roi):
                continue

            # SWITCH
            if key == "switch" and "Switch" in name:
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            # BUTTONS
            elif "button" in key and "Button" in name:
                if conf > roi_conf[key]:
                    roi_status[key] = name
                    roi_conf[key] = conf

            # SYMBOLS
            elif key == "symbol1" and name == "Symbol1":
                roi_status[key] = name

            elif key == "symbol2" and name == "Symbol2":
                roi_status[key] = name

            elif key == "symbol3" and name == "Symbol3":
                roi_status[key] = name

    # ---------------- EXPECTED ----------------
    switch_expected = f"{selected_type.capitalize()}_Switch"
    button_expected = f"{selected_type.capitalize()}_Button"

    final = "OK"

    # ---------------- YOLO VALIDATION ----------------
    if roi_status["switch"] != switch_expected:
        final = "NG"

    for b in ["button1", "button2", "button3"]:
        if roi_status[b] != button_expected:
            final = "NG"

    # ---------------- TEMPLATE MATCH ----------------
    for symbol in ["symbol1", "symbol2", "symbol3"]:

        x, y, w, h = ROIS[symbol]

        roi_img = frame[y:y+h, x:x+w]

        template_path = f"templates/{selected_type}/{symbol}.jpg"

        matched, score = template_match(
            roi_img,
            template_path,
            threshold=0.65
        )

        print(symbol, "Score:", round(score, 2))

        if not matched:
            final = "NG"

        # DRAW TEMPLATE SCORE
        color = (0, 255, 0) if matched else (0, 0, 255)

        cv2.rectangle(
            annotated,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            annotated,
            f"{symbol}:{score:.2f}",
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    print("ROI STATUS:", roi_status)

    return annotated, roi_status, final