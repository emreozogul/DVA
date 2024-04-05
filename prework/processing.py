import cv2
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import sys

# Calculate features 
def calculate_features(contour, scale_factor):
    # Calculate area in square millimeters.
    area_mm2 = cv2.contourArea(contour) * (scale_factor)**2
    perimeter_mm = cv2.arcLength(contour, True) * (scale_factor)
    (x, y), radius_pixels = cv2.minEnclosingCircle(contour)
    diameter_mm = 2 * radius_pixels * (scale_factor)
    return area_mm2, perimeter_mm, diameter_mm

# Process an image to extract the largest contour and its features.
def process_image(image_path, scale_factor):
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
        # Draw the largest contour on the original image.
        contoured_image = cv2.drawContours(image.copy(), [largest_contour], -1, (0, 255, 0), 2)
        area_mm2, perimeter_mm, diameter_mm = calculate_features(largest_contour, scale_factor)
        particle_count = count_particles(image)
        return (area_mm2, perimeter_mm, diameter_mm, particle_count), contoured_image  
    else:
        return None, None
   
def process_images_4x(image_dir, scale_factor_4x):
    image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith('.tif')]
    images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in image_paths]

    low_threshold = 30
    high_threshold = 100
    features_4x = []
    contoured_images_4x = []  # To store contoured images

    for image in images:
        edge = cv2.Canny(image, low_threshold, high_threshold)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel, iterations=3)
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contoured_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # For particle counting, let's convert the image back to BGR, since count_particles expects a BGR image
        # If the original color information is needed for accurate particle counting, adjustments might be needed
        image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        particle_count = count_particles(image_bgr)

        for contour in contours:
            cv2.drawContours(contoured_image, [contour], -1, (0, 255, 0), 2)
            area_mm2, perimeter_mm, diameter_mm = calculate_features(contour, scale_factor_4x)
            features_4x.append((area_mm2, perimeter_mm, diameter_mm, particle_count))
        contoured_images_4x.append(contoured_image)

    return features_4x, contoured_images_4x, [path.split(os.sep)[-1] for path in image_paths]


# Write the calculated features of contours to a CSV file.
def count_particles(image, lower_thresh=100, upper_thresh=255, min_area=10, max_area=1000):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, thresh_image = cv2.threshold(gray_image, lower_thresh, upper_thresh, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area
    filtered_contours = [contour for contour in contours if min_area <= cv2.contourArea(contour) <= max_area]
    
    # Count the filtered particles
    particle_count = len(filtered_contours)
    return particle_count

def write_features_to_csv_mm(features, image_names, output_dir, target_values):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_spheroid_features.csv"
    csv_file_path = os.path.join(output_dir, csv_file_name)
    
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Particle_Count', 'Target']
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i, feature in enumerate(features):
            image_name = image_names[i]
            if feature[0]:  # Check if there's a valid feature tuple
                writer.writerow({
                    'Image_Name': image_name, 
                    'Area_mm2': feature[0][0],
                    'Perimeter_mm': feature[0][1], 
                    'Diameter_mm': feature[0][2], 
                    'Particle_Count': feature[0][3] if len(feature[0]) > 3 else 'N/A',  # Check for particle count
                    'Target': target_values[i] if target_values and len(target_values) > i else None
                })
    return csv_file_path


# Write the calculated features of contours to a CSV file for 4x.
def write_features_to_csv_4x(features, image_names, output_dir, target_values_4x=None):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_4x_spheroid_features.csv"
    csv_file_path = os.path.join(output_dir, csv_file_name)
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Particle_Count', 'Target']
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for feature, image_name in zip(features, image_names):
            writer.writerow({
                'Image_Name': image_name, 
                'Area_mm2': feature[0],
                'Perimeter_mm': feature[1], 
                'Diameter_mm': feature[2],
                'Particle_Count': feature[3] if len(feature) > 3 else 'N/A',  # Check for particle count
                'Target': target_values_4x[image_names.index(image_name)] if target_values_4x and image_name in target_values_4x else None
            })
    return csv_file_path


# Set parameters for image processing.
scale_factor = 0.0786
scale_factor_4x = 0.0786 * 10 / 4
spheroid_image_dir = 'prework/assets/images'
spheroid_image_dir_4x = 'prework/assets/images4x'
output_dir = 'prework/data'
image_names = os.listdir(spheroid_image_dir)
spheroid_features_mm = []

# Process 4x images and write the features to a CSV file.
features_4x, contoured_images_4x, image_names_4x = process_images_4x(spheroid_image_dir_4x, scale_factor_4x)
csv_file_path_4x = write_features_to_csv_4x(features_4x, image_names_4x, output_dir)
print(f"4x features CSV file saved to: {csv_file_path_4x}")

# Process each image and store the features in a list.
for img_name in image_names:
    img_path = os.path.join(spheroid_image_dir, img_name)
    features, contoured_image = process_image(img_path, scale_factor) 
    spheroid_features_mm.append((features, contoured_image)) 

target_values = ["1", "0", "1", "0"] 
#target values for 4x images
target_values_4x = ["1", "0", "1", "0"]

# Write the features to a CSV file and display the results.
csv_file_path_mm = None
if len(spheroid_features_mm) == len(image_names) and spheroid_features_mm:
    csv_file_path_mm = write_features_to_csv_mm(spheroid_features_mm, image_names, output_dir, target_values)
    print(f"CSV file saved to: {csv_file_path_mm}")

    df = pd.read_csv(csv_file_path_mm)
    print(df[['Image_Name', 'Area_mm2','Perimeter_mm', 'Diameter_mm', 'Target']])

for i, (feature, contoured_image) in enumerate(spheroid_features_mm):
    img_name = image_names[i]
 
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
python_path = sys.executable
model_py_path = os.path.join('prework', 'model.py')

if os.path.isfile(model_py_path):
    try:
        print("Running the model.py file...")
        subprocess.run([python_path, model_py_path, csv_file_path_mm], check=True)
        print("model.py file executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the model.py file: {e}")
else:
    print("Model.py file not found.")