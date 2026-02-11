# ADAS Lane Detection and Steering Assist

## Overview
This project is a real-time lane detection and steering assist system built using Python and OpenCV. It processes video input, detects lane boundaries, calculates the lane center, and estimates a steering angle to simulate basic ADAS behavior.

The system uses classical computer vision techniques and temporal smoothing to produce stable lane detection suitable for beginner-level ADAS research and internship portfolios.

---

## Features
- Real-time lane detection from video input  
- Canny edge detection  
- Region of Interest (ROI) masking  
- Hough Line Transform for lane extraction  
- Weighted averaging of lane lines  
- Temporal smoothing to reduce flickering  
- Lane center calculation  
- Steering angle estimation  
- Visual lane area overlay  
- Steering guidance visualization  

---

## System Pipeline

Description:

1. Convert frame to grayscale 
2. Apply Gaussian blur 
3. Detect edges using Canny 
4. Apply region of interest mask 
5. Detect lane lines using Hough Transform
6. Average and smooth lane lines 
7. Calculate lane center 
8. Estimate steering angle 
9. Overlay lane area and steering line

---

## Project Structure

```
Lane-Detection-ADAS/
│
├── main.py
├── utils.py
├── Vids/
│   └── testvideo2.mp4 and lane.webm.
└── README.md
```

---

## Output

The system displays:

- Detected lane lines  
- Filled lane area  
- Steering direction line  
- Steering angle value  

---

## Core Algorithms Used

Canny Edge Detection  
Hough Line Transform  
Weighted Line Averaging  
Temporal Smoothing  
Geometric Steering Estimation  

---

## Completed Tasks

- [x] Real-time lane detection  
- [x] Lane smoothing  
- [x] Steering angle estimation  
- [x] Lane area visualization  

---

## Future Improvements

- Add PID-based steering control  
- Integrate with CARLA simulator  
- Replace classical vision with deep learning  
- Add curvature estimation  
- Multi-lane detection  

---

## Technical Summary

Classical computer vision ADAS pipeline with real-time steering estimation using Python and OpenCV.

---

## Author

Yashwanth Raj  

---
