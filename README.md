# ADAS Lane Detection and Steering Assist

## Overview
This project is a **real-time ADAS lane detection and steering assist system** built with Python and OpenCV. It processes video input, detects lane boundaries, calculates the lane or road center, and estimates a steering angle to simulate basic ADAS behavior.

The system integrates **classical lane detection** with a **fallback road segmentation mode** to handle complex environments such as roads with faded or missing lane markings. Temporal smoothing and FPS synchronization ensure **stable and realistic steering guidance**, making this suitable for ADAS research and internship portfolios.

---

## Features
- Real-time lane detection from video input  
- Canny edge detection  
- Region of Interest (ROI) masking  
- Hough Line Transform for lane extraction  
- Weighted averaging of lane lines  
- Temporal smoothing for stability  
- Lane center calculation  
- Steering angle estimation  
- Visual lane area overlay  
- Steering guidance visualization  
- Automatic fallback to **road detection** when lane markings are missing  
- Road center estimation using color-based segmentation  
- Dual-mode ADAS pipeline (**Lane Mode + Road Mode**)  
- Constant FPS synchronization with input video  
- Real-time FPS counter display  

---

## System Pipeline

**Lane Detection Mode:**  
1. Convert frame to grayscale  
2. Apply Gaussian blur  
3. Detect edges using Canny  
4. Apply region of interest mask  
5. Detect lane lines using Hough Transform  
6. Average and smooth lane lines  
7. Calculate lane center  
8. Estimate steering angle  
9. Overlay lane area and steering guidance  

**Road Fallback Mode (when lane markings are missing):**  
1. Apply color-based segmentation to detect drivable area  
2. Estimate road center  
3. Compute steering angle from road center  
4. Overlay road guidance path  

**General:**  
- Synchronize processing speed with video FPS  
- Display steering angle and FPS counter  

---

## Project Structure


## Project Structure

```
Lane-Detection-ADAS/
│
├── main.py
├── utils.py
├── Vids/
│   └── testvideo2.mp4, lane.webm, 2 No-LaneVideo.mp4.
└── README.md
```

---


---

## Output
The system displays:  
- Detected lane lines  
- Filled lane area  
- Steering direction line  
- Steering angle value  
- Road-mode guidance when lane lines are missing  
- Real-time FPS counter  

---

## Core Algorithms Used
- Canny Edge Detection  
- Hough Line Transform  
- Weighted Line Averaging  
- Temporal Smoothing  
- Color-Based Road Segmentation  
- Geometric Steering Estimation  

---

## Completed Tasks
- Real-time lane detection  
- Lane smoothing  
- Steering angle estimation  
- Lane area visualization  
- Road fallback detection for no-marking roads  
- Dual-mode steering logic  
- FPS-synchronized processing  

---

## Future Improvements
- Replace classical vision with deep learning lane segmentation  
- Add vehicle, pedestrian, and obstacle detection  
- Integrate with CARLA simulator  
- Implement PID-based steering control  
- Add curvature estimation  
- Sensor fusion with LiDAR or radar  

---

## Technical Summary
**Dual-mode classical computer vision ADAS pipeline** with real-time lane detection, road segmentation fallback, and steering estimation using Python and OpenCV.

---

## Author
**Yashwanth Raj**

