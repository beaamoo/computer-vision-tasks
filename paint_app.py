'''
Computer Vision Homework II
BCSAI ST24, IE University
Author: Beatrice Mossberg
Date: 2021-02-06
Description: This script defines a simple paint application using OpenCV to draw on a canvas using the mouse.
'''

import numpy as np
import cv2

# Define the PaintApp class
class PaintApp:
    # Initialize the Paint application with default parameters for the window, canvas, and drawing settings
    def __init__(self, window_name, canvas_size=(800, 800), background_color=(127, 127, 127), brush_color=(0, 255, 0), brush_size=5):
        self.window_name = window_name  
        self.canvas_size = canvas_size 
        self.background_color = background_color  
        self.brush_color = brush_color  
        self.brush_size = brush_size  
        self.canvas = np.ones((*canvas_size, 3), dtype="uint8") * np.array(background_color, dtype="uint8")  # Initialize the canvas with the background color
        self.drawing = False  # State to keep track of whether the mouse button is pressed for drawing
        self.last_position = None  # Last known position of the cursor for drawing lines
        
        cv2.namedWindow(window_name)  # Create a window for displaying the canvas
        cv2.setMouseCallback(window_name, self.handle_events)  # Set up a callback function to handle mouse events in the window

    # Define the event handler for mouse actions within the application window
    def handle_events(self, event, x, y, flags, param):
        # Check for mouse button press to start or stop drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:
                self.drawing = True
                self.last_position = (x, y)  # Start drawing from the current mouse position
            else:
                self.drawing = False
                self.last_position = None  # Reset the last position when stopping drawing
        # Draw a line from the last position to the current mouse position if the mouse is moving and drawing is enabled
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            cv2.line(self.canvas, self.last_position, (x, y), self.brush_color, self.brush_size)
            self.last_position = (x, y)  # Update the last position to the current position after drawing

    # Main loop to run the paint application
    def run(self):
        instructions = "Click to start/stop drawing, 'c' to clear, 's' to save, 'ESC' to exit"  # Instructions for the user
        while True:
            # Display the instructions on the canvas
            cv2.putText(self.canvas, instructions, (10, 790), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow(self.window_name, self.canvas)  # Show the current state of the canvas in the window
            key = cv2.waitKey(1) & 0xFF  # Wait for a key press
            
            # Clear the canvas if 'c' is pressed
            if key == ord('c'):
                self.canvas = np.ones((*self.canvas_size, 3), dtype="uint8") * np.array(self.background_color, dtype="uint8")
            # Save the current canvas to a file if 's' is pressed
            elif key == ord('s'):
                cv2.imwrite("painting.png", self.canvas)
            # Exit the loop and close the application if the ESC key is pressed
            elif key == 27:  # ESC key
                break
        
        cv2.destroyAllWindows()  # Close all OpenCV windows when done

# Check if this script is run as the main program and launch the paint application
if __name__ == "__main__":
    app = PaintApp("Paint")
    app.run()
