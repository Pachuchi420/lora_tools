
import os
import cv2

# Load pre-trained face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Prompt the user for the input and output paths
input_path = input("Enter the path to the input image folder: ").strip('\"')
output_path = input("Enter the path to the output folder for enhanced images: ").strip('\"')

# Count the images to enhance
image_count = 0

# Process each image in the input folder
for filename in os.listdir(input_path):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # Load image
        image_path = os.path.join(input_path, filename)
        image = cv2.imread(image_path)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over detected faces
        for (x, y, w, h) in faces:
            # Extract face region of interest
            face_roi = image[y:y + h, x:x + w]

            # Apply facial enhancements (e.g., filters, adjustments, etc.) to face_roi
            # Add your code here to enhance the facial features

            # Replace the original face region with the enhanced face_roi
            image[y:y + h, x:x + w] = face_roi

        # Save the enhanced image
        output_filename = os.path.join(output_path, filename)
        cv2.imwrite(output_filename, image)

        # Display the message for the enhanced image
        image_count += 1
        print(f"Enhanced image {image_count}: {output_filename}")

print("Face enhancement completed!")
