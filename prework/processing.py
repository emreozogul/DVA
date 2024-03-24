import cv2
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import sys

def calculate_features(contour, scale_factor):
    area_mm2 = cv2.contourArea(contour) * (scale_factor)**2
    perimeter_mm = cv2.arcLength(contour, True) * (scale_factor)
    (x, y), radius_pixels = cv2.minEnclosingCircle(contour)
    diameter_mm = 2 * radius_pixels * (scale_factor)
    return area_mm2, perimeter_mm, diameter_mm

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
        contoured_image = cv2.drawContours(image.copy(), [largest_contour], -1, (0, 255, 0), 2)
        return calculate_features(largest_contour, scale_factor), contoured_image # Değişiklik: binary yerine contoured_image döndürülüyor
    else:
        return None, None

def write_features_to_csv_mm(features, image_names, output_dir, target_values):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_spheroid_features.csv"
    csv_file_path = os.path.join(output_dir, csv_file_name)
    
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Target']
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i, feature in enumerate(features):
            image_name = image_names[i]
            if feature[0]: # Değişiklik: Özellikler varsa
                writer.writerow({
                    'Image_Name': image_name, 
                    'Area_mm2': feature[0][0],
                    'Perimeter_mm': feature[0][1], 
                    'Diameter_mm': feature[0][2], 
                    'Target': target_values[i] if target_values and len(target_values) > i else None
                })
    return csv_file_path

scale_factor = 0.0786
spheroid_image_dir = 'prework/assets/images'
output_dir = 'prework/data'
image_names = os.listdir(spheroid_image_dir)
spheroid_features_mm = []

for img_name in image_names:
    img_path = os.path.join(spheroid_image_dir, img_name)
    features, contoured_image = process_image(img_path, scale_factor) # Değişiklik: binary_image yerine contoured_image
    if features:
        spheroid_features_mm.append((features, contoured_image)) # Değişiklik: contoured_image ekleniyor

target_values = ["1", "0", "1", "0"] # Örnek olarak, resim sayınıza uygun bir liste sağlayın

# CSV dosyasını yazdırma kısmı
csv_file_path_mm = None
if len(spheroid_features_mm) == len(image_names) and spheroid_features_mm:
    csv_file_path_mm = write_features_to_csv_mm(spheroid_features_mm, image_names, output_dir, target_values)
    print(f"CSV file saved to: {csv_file_path_mm}")

    # CSV dosyasını okuyup içeriğini gösterme
    df = pd.read_csv(csv_file_path_mm)
    print(df[['Image_Name', 'Area_mm2','Perimeter_mm', 'Diameter_mm', 'Target']])

for i, (feature, contoured_image) in enumerate(spheroid_features_mm):
    img_name = image_names[i]
    # Görüntüleri gösterme
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

# model.py dosyasını çalıştırma bölümü
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

