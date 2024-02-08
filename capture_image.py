"""
Computer Vision Assignment 1
Beatrice Mossberg
BCSAI - ST24

This script captures a single image from the webcam, 
displays it, prints the intensity values of the center pixel, 
and saves the image as captured_image.jpg
"""

import cv2
import numpy as np

# Initialize the webcam (0 or -1 to select the default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam 😔")
    exit()

# Capture a single frame
ret, frame = cap.read()

if ret:
    # Display the captured image
    cv2.imshow('Captured Image', frame)

    # Print pixel intensity values at a specific point (center of the image)
    height, width, _ = frame.shape
    center_pixel = frame[height // 2, width // 2]
    print("Center pixel intensity values (BGR):", center_pixel)

    # Save the frame as an image file
    cv2.imwrite('captured_image.jpg', frame)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Could not capture a frame 🙄")

# Release the webcam
cap.release()
