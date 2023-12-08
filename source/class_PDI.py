import os
import cv2 as cv
import datetime
import numpy as np
import time

class Processamentos:
     
    def __init__(self):
        
        pass


    def apply_gaussian_blur(self, image, kernel_size):

        return cv.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def calculate_gradients(self, image):

        gray = image
        gradient_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)
        gradient_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)
        
        magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        direction = np.arctan2(gradient_y, gradient_x)
        
        return magnitude, direction

    def apply_non_max_suppression(self, magnitude, direction):

        height, width = magnitude.shape
        suppressed = np.zeros_like(magnitude)
        
        angle = np.degrees(direction) % 180
        
        for i in range(1, height - 1):
            
            for j in range(1, width - 1):

                q1 = 0
                q2 = 0
                
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):

                    q1 = magnitude[i, j+1]
                    q2 = magnitude[i, j-1]

                elif 22.5 <= angle[i, j] < 67.5:
                    
                    q1 = magnitude[i-1, j+1]
                    q2 = magnitude[i+1, j-1]

                elif 67.5 <= angle[i, j] < 112.5:

                    q1 = magnitude[i-1, j]
                    q2 = magnitude[i+1, j]

                elif 112.5 <= angle[i, j] < 157.5:

                    q1 = magnitude[i-1, j-1]
                    q2 = magnitude[i+1, j+1]
                
                if (magnitude[i, j] >= q1) and (magnitude[i, j] >= q2):

                    suppressed[i, j] = magnitude[i, j]
        
        return suppressed

    def apply_double_threshold(self, image, low_threshold, high_threshold):

        strong_edges = (image >= high_threshold)
        weak_edges = (image >= low_threshold) & (image < high_threshold)

        return strong_edges, weak_edges

    def edge_tracking(self, strong_edges, weak_edges):

        height, width = strong_edges.shape

        edge_image = np.zeros((height, width), dtype=np.uint8)
        edge_image[strong_edges] = 255
        
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for i in range(1, height - 1):

            for j in range(1, width - 1):

                if weak_edges[i, j]:

                    for dx, dy in neighbors:

                        if strong_edges[i + dx, j + dy]:
                            edge_image[i, j] = 255

                            break
        
        return edge_image


    def processamento_de_imagem(self, input_image, low_thresh, max_thresh):

        blurred_image = self.apply_gaussian_blur(input_image, kernel_size = 5)

        magnitude, direction = self.calculate_gradients(blurred_image)

        suppressed_image = self.apply_non_max_suppression(magnitude, direction)

        strong_edges, weak_edges = self.apply_double_threshold(suppressed_image, low_threshold = low_thresh, high_threshold = max_thresh)

        edge_image = self.edge_tracking(strong_edges, weak_edges)

        return edge_image 
        