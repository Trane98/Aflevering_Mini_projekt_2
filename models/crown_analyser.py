"""
contains the variable of the crown analyser

* consider making this a class with functions to train the model and use the model.
"""

import numpy as np
import cv2
from joblib import load
import joblib
import pandas as pd


class CrownAnalyser: 
    def __init__(self): 
        self.kmeans = joblib.load("models\kmeans_model.joblib")
        self.svm_sift = joblib.load("models\SVM_SIFT_finde_kroner.joblib")
        self.scaler = joblib.load("models\SVM_SIFT_finde_kroner_scaler.joblib")

        #self.kmeans = load(r"C:\Program Files (x86)\2 Semester python work\Mini_projekt_AI_Systemer\Billeder\Program_AD\models\kmeans_model.joblib")
        #self.svm_sift = load(r"C:\Program Files (x86)\2 Semester python work\Mini_projekt_AI_Systemer\Billeder\Program_AD\models\SVM_SIFT_finde_kroner.joblib")
        #self.scaler = load(r"C:\Program Files (x86)\2 Semester python work\Mini_projekt_AI_Systemer\Billeder\Program_AD\models\SVM_SIFT_finde_kroner_scaler.joblib")


    def feature_extraction_SIFT_descriptors(self, image):
        """Udtrækker SIFT descriptors fra et billede"""

        # Sikrer korrekt format og størrelse
        if image.shape[-1] == 4:  # PNG med alfa
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        image = cv2.resize(image, (100, 100))

        # Konverter billedet til gråtoner
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if image is None:
            raise ValueError("Image is None.")

        # Vi har ikke brug for at finde keypoints, da vi kun er interesseret i descriptors
        _, descriptors = cv2.SIFT_create().detectAndCompute(image, None)
        return descriptors

    


    def classify_descriptors_with_model(self, kmeans, descriptors):
        """Klassificerer SIFT descriptors med KMeans og returnerer et normaliseret histogram"""

        n_clusters = kmeans.n_clusters

        if descriptors is None:
            # Hvis der ikke er nogen descriptors, returner en tom array
            return np.zeros(n_clusters, dtype=float)
        
        # Forudsig cluster-labels for descriptors
        labels = self.kmeans.predict(descriptors)

        # Samme metode brug som i træning: np.histogram og normalisering
        hist, _ = np.histogram(labels, bins=np.arange(n_clusters + 1))
        hist = hist / np.sum(hist) # Normalisering
        return hist
        #(Vi normalisere, da vi ikke er interesseret i hvor mange features der var, 
        # men hvordan de var fordelt)

    def extract_bovw_vector(self, image):
        """Udtrækker en BoVW-vektor fra et billede"""
        descriptors = self.feature_extraction_SIFT_descriptors(image)
        bovw_vector = self.classify_descriptors_with_model(self.kmeans, descriptors)
        return bovw_vector


    def predict_image_label(self, image):
        bovw_vector = self.extract_bovw_vector(image)

        # Genskab feature-navne
        feature_names = [f"Cluster_{i}" for i in range(len(bovw_vector))]

        # Lav dataframe med samme struktur som under træning
        bovw_df = pd.DataFrame([bovw_vector], columns=feature_names)

        bovw_vector_scaled = self.scaler.transform(bovw_df)
        prediction = self.svm_sift.predict(bovw_vector_scaled)
        return prediction[0]