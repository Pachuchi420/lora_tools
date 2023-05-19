import os
import cv2
import face_recognition

# Function to detect and crop faces
def crop_faces(image_path, output_path, target_size, expansion_factor):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    # If no faces are detected, return
    if len(face_locations) == 0:
        return

    # Crop and save each face with expanded bounding box
    for face_location in face_locations:
        top, right, bottom, left = face_location

        # Calculate the expansion amount
        expand_width = int((right - left) * expansion_factor)
        expand_height = int((bottom - top) * expansion_factor)

        # Expand the bounding box coordinates
        expanded_top = max(0, top - expand_height)
        expanded_right = min(image.shape[1], right + expand_width)
        expanded_bottom = min(image.shape[0], bottom + expand_height)
        expanded_left = max(0, left - expand_width)

        # Crop the expanded face region
        expanded_face_image = image[expanded_top:expanded_bottom, expanded_left:expanded_right]

        # Resize the expanded face to a larger size
        resized_face = cv2.resize(expanded_face_image, target_size, interpolation=cv2.INTER_CUBIC)

        # Convert back to BGR color space
        bgr_face = cv2.cvtColor(resized_face, cv2.COLOR_RGB2BGR)

        # Save the cropped face
        cv2.imwrite(output_path, bgr_face)

        print(f"Cropped and saved image: {output_path}")

# Prompt the user to input the input and output paths
input_folder = input("Enter the path to the folder containing the images: ")
output_folder = input("Enter the path to the folder where the cropped images will be saved: ")

# Target size for cropping
target_size = (768, 768)

# Expansion factor for the bounding box (adjust as needed)
expansion_factor = 0.5  # 50% expansion

# Iterate over the images in the input folder
image_count = 0
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Call the crop_faces function to detect and crop faces with expanded bounding box
        crop_faces(image_path, output_path, target_size, expansion_factor)

        image_count += 1
        if image_count >= 500:
            break

print("Face cropping completed!")
