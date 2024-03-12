import cv2
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os

def calculate_features(contour, scale_factor_pixels_per_micrometer):
    # Convert from pixels to micrometers, then to millimeters
    area_mm2 = cv2.contourArea(contour) * (scale_factor_pixels_per_micrometer/1000)**2  # Convert area to mm^2
    perimeter_mm = cv2.arcLength(contour, True) * (scale_factor_pixels_per_micrometer/1000)  # Convert perimeter to mm
    (x, y), radius_pixels = cv2.minEnclosingCircle(contour)
    diameter_mm = 2 * radius_pixels * (scale_factor_pixels_per_micrometer/1000)  # Convert diameter to mm
    return area_mm2, perimeter_mm, diameter_mm

def write_features_to_csv_mm(features, image_names):
    # Include a timestamp in the CSV file name to ensure uniqueness
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file_name = f"{timestamp}_spheroid_features.csv"
    csv_file_path = os.path.join("prework", "data", csv_file_name)
    
    # Define the headers for the CSV file
    # TODO --> add target column name
    fieldnames = ['Image_Name', 'Area_mm2', 'Perimeter_mm', 'Diameter_mm']
    
    # Write to CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for feature_set, image_name in zip(features, image_names):
            for feature in feature_set:
                writer.writerow({'Image_Name': image_name, 'Area_mm2': feature[0], 'Perimeter_mm': feature[1], 'Diameter_mm': feature[2]})
    return csv_file_path

def equalize_histogram(image):
    # LAB renk uzayına dönüştür
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # Histogram eşitleme uygula
    l_eq = cv2.equalizeHist(l)
    limg = cv2.merge((l_eq, a, b))
    # Sonuçları BGR renk uzayına geri dönüştür
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


# Load the calibration image
calibration_path = "prework/assets/calibrations/4x_calibration.tif"
calibration_image = cv2.imread(calibration_path, cv2.IMREAD_UNCHANGED)

# Check if the image is loaded successfully
if calibration_image is not None:
    print("Image loaded successfully.")
    print("Image shape:", calibration_image.shape)
    print("Image depth:", calibration_image.dtype)

    # Convert the depth of the image to uint8
    calibration_image = cv2.convertScaleAbs(calibration_image)

    # Convert to grayscale and apply Gaussian Blur
    calibration_blurred = cv2.GaussianBlur(cv2.cvtColor(calibration_image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(calibration_blurred, 50, 150)

    # Continue with your further processing...
else:
    print("Failed to load the image.")


# Convert to grayscale and apply Gaussian Blur
calibration_blurred = cv2.GaussianBlur(cv2.cvtColor(calibration_image, cv2.COLOR_BGR2GRAY), (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(calibration_blurred, 50, 150)

# Sum the edges vertically
vertical_sum = np.sum(edges, axis=0)

# Find peaks in the vertical_sum which correspond to the edges of the scale bar lines
peaks, _ = find_peaks(vertical_sum, height=np.max(vertical_sum)/2)
sorted_peaks = np.sort(peaks)[:2]
distance_pixels = np.diff(sorted_peaks)[0]
scale_factor_micrometers_per_pixel = 10 / distance_pixels  # 10 micrometers divided by distance in pixels

spheroid_image_dir = "prework/assets/images"
image_names = os.listdir(spheroid_image_dir)
spheroid_images = []


for img_name in image_names:
    img_path = os.path.join(spheroid_image_dir, img_name)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Failed to load image: {img_name}")
        continue
    # Convert the depth of the image to uint8 if necessary
    if img.dtype != np.uint8:
        img = cv2.convertScaleAbs(img)
    spheroid_images.append(img)

# Check if any images were loaded
if not spheroid_images:
    print("No spheroid images were loaded.")
    exit()

# Convert images to grayscale and apply thresholding
binary_images = []
for img in spheroid_images:
    # Histogram eşitleme uygula
    img_eq = equalize_histogram(img)
    
    # Gri tonlamaya çevir ve eşikleme uygula
    gray_img = cv2.cvtColor(img_eq, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    _, binary_img = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binary_images.append(binary_img)

# Find contours and filter out small ones
contours_list = [cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] for binary_image in binary_images]
spheroid_contours = [[cnt for cnt in contours if cv2.contourArea(cnt) > 100] for contours in contours_list]

# Calculate the features for each spheroid using the new scale factor
spheroid_features_mm = [[calculate_features(cnt, scale_factor_micrometers_per_pixel) for cnt in contours] for contours in spheroid_contours]

csv_file_path_mm = None

# Ensure both lists have the same length and are not empty
if len(spheroid_features_mm) == len(image_names) and len(spheroid_features_mm) > 0:
    # Write the features to a CSV file in the image directory
    csv_file_path_mm = write_features_to_csv_mm(spheroid_features_mm, image_names)
else:
    print("Error: Length mismatch or empty list.")


# Display and save processed images individually
for i, (original_img, binary_img) in enumerate(zip(spheroid_images, binary_images)):
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(binary_img, cmap='gray')
    plt.title('Processed Image')
    plt.axis('off')
    
    plt.show()

