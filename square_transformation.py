'''
Computer Vision Homework III
BCSAI ST24, IE University
Author: Beatrice Mossberg
Date: 2021-02-06
Description: This script defines a simple visualizer for comparing different transformations on a square using OpenCV.
'''

import numpy as np
import cv2

# Define the Visualizer class
class Visualizer:
    def __init__(self, size=(800, 1200), length=100, pos=(50, 50)):
        self.canvas = np.zeros((*size, 3), dtype=np.uint8) # Initialize the canvas with a black background
        self.side_length = length # Length of the square
        self.pos = np.array(pos) # Position of the square
        self.colors = {'Original': (255, 255, 255), 'Translation': (255, 0, 0), 'Euclidean': (0, 255, 0), 'Affine': (0, 0, 255), 'Homography': (0, 255, 255)}
        self.space_x, self.space_y = 150, 250  # Adjust as necessary to fit names

    # Draw a square on the canvas
    def draw(self, points, color):
        cv2.polylines(self.canvas, [np.int32(points)], True, color, 2)

    # Apply a transformation matrix to a square
    def transform(self, matrix):
        square = np.array([[0, 0], [self.side_length, 0], [self.side_length, self.side_length], [0, self.side_length]])
        return cv2.perspectiveTransform(np.float32([square]), matrix)[0] if matrix.shape[0] == 3 else cv2.transform(np.float32([square]), matrix)[0]

    # Define the transformations to be applied to the square
    def transformations(self):
        square = np.array([[0, 0], [self.side_length, 0], [self.side_length, self.side_length], [0, self.side_length]], dtype=np.float32)
        src = square[:3] # Original points
        dest_points_adjustment = np.array([[0, 0.3], [0, -0.3], [0.3, 0]]) * self.side_length # Adjusted points
        dst = np.array([
            [src[0][0] + dest_points_adjustment[0][0], src[0][1] + dest_points_adjustment[0][1]],
            [src[1][0] + dest_points_adjustment[1][0], src[1][1] + dest_points_adjustment[1][1]],
            [src[2][0] + dest_points_adjustment[2][0], src[2][1] + dest_points_adjustment[2][1]]
        ], dtype=np.float32)

        # Return the transformation matrices
        return [
            np.eye(3),  # Original
            np.float32([[1, 0, self.side_length / 2], [0, 1, self.side_length], [0, 0, 1]]),  # Translation
            np.vstack([cv2.getRotationMatrix2D((self.side_length / 2, self.side_length / 2), 45, 1), [0, 0, 1]]),  # Euclidean
            cv2.getAffineTransform(src, dst),  # Affine
            cv2.findHomography(square, square + np.array([[0.2, -0.1], [-0.2, 0.1], [0.1, 0.2], [-0.1, -0.2]]) * self.side_length)[0]  # Homography
        ]

    # Visualize the transformations on the canvas
    def visualize(self):
        cell_width = self.canvas.shape[1] // len(self.colors)
        for i, (name, matrix) in enumerate(zip(self.colors, self.transformations())):
            pos = np.array([cell_width * i + self.space_x // 2, self.space_y])
            square = self.transform(matrix) + pos
            self.draw(square, self.colors[name])
            cv2.putText(self.canvas, name, (pos[0], 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, self.colors[name], 1)
        
        # Instructions at the bottom
        cv2.putText(self.canvas, "Press any key to exit", (10, self.canvas.shape[0] - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
        cv2.imshow("Transformations", self.canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Run the visualizer
if __name__ == "__main__":
    Visualizer().visualize()
