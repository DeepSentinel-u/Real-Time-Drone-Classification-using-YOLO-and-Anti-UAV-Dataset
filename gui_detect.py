import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from ultralytics import YOLO
import os
import time
import threading
import winsound

class DetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual-Model Video Detection System")
        self.root.geometry("800x600")

        # Initialize variables with default model paths
        self.visible_model_path = r"C:\Users\Lenovo\Desktop\best(可见光）.pt"
        self.infrared_model_path = r"C:\Users\Lenovo\Desktop\best（红外）.pt"
        self.video_path = None
        self.model = None
        self.is_running = False
        self.cap = None
        self.last_alert_time = 0  # Track last alert time to avoid spamming

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Model Type Selection
        tk.Label(self.root, text="Model Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.model_type_var = tk.StringVar(value="Visible")
        model_types = ["Visible", "Infrared"]
        tk.OptionMenu(self.root, self.model_type_var, *model_types).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Visible Model Path
        tk.Label(self.root, text="Visible Model:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.visible_model_entry = tk.Entry(self.root, width=50)
        self.visible_model_entry.grid(row=1, column=1, padx=5, pady=5)
        self.visible_model_entry.insert(0, self.visible_model_path)
        tk.Button(self.root, text="Browse", command=self.browse_visible_model).grid(row=1, column=2, padx=5, pady=5)

        # Infrared Model Path
        tk.Label(self.root, text="Infrared Model:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.infrared_model_entry = tk.Entry(self.root, width=50)
        self.infrared_model_entry.grid(row=2, column=1, padx=5, pady=5)
        self.infrared_model_entry.insert(0, self.infrared_model_path)
        tk.Button(self.root, text="Browse", command=self.browse_infrared_model).grid(row=2, column=2, padx=5, pady=5)

        # Video Path
        tk.Label(self.root, text="Video File:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.video_entry = tk.Entry(self.root, width=50)
        self.video_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_video).grid(row=3, column=2, padx=5, pady=5)

        # Control Buttons
        tk.Button(self.root, text="Load Model", command=self.load_model).grid(row=4, column=0, padx=5, pady=10)
        tk.Button(self.root, text="Start Detection", command=self.start_detection).grid(row=4, column=1, padx=5,
                                                                                        pady=10)

        # Video Display
        self.video_label = tk.Label(self.root)
        self.video_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def browse_visible_model(self):
        path = filedialog.askopenfilename(filetypes=[("Model files", "*.pt")])
        if path:
            self.visible_model_entry.delete(0, tk.END)
            self.visible_model_entry.insert(0, path)
            self.visible_model_path = path

    def browse_infrared_model(self):
        path = filedialog.askopenfilename(filetypes=[("Model files", "*.pt")])
        if path:
            self.infrared_model_entry.delete(0, tk.END)
            self.infrared_model_entry.insert(0, path)
            self.infrared_model_path = path

    def browse_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if path:
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                messagebox.showerror("Error", "Selected video file cannot be opened.")
                cap.release()
                return
            cap.release()
            self.video_entry.delete(0, tk.END)
            self.video_entry.insert(0, path)
            self.video_path = path
            messagebox.showinfo("Success", "Video file selected successfully.")

    def load_model(self):
        model_type = self.model_type_var.get()
        model_path = self.visible_model_path if model_type == "Visible" else self.infrared_model_path

        if not model_path or not os.path.exists(model_path):
            messagebox.showerror("Error", f"Invalid {model_type} model path: {model_path}")
            return

        try:
            self.model = YOLO(model_path)
            messagebox.showinfo("Success", f"{model_type} model loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {str(e)}")

    def start_detection(self):
        if self.is_running:
            self.is_running = False
            return

        if not self.model:
            messagebox.showerror("Error", "Please load a model first.")
            return

        if not self.video_path or not os.path.exists(self.video_path):
            messagebox.showerror("Error", "Please select a valid video file.")
            return

        self.is_running = True
        threading.Thread(target=self.detect_video, daemon=True).start()

    def detect_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open video file.")
            self.is_running = False
            return

        # Prepare output video
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        model_type = self.model_type_var.get().lower()
        output_path = os.path.join(output_dir, f"output_{model_type}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(self.cap.get(3)), int(self.cap.get(4))))

        while self.is_running and self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()
            if not ret:
                break

            # Perform detection with lower confidence threshold
            results = self.model(frame, conf=0.2, verbose=False)
            annotated_frame = results[0].plot()

            # Check for drone detection
            drone_detected = False
            for box in results[0].boxes:
                cls_id = int(box.cls)
                class_name = self.model.names[cls_id]
                conf = float(box.conf)
                # Broaden class name matching and ensure confidence is met
                if class_name.lower() in ["drone", "uav"] and conf > 0.2:
                    drone_detected = True
                    break

            # Display alert text and play sound if drone detected
            if drone_detected:
                cv2.putText(
                    annotated_frame,
                    "Drone Detected!",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),  # Red color
                    2,
                )
                current_time = time.time()
                if current_time - self.last_alert_time > 1.0:  # 1-second cooldown
                    winsound.Beep(1000, 500)  # 1000 Hz, 500 ms
                    self.last_alert_time = current_time

            # Calculate and display FPS
            fps = 1 / (time.time() - start_time)
            cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write to output video
            out.write(annotated_frame)

            # Update GUI
            self.update_gui(annotated_frame)

        # Cleanup
        self.cap.release()
        out.release()
        self.is_running = False
        messagebox.showinfo("Success", f"Detection completed. Output saved to {output_path}")

    def update_gui(self, frame):
        # Convert frame to PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # Resize for display (maintain aspect ratio)
        max_size = (700, 400)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)
        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk  # Keep reference

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectionGUI(root)
    app.run()