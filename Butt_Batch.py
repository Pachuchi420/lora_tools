import tensorflow as tf
import cv2
import numpy as np

# Load the trained model
model = tf.saved_model.load('path_to_your_model')

# Load the image
image = cv2.imread('path_to_your_image')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
input_tensor = tf.convert_to_tensor(image_rgb)
input_tensor = input_tensor[tf.newaxis, ...]  # Add batch dimension

# Run inference
output_dict = model(input_tensor)

# Loop over the detections and draw bounding boxes on the image
num_detections = int(output_dict.pop('num_detections'))
for i in range(num_detections):
    # You might need to adjust this depending on your model's output
    class_id = int(output_dict['detection_classes'][0][i])
    score = output_dict['detection_scores'][0][i]
    bbox = output_dict['detection_boxes'][0][i]

    # Check if the detection is of a leg and its score is more than 0.5
    if class_id == 1 and score > 0.5:
        # The bounding box coordinates are given in normalized form (i.e., in the interval [0, 1]).
        # Therefore, denormalize the bounding box coordinates.
        height, width, _ = image.shape
        (left, top, right, bottom) = (bbox[1] * width, bbox[0] * height, bbox[3] * width, bbox[2] * height)
        
        # Crop the image
        cropped_image = image[int(top):int(bottom), int(left):int(right)]
        cv2.imwrite(f"crop_{i}.jpg", cropped_image)
