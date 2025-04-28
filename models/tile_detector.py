"""
contains the variable of the tile detector

* consider making this a class with functions to train the model and use the model.
"""

import os
import cv2
import pandas as pd
import numpy as np
from skimage.feature import hog
import matplotlib.pyplot as plt
import joblib


class TileDetector: 
    def __init__(self): 
        self.model = joblib.load('svm_model_final.joblib')
        #self.model = joblib.load("Program_AD\models\svm_model_lin_bal.joblib")
    
    def extract_hog_features_from_image(self, image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray_image, (100, 100))
        features = hog(resized_image,
                       orientations=orientations,
                       pixels_per_cell=pixels_per_cell,
                       cells_per_block=cells_per_block,
                       visualize=False)
        return features

    def extract_hsv_features_from_image(self, image):
        img = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h = np.median(hsv[:, :, 0])
        s = np.median(hsv[:, :, 1])
        v = np.median(hsv[:, :, 2])
        return [h, s, v]

    def preprocess_image(self, image):
        """
        Takes an image, loads it, and extracts combined HOG+HSV features.
        """
        if image is None:
            raise ValueError("The image could not be loaded correctly.")
        hog_features = self.extract_hog_features_from_image(image)
        hsv_features = self.extract_hsv_features_from_image(image)
        combined_features = np.hstack([hog_features, hsv_features])
        return combined_features.reshape(1, -1)  # Shape: (1, n_features)

    def predict(self, image):
        """
        Predicts the tile class of a given image path using the trained SVM model.
        """
        features = self.preprocess_image(image)
        prediction = self.model.predict(features)  
        return prediction[0]