<p align="center">
  <img src="https://i.imgur.com/gKLxJl9.png" width="600"/>
</p>

# DRONE-DETECTION-INTRUSION-ALERT

![Python](https://img.shields.io/badge/Python-3.10-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Model-green)
![MIT License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Colab-lightgrey)

# DRONE-DETECTION-INTRUSION-ALERT

This project implements a real-time drone detection and classification system using the Anti-UAV datasets (S300 and S410), powered by YOLOv8 and supported with a GUI for interactive deployment.

### 👥 Team Contribution

| Name            | Key Roles and Contributions                                                                                   |
|-----------------|----------------------------------------------------------------------------------------------------------------|
| **Li&nbsp;Kerui**       | YOLOv8 training and optimization, data preprocessing, mAP and inference time analysis, visualization.       |
| **Zhao&nbsp;Jichen**    | Project design, methodology writing, heatmap/confidence analysis, report integration and polishing.         |
| **Zhou&nbsp;Xingyu**    | Dataset split and management, YOLOv5 comparison, error analysis, visualization and presentation framework.   |
| **Thuta&nbsp;Zaw**      | Literature review, experiment logging, multilingual presentation materials and poster design.               |
| **Zhang&nbsp;Gaorui**   | GUI design and visualization output support, system reproducibility and testing.                            |

> All members participated in weekly discussions, documentation, and final presentation.  


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

## 📦 Dataset & Resources Download

Due to large file size, key resources are hosted externally via Google Drive:
- 📁 **S300 Dataset**  
  [🔗 Download Link](https://drive.google.com/drive/folders/1ktO5aHELg45Jj5dGWGw9rQlAsF5boMXM?usp=drive_link)

- 📁 **S410 Dataset**  
  [🔗 Download Folder](https://drive.google.com/drive/folders/1VLktm_N9jHb3UD0dQCLKmJG8OQWavBIv?usp=drive_link)

> ⚠️ Some folders are large. Please download selectively as needed.

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

## 🙌 Acknowledgements

- **Dataset**: [Anti-UAV Benchmark (ECCV 2020)](https://github.com/ZhaoJ9014/Anti-UAV)  
  We sincerely thank the authors of the Anti-UAV dataset for providing a valuable resource for UAV detection and tracking research.
  
- **Model Framework**: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
