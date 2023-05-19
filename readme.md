
I've created this whole setup to be able to crop on butts for my dataset to train a Lora model. Yeah, it's dumb I know.

The workflow goes as follows: 

1. Install instaload
2. Download images of selected user with command found in "instaload command.txt"
3. Use Body_Batch.py to crop images from neck down. Take into note that that actual script isn't really good, needs improving, you also have to change the input and output paths. 
4. Face_Batch.py works the same just change the input and output paths.
5. Use the Butt_Batch.py as same. 


EXTRA
If you want to train a new model to detect a body_part in specific do the following: 

1. Place images you want to use to train your model in a folder, ex. .../images/. 
1. Use https://www.makesense.ai to import images you want to work on (the ones in .../images/) ( >= 200 is recommended) then using the labeling and selection boxes, work on what you want to detect (say you want to detect feet, then name the label feet and select the feet on every image)

2. Download the .zip package containing files in VOC XML format, open the zip file and place all of the xml files just where you saved your images in the .../images/ directory. 

3. Parse the information with Parser.py, make sure to use the right directory pointing to .../images/ in the last line.

4. Use this new parsed .json and convert it to a TFRecords format:
    - Install TensorFlow and TensorFlow's Object Detection API
    - Use the convert_tfrecord.py (make sure to add the right path and also add the right classes, classes are basically the lables, so if you have 3 labels: feet, eyes, and stomach add this at the top of the list: label_map = {"feet": 1, "eyes": 2, "stomach": 3} )

5. Once you have the tfrecords file, download a pre-trained model from https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md and configure it. Each pre-trained model comes with a pipeline configuration file. This file contains several settings that control how the model is trained, including which pre-trained model to use, how many training steps to take, what learning rate to use, etc. You'll need to download this file and modify certain fields to suit your task. Key fields to update include:
* num_classes: This should match the number of classes in your dataset.
* fine_tune_checkpoint: This should point to the 'checkpoint' file from your pre-trained model.
* train_input_reader and eval_input_reader: These sections should be updated to point to your TFRecord files and label map.
* batch_size, learning_rate, num_steps: Depending on your resources and the size of your dataset, you might also need to tweak these fields.

Some more infromation regarding the models, below I give some recommendations:
- SSD (Single Shot MultiBox Detector) with MobileNet: SSD is a very efficient model in terms of speed and is sufficient for tasks where high precision is not required. It can be combined with MobileNet, a lightweight and efficient base network designed to run on devices with limited computational resources. It's a good choice if speed is a concern.
- Faster R-CNN (Region Proposal Network + Fast R-CNN): This is a slower but highly accurate model. It is often used when high precision is needed. It comes with various backbone options such as ResNet and Inception.

6. Train the model: With everything set up, you're ready to train your model. Using the model_main_tf2.py script in the TensorFlow Object Detection API, you can start the training process. The command usually looks something like this:

python model_main_tf2.py --pipeline_config_path=path_to_your_pipeline.config --model_dir=path_to_output_directory --alsologtostderr

path_to_your_pipeline.config is the path to the pipeline configuration file you just modified. path_to_output_directory is the directory where you want the model to save its checkpoints.


7. Evaluate and export the model: After training, you can evaluate your model's performance on your validation or test data. Once you're satisfied with the performance, you can export the model into a form that can be used for inference. This is typically done with the exporter_main_v2.py script in the TensorFlow Object Detection API:

python exporter_main_v2.py --input_type=image_tensor --pipeline_config_path=path_to_your_pipeline.config --trained_checkpoint_dir=path_to_checkpoints --output_directory=path_to_output_directory

path_to_checkpoints is the directory where your model saved its checkpoints during training.


8. Say your model was trained to detect legs. You can use it to detect legs in new images and then crop the images around the detected bounding boxes. Use Butt_Batch.py as a starting point.

This script reads an image, runs the model on the image, checks if the model detected any legs with a confidence score of more than 0.5, and if so, crops the image around the bounding box of each detection and saves the cropped image.

You could easily modify this script to loop over multiple images and apply the same process to each one.

Please note that depending on your specific use case, you may want to adjust the confidence threshold (I've used 0.5 in this example). Also, keep in mind that the code for extracting the class ID, score, and bounding box from the output dictionary might need to be adjusted depending on how your specific model structures its output.

Finally, remember to replace 'path_to_your_model' and 'path_to_your_image' with the paths to your saved model and your input image, respectively.



