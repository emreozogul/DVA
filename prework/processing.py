import cv2
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import sys

# Calculate the features of a contour
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

# Process an image and return the features and contoured image
def process_image(image_path, scale_factor):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error: Unable to load image '{image_path}'")
        return None, None
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
        contoured_image = cv2.drawContours(image.copy(), [largest_contour], -1, (0, 255, 0), 2)
        area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity = calculate_features(largest_contour, scale_factor)
        particle_count = count_particles(image)

        return (area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count), contoured_image
    else:
        return None, None
    
# Process 4x images and return the features and contoured images
def process_images_4x(image_dir, scale_factor):
    image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('.tif', '.jpg', '.png')) and not img.startswith('.')]
    features_4x = []
    contoured_images_4x = []

    for path in image_paths:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Error: Unable to load image '{path}'")
        edges = cv2.Canny(image, 30, 120)
        kernel = np.ones((11, 11), np.uint8)
        closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=3)
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            contoured_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(contoured_image, [largest_contour], -1, (0, 255, 0), 3)
            features = calculate_features(largest_contour, scale_factor)
            particle_count = count_particles_4x(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
            features_4x.append(features + (particle_count,))
            contoured_images_4x.append(contoured_image)
    return features_4x, contoured_images_4x, [os.path.basename(path) for path in image_paths]

# Count the number of particles in an image
def count_particles(image, min_area=100, max_area=5000, circularity_thresh=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    particle_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter > 0 else 0

            if circularity >= circularity_thresh:
                particle_count += 1

    return particle_count

def count_particles_4x(image, min_area=100, max_area=2500, circularity_thresh=0.3):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    particle_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter > 0 else 0

            if circularity >= circularity_thresh:
                particle_count += 1

    return particle_count

def write_features_to_csv_mm(features, image_names, output_dir, target_values):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_spheroid_features.csv"
    csv_file_path = os.path.join(output_dir, csv_file_name)
    
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Roundness', 'Aspect_Ratio', 'Solidity', 'Convexity', 'Particle_Count', 'Target']    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i, (feature, _) in enumerate(features):
            image_name = image_names[i]
            if feature:  # Check if there's a valid feature tuple
                writer.writerow({
                    'Image_Name': image_name, 
                    'Area_mm2': feature[0],
                    'Perimeter_mm': feature[1], 
                    'Diameter_mm': feature[2],
                    'Roundness': feature[3],
                    'Aspect_Ratio': feature[4],
                    'Solidity': feature[5],
                    'Convexity': feature[6],
                    'Particle_Count': feature[7],
                    'Target': 'Extremely Death'
                })
    return csv_file_path

def write_features_to_csv_4x(features, image_names, output_dir, target_values_4x=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_4x_spheroid_features.csv"
    csv_file_path = os.path.join(output_dir, csv_file_name)
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Roundness', 'Aspect_Ratio', 'Solidity', 'Convexity', 'Particle_Count', 'Target']    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for feature, image_name in zip(features, image_names):
             if image_name in image_names and image_names.index(image_name) < len(target_values_4x):
                target_values = target_values_4x[image_names.index(image_name)]
             else:
                target_values = None

             writer.writerow({
                'Image_Name': image_name, 
                'Area_mm2': feature[0],
                'Perimeter_mm': feature[1], 
                'Diameter_mm': feature[2],
                'Roundness': feature[3],  # Add roundness to the CSV
                'Aspect_Ratio': feature[4],
                'Solidity': feature[5],
                'Convexity': feature[6],
                'Particle_Count': feature[7],
                'Target': 'Extremely Death'
            })
    return csv_file_path

# Set parameters for image processing.    
scale_factor = 0.0786

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the current directory
spheroid_image_dir = os.path.join(current_dir, 'assets', 'images')
spheroid_image_dir_4x = os.path.join(current_dir, 'assets', 'images4x')
output_dir = os.path.join(current_dir, 'data')

# Check if the directory exists
if os.path.exists(spheroid_image_dir):
    image_names = os.listdir(spheroid_image_dir)
else:
    print(f"The directory '{spheroid_image_dir}' does not exist.")

spheroid_features_mm = []

target_values_4x = ""

target_values = ""

# Process 4x images and write the features to a CSV file.
features_4x, contoured_images_4x, image_names_4x = process_images_4x(spheroid_image_dir_4x, scale_factor)
csv_file_path_4x = write_features_to_csv_4x(features_4x, image_names_4x, output_dir, target_values_4x)
print(f"4x features CSV file saved to: {csv_file_path_4x}")

# Process each image and store the features in a list.
for img_name in image_names:
    img_path = os.path.join(spheroid_image_dir, img_name)
    features, contoured_image = process_image(img_path, scale_factor) 
    spheroid_features_mm.append((features, contoured_image)) 

# Write the features to a CSV file and display the results.
csv_file_path_mm = None
if len(spheroid_features_mm) == len(image_names) and spheroid_features_mm:
    csv_file_path_mm = write_features_to_csv_mm(spheroid_features_mm, image_names, output_dir, target_values)
    print(f"CSV file saved to: {csv_file_path_mm}")

    df = pd.read_csv(csv_file_path_mm)
    print(df[['Image_Name', 'Area_mm2','Perimeter_mm', 'Diameter_mm', 'Target']])

for i, (feature, contoured_image) in enumerate(spheroid_features_mm):
    img_name = image_names[i]
    original_img_path = os.path.join(spheroid_image_dir, img_name)
    original_img = cv2.imread(original_img_path, cv2.IMREAD_UNCHANGED)

    if original_img is None:
        print(f"Error: Unable to load original image '{original_img_path}'")
        continue

    if contoured_image is None:
        print(f"Error: Contoured image is None for '{img_name}'")
        continue
 
    plt.figure(figsize=(12, 6))
    original_img = cv2.imread(os.path.join(spheroid_image_dir, img_name), cv2.IMREAD_UNCHANGED)
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.title(f'Original Image - {img_name}')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(contoured_image, cv2.COLOR_BGR2RGB))
    plt.title('Processed Image')
    plt.axis('off')

    plt.show()

#Show 4x images with contours drawn on them
for i, contoured_image in enumerate(contoured_images_4x):
    img_name = image_names_4x[i]
    original_img_path = os.path.join(spheroid_image_dir_4x, img_name)
    original_img = cv2.imread(original_img_path, cv2.IMREAD_UNCHANGED)

    if original_img is None:
        print(f"Error: Unable to load original image '{original_img_path}'")
        continue

    if contoured_image is None:
        print(f"Error: Contoured image is None for '{img_name}'")
        continue

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(os.path.join(spheroid_image_dir_4x, img_name), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB))
    plt.title(f'Original Image - {img_name}')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(contoured_image, cv2.COLOR_BGR2RGB))
    plt.title('Processed Image')
    plt.axis('off')

    plt.show()
    

# Run the model.py file
# python_path = sys.executable
# model_py_path = os.path.join('prework', 'model.py')
#
# if os.path.isfile(model_py_path):
#     try:
#         print("Running the model.py file...")
#         subprocess.run([python_path, model_py_path, csv_file_path_mm], check=True)
#         print("model.py file executed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred while running the model.py file: {e}")
# else:
#     print("Model.py file not found.")