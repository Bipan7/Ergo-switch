import tkinter as tk
from tkinter import Label, Frame, Button, Radiobutton, StringVar
from PIL import Image, ImageTk
from datetime import datetime
import cv2


class App:
    def __init__(self, root, on_start, on_capture, on_stop):
        self.root = root
        self.root.title("Ergo Switch")
        self.root.state("zoomed")
        self.root.configure(bg="#dfe6e9")

        self.on_start = on_start
        self.on_capture = on_capture
        self.on_stop = on_stop

        self.selected_type = StringVar(value="black")

        self.ok_count = 0
        self.ng_count = 0

        # ================= HEADER =================
        header = Frame(root, bg="#2c3e50", height=80)
        header.pack(fill="x")

        # LOGO (LEFT)
        try:
            logo_img = Image.open("Black.jpg")  # <-- put your logo file
            logo_img = logo_img.resize((60, 60))
            self.logo = ImageTk.PhotoImage(logo_img)
            Label(header, image=self.logo, bg="#2c3e50").pack(side="left", padx=10)
        except:
            pass

        # TITLE
        Label(header, text="ERGO SWITCH",
              bg="#2c3e50", fg="white",
              font=("Arial", 24, "bold")).pack(side="left", padx=10)

        # DATE TIME (BIG + BOLD)
        self.time_label = Label(header,
                                bg="#2c3e50",
                                fg="white",
                                font=("Arial", 16, "bold"))
        self.time_label.pack(side="right", padx=20)
        self.update_time()

        # ================= BODY =================
        body = Frame(root, bg="#dfe6e9")
        body.pack(fill="both", expand=True)

        # -------- LEFT PANEL (REFERENCE IMAGE) --------
        left_panel = Frame(body, width=300, bg="#ecf0f1", bd=2, relief="solid")
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        Label(left_panel,
              text="REFERENCE",
              font=("Arial", 16, "bold"),
              bg="#ecf0f1").pack(pady=10)

        self.ref_label = Label(left_panel, bg="#ecf0f1")
        self.ref_label.pack(padx=10, pady=10)

        # Load reference image
        try:
            ref_img = Image.open("Brown.jpg")  # <-- put your reference image
            ref_img = ref_img.resize((260, 300))
            self.ref_imgtk = ImageTk.PhotoImage(ref_img)
            self.ref_label.configure(image=self.ref_imgtk)
        except:
            self.ref_label.configure(text="No Image")

        # -------- RIGHT SIDE --------
        right_panel = Frame(body, bg="#dfe6e9")
        right_panel.pack(side="right", expand=True)

        # LIVE VIEW
        live_frame = Frame(right_panel, width=550, height=500,
                           bg="black", bd=3, relief="solid")
        live_frame.pack(side="left", padx=20, pady=20)
        live_frame.pack_propagate(False)

        self.live_label = Label(live_frame, bg="black")
        self.live_label.pack(expand=True)

        # RESULT VIEW
        result_frame = Frame(right_panel, width=550, height=500,
                             bg="black", bd=3, relief="solid")
        result_frame.pack(side="right", padx=20, pady=20)
        result_frame.pack_propagate(False)

        self.result_label = Label(result_frame, bg="black")
        self.result_label.pack(expand=True)

        # ================= CONTROLS =================
        control = Frame(root, bg="#b2bec3")
        control.pack(fill="x", ipady=15)

        # BIG BUTTONS
        Button(control, text="START",
               bg="#27ae60", fg="white",
               font=("Arial", 14, "bold"),
               width=10,
               command=self.on_start).pack(side="left", padx=15)

        Button(control, text="CAPTURE",
               bg="#8e44ad", fg="white",
               font=("Arial", 14, "bold"),
               width=12,
               command=self.capture_click).pack(side="left", padx=15)

        Button(control, text="STOP",
               bg="#c0392b", fg="white",
               font=("Arial", 14, "bold"),
               width=10,
               command=self.on_stop).pack(side="left", padx=15)

        # RADIO BUTTONS
        Radiobutton(control, text="Black",
                    variable=self.selected_type,
                    value="black",
                    bg="#b2bec3",
                    font=("Arial", 12, "bold")).pack(side="left", padx=10)

        Radiobutton(control, text="Brown",
                    variable=self.selected_type,
                    value="brown",
                    bg="#b2bec3",
                    font=("Arial", 12, "bold")).pack(side="left", padx=10)

        Radiobutton(control, text="Grey",
                    variable=self.selected_type,
                    value="grey",
                    bg="#b2bec3",
                    font=("Arial", 12, "bold")).pack(side="left", padx=10)

        # RESULT TEXT
        #self.result_text = Label(control,
         #                        text="Result: -",
          #                       font=("Arial", 12, "bold"),
           #                      bg="#b2bec3")
        #self.result_text.pack(side="right", padx=20)

        # COUNTER
        self.counter = Label(control,
                             text="OK: 0 | NG: 0",
                             font=("Arial", 12, "bold"),
                             bg="#b2bec3")
        self.counter.pack(side="right", padx=20)

        # ================= STATUS BAR (BIG) =================
        self.status = Label(root,
                            text="WAITING",
                            bg="#f1c40f",
                            fg="black",
                            font=("Arial", 28, "bold"),
                            relief="sunken",
                            bd=4)
        self.status.pack(fill="x", ipady=30)

    # ---------------- UPDATE LIVE IMAGE ----------------
    def update_image(self, frame):
        self.live_label.configure(image=frame)
        self.live_label.image = frame

    # ---------------- CAPTURE ----------------
    def capture_click(self):
        self.on_capture(self.selected_type.get())

    # ---------------- RESULT ----------------
    def update_result(self, final, yolo_frame, detected):

        display = cv2.resize(yolo_frame, (680, 480))
        rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb))

        self.result_label.configure(image=img)
        self.result_label.image = img

        if final == "OK":
            self.ok_count += 1
            self.status.config(text="OK", bg="#2ecc71")
        else:
            self.ng_count += 1
            self.status.config(text="NG", bg="#e74c3c")

        self.counter.config(text=f"OK: {self.ok_count} | NG: {self.ng_count}")
        #self.result_text.config(text=f"{final} | {', '.join(detected)}")

    # ---------------- TIME ----------------
    def update_time(self):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)