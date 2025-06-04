
# DRONE-DETECTION-INTRUSION-ALERT

This project implements a real-time drone detection and classification system using the Anti-UAV datasets (S300 and S410), powered by YOLOv8 and supported with a GUI for interactive deployment.

## 📁 Project Structure

```
DRONE-DETECTION-INTRUSION-ALERT/
│  gui_detect.py
│  gui_interface.png
│  model_notes.txt
│  requirements.txt
│  S300 trained.ipynb
│  S410 trained.ipynb
│  
├─Dataset/
│  ├─Anti-UAV-RGBT-Processed/
│  │  ├─images/ (train, val, test)
│  │  └─labels/ (train, val, test)
│  └─Anti-UAV410-Processed/
│     ├─images/ (train, val, test)
│     └─labels/ (train, val, test)
│
├─flowercharts/
│  ├─Detected_System_Flowchart.png
│  ├─S300_Flowchart.png
│  └─S410_Flowchart.png
│
├─S300_Result/
├─S410_Result/
├─weights(S300)/
└─weights(S410)/
```

## 🧠 Model Overview

- **S300 Dataset**: RGBT-based Anti-UAV dataset with infrared and visible images.
- **S410 Dataset**: Higher resolution UAV dataset with detailed annotations.
- Models trained include YOLOv8 with `.pt` and `.onnx` exported weights.
- Confusion matrices, mAP curves, and loss curves are available in result folders.

## 🚀 Getting Started

### 1. Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. GUI Detection

To launch the GUI interface:

```bash
python gui_detect.py
```

This opens an interface allowing users to upload images or videos and run detection using trained models.

## 📊 Dataset Description

- The datasets are split into train/val/test sets under both RGBT and 410 variants.
- Each sample includes bounding boxes of UAVs in `.txt` format (YOLO format).
- `dataset_description.txt` provides metadata and task context.

## 🏋️‍♂️ Training

Training notebooks:

- `S300 trained.ipynb` for Anti-UAV-RGBT data.
- `S410 trained.ipynb` for Anti-UAV410 data.

Results and logs are stored under `S300_Result/` and `S410_Result/` respectively.

## 🧾 Model Notes

Additional observations and configuration tips are documented in `model_notes.txt`.

