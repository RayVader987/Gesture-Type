# GestureType

## Overview

This project implements a virtual keyboard controlled by hand gestures using computer vision. It leverages the Mediapipe library for real-time hand tracking and OpenCV for rendering a graphical keyboard interface. Users can type by hovering their index finger over keys detected on screen, with hover duration triggering key presses.

The system supports:
- Real-time hand tracking and gesture-based key selection  
- A full keyboard layout including alphabets, numbers, symbols, and control keys (e.g., BACKSPACE, ENTER, CAPS LOCK)  
- Launching common applications and websites through typed commands  
- Visual feedback including key highlighting, hover timers, and typed text display  

## Features

- Accurate single-hand tracking for keyboard interaction  
- Hover-based key press detection with adjustable delay  
- Dynamic CAPS LOCK toggle  
- Support for launching desktop and web applications by typing and pressing ENTER  
- On-screen display of typed text with automatic line wrapping  
- Ability to close active windows via gesture command  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/RayVader987/Gesture-Type.git
   cd Gesture-Type
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Connect a webcam to your computer.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Use your index finger in front of the webcam to hover over virtual keys displayed on screen.
4. Hold the finger steady over a key for 1 second to "press" it.
5. Type commands like notepad, google, or youtube followed by ENTER to launch corresponding applications or websites.
6. Use special keys like CAPS, BACKSPACE, CLEAR, SPACE, ENTER, and CLOSE as needed.
7. Press the ESC key to exit the application.

## Dependencies
1. Python 3.7+
2. OpenCV (opencv-python)
3. Mediapipe
4. PyAutoGUI
5. PyGetWindow
