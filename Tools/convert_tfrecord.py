import tensorflow as tf
import json
import os
import cv2
from object_detection.utils import dataset_util

# Label map - map class names to integer labels
label_map = {"body": 1}  # replace with your class labels

def create_tf_example(data, img_path):
    with tf.io.gfile.GFile(img_path, 'rb') as fid:
        encoded_image_data = fid.read()
    image = cv2.imread(img_path)
    height, width, _ = image.shape

    filename = data['filename'].encode('utf8')
    image_format = b'jpeg'

    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for obj in data['objects']:
        xmins.append(obj['bbox'][0] / width)
        xmaxs.append(obj['bbox'][2] / width)
        ymins.append(obj['bbox'][1] / height)
        ymaxs.append(obj['bbox'][3] / height)
        classes_text.append(obj['label'].encode('utf8'))
        classes.append(label_map[obj['label']])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def create_tf_records(parsed_data_file, output_file):
    with tf.io.TFRecordWriter(output_file) as writer:
        with open(parsed_data_file, 'r') as f:
            data = json.load(f)
        for item in data:
            img_path = os.path.join(os.path.dirname(parsed_data_file), item['filename'])
            tf_example = create_tf_example(item, img_path)
            writer.write(tf_example.SerializeToString())

create_tf_records('/Users/sebastianmacias/Pictures/Train/boutinela/Model2/Batch1/parsed_annotations.json', '/Users/sebastianmacias/Pictures/Train/boutinela/Model2/Batch1/train.record')
print("Done")

