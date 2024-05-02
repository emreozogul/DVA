import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


def calculate_features(contour, scale_factor):
    area_pixels = cv2.contourArea(contour)
    perimeter_pixels = cv2.arcLength(contour, True)
    (_, _), radius_pixels = cv2.minEnclosingCircle(contour)
    # Calculate the roundness of the contour    
    roundness = 4 * np.pi * area_pixels / (perimeter_pixels ** 2)
    area_mm2 = area_pixels * scale_factor ** 2
    perimeter_mm = perimeter_pixels * scale_factor
    diameter_mm = 2 * radius_pixels * scale_factor
    # Calculate the aspect ratio of the minimum bounding rectangle of the contour   
    rect = cv2.minAreaRect(contour)
    width, height = rect[1][0], rect[1][1]
    aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0
    # Calculate the solidity and convexity of the contour
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = area_pixels / hull_area if hull_area > 0 else 0
    hull_perimeter = cv2.arcLength(hull, True)
    convexity = perimeter_pixels / hull_perimeter if hull_perimeter > 0 else 0

    return area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity

def process_image_10x(image_path, scale_factor=0.0786):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity = calculate_features(largest_contour, scale_factor)
        particle_count = count_particles(image)
        return area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count
    else:
        return None, None
    
# Process 4x images and return the features and contoured images
def process_image_4x(image_path, scale_factor=0.1965):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 30, 120)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=3)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity  = calculate_features(largest_contour, scale_factor)
        particle_count = count_particles_4x(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
        return area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count

    else:
        return None, None


def count_particles(image, min_area=100, max_area=5000, circularity_thresh=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 120)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    particle_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter > 0 else 0

            if circularity >= circularity_thresh:
                particle_count += 1

    return particle_count

def count_particles_4x(image, min_area=50, max_area=2500, circularity_thresh=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 120)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    particle_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter > 0 else 0

            if circularity >= circularity_thresh:
                particle_count += 1
