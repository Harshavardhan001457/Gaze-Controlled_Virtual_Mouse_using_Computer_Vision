# Gaze-Controlled Virtual Mouse using Computer Vision

##  Overview

This project implements a **real-time gaze-controlled virtual mouse** that allows a user to control the system cursor using only **eye movements and blink gestures**, captured through a standard webcam.

The system translates **eye gaze direction** into smooth cursor movement and uses **blink patterns** (double / triple blink) and **gaze hold** as mouse click actions.
All processing is done in real time using **classical computer vision logic combined with MediaPipe’s facial landmark tracking**, without relying on any deep learning–based tracking APIs.


##  Core Concepts Used

### 1. Face & Eye Landmark Detection (MediaPipe Face Mesh)

I used **MediaPipe Face Mesh** to detect **468 facial landmarks** in real time.
From these landmarks, only the **eye region landmarks** are selected for gaze and blink analysis.

Why MediaPipe?

* Highly optimized for real-time performance
* Robust to head movement and lighting changes
* Provides normalized landmark coordinates independent of face size



### 2. Gaze Direction Estimation (Relative Geometry)

Instead of using raw pixel positions, gaze direction is computed using **relative landmark ratios**:

* The **iris center** position is compared with the **eye corner landmarks**
* Horizontal and vertical offsets determine:

  * LEFT
  * RIGHT
  * UP
  * DOWN
  * CENTER (dead-zone)

This ratio-based approach ensures robustness across users and camera distances.



### 3. Blink Detection using EAR (Eye Aspect Ratio)

Blink detection is implemented using the **Eye Aspect Ratio (EAR)** concept.

**EAR formula:**

```
EAR = (vertical distances) / (horizontal distance)
```

Key ideas:

* EAR drops sharply when the eye closes
* EAR is stable when the eye is open
* We detect a blink only when the eye transitions from **open → closed → open**

To improve stability:

* EAR is computed for **both eyes**
* A **temporal moving average** smooths noise
* Blinks are counted using a **state-based approach**, not frame-based counting



### 4. Gesture Interpretation (Temporal Logic)

Blink gestures are interpreted using **time windows**:
```
 Gesture       Logic                                   

 Double Blink  2 blinks within a short interval        
 Triple Blink  3 blinks within the same blink sequence 
 Gaze Hold     CENTER gaze maintained for ≥ 3 seconds  
```

The system waits for the **blink sequence to finish** before deciding the action, ensuring reliable triple-blink detection.


### 5. Cursor Control (System Interaction)

Mouse actions are performed using **PyAutoGUI**:

* Relative cursor movement for smooth control
* Left click → Double blink
* Right click → Triple blink
* Select action → Gaze hold

Movement is rate-limited to avoid jitter and CPU overload.



##  System Pipeline

1. Capture webcam frame (OpenCV)
2. Detect face landmarks (MediaPipe Face Mesh)
3. Extract eye landmarks
4. Compute gaze direction
5. Compute EAR and detect blink events
6. Interpret gestures (double / triple blink, gaze hold)
7. Control mouse cursor (PyAutoGUI)
8. Visualize gaze indicators and system state


## 🗂️ Project Structure

```
gaze-controlled-virtual-mouse/
│
├── main.py
├── eye_tracker.py
├── mouse_controller.py
├── utils.py
├── face_landmarker.task
├── Demo.mp4
└── README.md
```



##  Technologies Used

* **Python**
* **OpenCV** – video capture & visualization
* **MediaPipe (Tasks API)** – facial landmark detection
* **NumPy** – numerical computations
* **PyAutoGUI** – system mouse control


##  Conclusion

This project demonstrates how **classical computer vision principles**, combined with robust landmark tracking, can be used to build a **practical human–computer interaction system**.
