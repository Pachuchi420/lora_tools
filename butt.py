import cv2
import os

# Path to the folder containing the images
folder_path = '/Users/sebastianmacias/Pictures/Train/boutinela/Original'

# Output folder to save the cropped images
output_folder = '/Users/sebastianmacias/Pictures/Train/boutinela/Butt'

# Iterate through the images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Load the image
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply suitable image processing techniques
        # to highlight the buttocks/glutes region

        # Example: Apply binary thresholding
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort the contours based on area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get the bounding box of the largest contour
        if len(contours) > 0:
            x, y, w, h = cv2.boundingRect(contours[0])

            # Crop the image using the bounding box coordinates
            cropped_image = image[y:y+h, x:x+w]

            # Save the cropped image to the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, cropped_image)

            print(f"Cropped image saved: {output_path}")
        else:
            print(f"No buttocks/glutes region found in {filename}")
