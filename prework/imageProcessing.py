import cv2

def process_image(image_path):
    # Load the image from the file path
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        raise ValueError("Could not load the image at the path: {}".format(image_path))

    # Apply your OpenCV processing here
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Let's just save the processed image, or you can return the processed image
    processed_image_path = 'processed_image.png'
    cv2.imwrite(processed_image_path, processed_img)
    
    return processed_image_path
