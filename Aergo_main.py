import tkinter as tk
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import os
from Aergo_camera import Camera
from Aergo_processing import process_frame
from Aergo_gui import App
from Aergo_logger import init_log, save_log   # ✅ NEW


cam = Camera()
init_log()   # ✅ CREATE CSV FILE

running = False


# -------------------------------
# START CAMERA
# -------------------------------
def start_camera():
    global running
    cam.start()
    running = True
    update_frame()


# -------------------------------
# LIVE FRAME LOOP
# -------------------------------
def update_frame():
    if not running:
        return

    ret, frame = cam.read()
    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb))
        app.update_image(img)

    root.after(10, update_frame)


# -------------------------------
# CAPTURE + PROCESS
# -------------------------------
def capture_image(selected_type):
    frame = cam.capture()

    if frame is None:
        return

    annotated, roi_status, final = process_frame(frame, selected_type)

    # Convert ROI status to readable text
    detected = [f"{k}:{v}" for k, v in roi_status.items()]

    # ✅ SAVE CSV LOG
    save_log(selected_type, final, roi_status)

    # ✅ SAVE NG IMAGE (optional but recommended)
    if final == "NG":
        os.makedirs("ng_images", exist_ok=True)
        filename = datetime.now().strftime("ng_images/%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(filename, frame)

    # UPDATE GUI
    app.update_result(final, annotated, detected)


# -------------------------------
# STOP CAMERA
# -------------------------------
def stop_camera():
    global running
    running = False
    cam.stop()


# -------------------------------
# GUI INIT
# -------------------------------
root = tk.Tk()

app = App(
    root,
    on_start=start_camera,
    on_capture=capture_image,
    on_stop=stop_camera
)

root.mainloop()

cam.stop()
cv2.destroyAllWindows()