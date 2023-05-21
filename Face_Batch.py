import os
import cv2
import face_recognition

# Function to detect and crop faces
def crop_faces(image_path, output_path, target_size, expansion_factor):

    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    # If no faces are detected, print a message and return
    if len(face_locations) == 0:
        print(f"No faces detected in {image_path}")
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

        print(f"{image_count}/{total_images} Cropped and saved image: {output_path}")

# Function to remove quotation marks from a path
def remove_quotes(path):
    if path.startswith('"') and path.endswith('"'):
        return path[1:-1]
    return path

# Prompt the user to input the input and output paths
input_folder = remove_quotes(input("Enter the path to the folder containing the images: "))
output_folder = remove_quotes(input("Enter the path to the folder where the cropped images will be saved: "))
expansion_factor = float(input("Enter the expansion factor for cropping (e.g., 0.2 for 20% expansion): "))
target_size = (768, 768)  # Specify your desired target size here

image_count = 0
total_images = sum([filename.endswith((".jpg", ".jpeg", ".png")) for filename in os.listdir(input_folder)])

for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        image_count += 1

        crop_faces(image_path, output_path, target_size, expansion_factor)

        if image_count >= total_images:
            break

print("Face cropping completed!")
