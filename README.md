# QCar-YOLOv5-Perception-Framework
A real-time AI perception pipeline for QLabs QCar capable of detecting traffic signs, pedestrians, cones, and traffic lights using YOLOv5 and OpenCV.
This repository provides a complete perception pipeline for autonomous driving experiments in the Quanser QLabs simulation environment. It integrates:

- Real-time camera streaming
- YOLOv5 object detection
- ONNX accelerated inference
- Multithreaded processing
- Manual QCar control
- Dataset collection utilities
- Dataset preprocessing scripts

---

# Features

- Real-time YOLOv5 object detection
- ONNX and PyTorch inference support
- GPU and CPU inference pipelines
- Multithreaded vision processing
- Smooth OpenCV visualization
- Real-time bounding box rendering
- Keyboard-based vehicle control
- QCar hardware integration
- Traffic object recognition
- Custom dataset collection system
- Dataset shuffling and renaming utility
- Optimized perception pipeline for QLabs

---

# Detected Classes

The trained model detects:

- Cone
- Green Light
- Pedestrian
- Red Light
- Roundabout
- Stop Sign
- Yellow Light
- Yield Sign

---

# Repository Structure

```bash
.
├── main_detector.py
├── qcar_detector.py
├── qcar_detector_onnx.py
├── data_collection.py
├── qlabs_rename.py
├── runs/
│   └── acc/
│       └── yolov5s_1/
│           └── weights/
│               ├── best.pt
│               └── best.onnx
└── README.md
```

---

# System Architecture

```text
QCar Camera Feed
        ↓
 Frame Acquisition
        ↓
Background YOLOv5 Inference
        ↓
Object Detection
        ↓
Bounding Box Rendering
        ↓
OpenCV Visualization
        ↓
QCar Control Output
```

---

# Script Descriptions

# 1. main_detector.py

## Overview

Main perception and control script for the QCar.

This script:
- Initializes QCar hardware
- Starts front camera streaming
- Runs YOLOv5 inference in a background thread
- Displays real-time detections
- Handles manual driving control
- Renders OpenCV HUD overlays

---

## Key Features

### Multithreaded Vision Pipeline

Uses separate threads for:
- Camera streaming
- Hardware control
- YOLO inference

This keeps the display smooth while inference runs asynchronously.

---

### Real-Time Visualization

Displays:
- Bounding boxes
- Confidence scores
- Class labels
- Steering/throttle values
- Detection count

---

### Keyboard Controls

| Key | Action |
|------|---------|
| Up Arrow | Increase throttle |
| Down Arrow | Decrease throttle |
| Left Arrow | Steer left |
| Right Arrow | Steer right |
| Q | Quit system |

---

### Performance Optimizations

- Model warmup before runtime
- Lock-based synchronization
- Lightweight rendering pipeline
- Fast detection sharing between threads

---

# 2. qcar_detector.py

## Overview

PyTorch-based YOLOv5 inference module.

This script:
- Loads the `.pt` YOLOv5 model
- Preprocesses frames
- Runs inference
- Applies Non-Maximum Suppression (NMS)
- Draws bounding boxes
- Returns structured detection data

---

## Detection Pipeline

```text
Input Frame
    ↓
Letterbox Resize
    ↓
Tensor Conversion
    ↓
YOLOv5 Inference
    ↓
Non-Maximum Suppression
    ↓
Bounding Box Scaling
    ↓
Visualization + Detection Output
```

---

## Key Features

- Automatic GPU/CPU selection
- OpenCV integration
- Dynamic resizing
- Bounding box annotation
- Structured detection outputs

---

# 3. qcar_detector_onnx.py

## Overview

ONNX-accelerated YOLOv5 detector.

This version provides:
- Faster CPU inference
- Lightweight deployment
- Reduced latency
- Better runtime efficiency

---

## Recommended Usage

Use this version when:
- Running on CPU-only systems
- Needing lower latency
- Deploying lightweight inference pipelines

---

# 4. data_collection.py

## Overview

Interactive dataset collection tool for generating custom training datasets directly from the QCar camera feed.

This script allows users to manually drive the QCar and capture labeled driving scenes in real time.

---

## Key Features

### Real-Time Dataset Capture

- Saves high-resolution images from the QCar front camera
- Captures snapshots instantly using the spacebar
- Stores images automatically with timestamped filenames

---

### Visual Capture Feedback

After each capture:
- Displays “SNAPSHOT SAVED”
- Shows a thumbnail preview
- Updates image counter in real time

---

### Driving Controls

| Key | Action |
|------|---------|
| Up Arrow | Increase throttle |
| Down Arrow | Decrease throttle |
| Left Arrow | Steer left |
| Right Arrow | Steer right |
| Space | Capture image |
| Q | Quit |

---

### Dataset Storage

Captured images are stored inside:

```bash
dataset_collection/
```

Example:

```text
img_20250805_142301_123456.jpg
```

---

## Purpose

Used for:
- Building custom object detection datasets
- Collecting QLabs driving scenes
- Capturing traffic sign data
- Training YOLOv5 models

---

# 5. qlabs_rename.py

## Overview

Dataset preprocessing utility for image organization.

This script:
- Finds all dataset images
- Randomly shuffles them
- Renames them sequentially

---

## Example Output

```text
000001.jpg
000002.jpg
000003.jpg
```

---

## Key Features

- Prevents filename conflicts
- Supports multiple image formats
- Randomized dataset ordering
- Sequential naming for training consistency

---

## Supported Formats

JPG, JPEG, PNG, BMP, WEBP

---

# GPU Installation Setup

## Clone YOLOv5

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
pip install keyboard
```

---

## Reinstall PyTorch with CUDA Support

```bash
pip uninstall torch torchvision -y
```

Install CUDA-compatible PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

This command installs:
- PyTorch 2.7.0
- CUDA 12.6 support

Compatible with:
- Python 3.9+

If using another CUDA version:
- Check your CUDA version
- Visit the PyTorch documentation
- Use the matching `index-url`

---

# Verify CUDA Installation

Run:

```python
import torch

print(torch.__version__)
print(torch.cuda.is_available())
print(torch.version.cuda)
print(torch.cuda.get_device_name(0))
```

Expected output:

```text
2.7.0+cu126
True
12.6
NVIDIA GPU NAME
```

---

# Using This Project

## Step 1 — Clone Your Repository

```bash
git clone https://github.com/myltiplex1/QCar-YOLOv5-Perception-Framework.git
```

---

## Step 2 — Copy Files Into YOLOv5

Copy the following files from your repository:

```text
main_detector.py
qcar_detector.py
runs/
```

Paste them inside the YOLOv5 folder.

---

## Model Location

The trained model can be found at:

```text
runs/acc/yolov5s_1/weights/
```

Files:
- best.pt
- best.onnx

---

# Running the System

## PyTorch Version

Ensure:

```python
from qcar_detector import load_model, infer_on_frame
```

Then run:

```bash
python3 main_detector.py
```

---

## ONNX Version

Replace import with:

```python
from qcar_detector_onnx import load_model, infer_on_frame
```

Then run:

```bash
python3 main_detector.py
```

---

# Performance Notes

## ONNX Version

Advantages:
- Faster CPU inference
- Lower latency
- Better deployment efficiency

---

## PyTorch Version

Advantages:
- Better GPU acceleration
- Easier debugging
- More flexible training workflow

---

# Future Improvements

- Autonomous braking
- Traffic light decision making
- Lane detection integration
- Object tracking
- Depth estimation
- Sensor fusion
- ROS2 support
- TensorRT optimization
- Full autonomous navigation

---

# Demo

Add screenshots or GIFs here.

---

# Author

Enoch Soyinka

AI/Robotics Engineer focused on:
- Autonomous systems
- Computer vision
- Embedded AI
- Intelligent robotics

---

# License

MIT License
