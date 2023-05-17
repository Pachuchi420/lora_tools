import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Step 1: Parse XML file
xml_file = '/Users/sebastianmacias/Pictures/TrainingModels/miranda.stx/SvmTrain/miranda.xml'

tree = ET.parse(xml_file)
root = tree.getroot()

data = []
labels = []

for image in root.findall('.//image'):
    image_file = image.get('file')

    for box in image.findall('box'):
        label = box.find('label').text

        if label == 'body':
            labels.append(1)
        else:
            labels.append(0)

        data.append(image_file)

# Step 2: Load images and convert to feature vectors
feature_vectors = []
image_dir = '/Users/sebastianmacias/Pictures/TrainingModels/miranda.stx/SvmTrain/'

for image_file in data:
    img_path = os.path.join(image_dir, image_file)
    img = cv2.imread(img_path)

    # Perform necessary preprocessing on the image
    # For example, resizing, normalization, etc.
    # ...

    feature_vectors.append(img.flatten())

# Ensure all feature vectors have the same length
max_length = max(len(vec) for vec in feature_vectors)
feature_vectors = [vec if len(vec) == max_length else np.pad(vec, (0, max_length - len(vec))) for vec in feature_vectors]

feature_vectors = np.array(feature_vectors)

# Step 3: Train the SVM classifier
X_train, X_test, y_train, y_test = train_test_split(
    feature_vectors, labels, test_size=0.2, random_state=42
)

svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Step 4: Save the trained SVM model
svm_model_file = '/Users/sebastianmacias/Pictures/TrainingModels/miranda.stx/SvmTrain/Detectors/body.pkl'
joblib.dump(svm, svm_model_file)

# Evaluate the trained model
y_pred = svm.predict(X_test)
print(classification_report(y_test, y_pred))
