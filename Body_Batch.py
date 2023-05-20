import os
import cv2
import numpy as np
import face_recognition

def crop_image_excluding_faces(image_path, output_path, expansion_factor):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        return

    top_most = image.shape[0]
    bottom_most = 0
    for face_location in face_locations:
        top, right, bottom, left = face_location

        # Calculate the expansion amount
        expand_width = int((right - left) * expansion_factor)
        expand_height = int((bottom - top) * expansion_factor)

        # Expand the bounding box coordinates
        expanded_top = max(0, top - expand_height)
        expanded_bottom = min(image.shape[0], bottom + expand_height)

        top_most = min(top_most, expanded_top)
        bottom_most = max(bottom_most, expanded_bottom)

    if top_most > image.shape[0] - bottom_most:
        cropped_image = image[0:top_most, :]
    else:
        cropped_image = image[bottom_most:, :]

    # Save the cropped image in BGR color space
    cv2.imwrite(output_path, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))

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

image_count = 0
total_images = sum([filename.endswith((".jpg", ".jpeg", ".png")) for filename in os.listdir(input_folder)])

for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        image_count += 1

        crop_image_excluding_faces(image_path, output_path, expansion_factor)

        if image_count >= total_images:
            break

print("Image cropping completed!")
