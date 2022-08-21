

def get_op():
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
    import pathlib
    import tensorflow as tf
    import cv2
    import argparse
    from IPython.display import display
    
    # from google.colab.patches import cv2_imshow
    # Enable GPU dynamic memory allocation
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    # PROVIDE PATH TO IMAGE DIRECTORY
    cwd=pathlib.Path(__file__).parent.resolve()
    # IMAGE_PATHS = r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy\static\test.jpg'
    IMAGE_PATHS = os.path.join(cwd,'static\\test.jpg')
    
    # PROVIDE PATH TO MODEL DIRECTORY
    # PATH_TO_MODEL_DIR = r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy'
    PATH_TO_MODEL_DIR = cwd
    
    # PROVIDE PATH TO LABEL MAP
    # PATH_TO_LABELS = r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy\label_map.pbtxt'
    PATH_TO_LABELS = os.path.join(cwd,'label_map.pbtxt')
    
    
    # PROVIDE THE MINIMUM CONFIDENCE THRESHOLD
    MIN_CONF_THRESH = float(0.60)
    # LOAD THE MODEL
    import time
    from object_detection.utils import label_map_util
    from object_detection.utils import visualization_utils as viz_utils
    
    # PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"
    PATH_TO_SAVED_MODEL = os.path.join(PATH_TO_MODEL_DIR, "saved_model")
    print('Loading model...', end='')
    start_time = time.time()
    
    
    
    # LOAD SAVED MODEL AND BUILD DETECTION FUNCTION
    
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    
    
    
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))
    # LOAD LABEL MAP DATA FOR PLOTTING
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                        use_display_name=True)
    import numpy as np
    from PIL import Image
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings
    def load_image_into_numpy_array(path):
        """Load an image from file into a numpy array.
        Puts image into numpy array to feed into tensorflow graph.
        Note that by convention we put it into a numpy array with shape
        (height, width, channels), where channels=3 for RGB.
        Args:
          path: the file path to the image
        Returns:
          uint8 numpy array with shape (img_height, img_width, 3)
        """
        return np.array(Image.open(path))
    print('Running inference for {}... '.format(IMAGE_PATHS), end='')
    
    image = cv2.imread(IMAGE_PATHS)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_expanded = np.expand_dims(image_rgb, axis=0)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]
    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)
    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
    detections['num_detections'] = num_detections
    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    image_with_detections = image.copy()
    # SET MIN_SCORE_THRESH BASED ON YOU MINIMUM THRESHOLD FOR DETECTIONS
    viz_utils.visualize_boxes_and_labels_on_image_array(
          image_with_detections,
          detections['detection_boxes'],
          detections['detection_classes'],
          detections['detection_scores'],
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=200,
          min_score_thresh=0.5,
          agnostic_mode=False)
    # print('Done')
    # DISPLAYS OUTPUT IMAGE
    cv2.imshow('',image_with_detections)
    
    # CLOSES WINDOW ONCE KEY IS PRESSED
    # print(detections['detection_classes'])
    # print(plt.imshow(image_with_detections))
    # plt.imshow(image_with_detections)
    
    cv2.imwrite(r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy\static\output.jpg', image_with_detections)
    print('Done')
    # DISPLAYS OUTPUT IMAGE
    
    # CLOSES WINDOW ONCE KEY IS PRESSED
    return image_with_detections




if __name__== '__main__':
    get_op()

