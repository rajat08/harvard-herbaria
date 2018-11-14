import sys
import cv2 as cv
import tensorflow as tf
from alexNet import AlexNet
import numpy as np
#----------------------------------------------------------------------------------------------------------------------
# Author: Siqi Zhang
# Description: This is the executable for predicting on minipatch
# Input: a filename
# Output: a .jpg file with feature labeled
# Assumptions:
#               executable and csv are in the same directory
#----------------------------------------------------------------------------------------------------------------------
weights_file = "model/model_epoch401.ckpt"
# validation patch location
IMAGENET_MEAN = [123.68, 116.779, 103.939]
# Learning params
learning_rate = 0.001
num_epochs = 500
batch_size = 225
# Network params
dropout_rate = 0.5
num_classes = 4
train_layers = ['fc8', 'fc7', 'fc6']
patch_size = 227
def main(argv):
    img_name = "Anemone_canadensis.102823.6293.jpg"
    # load and preprocess the image
    print(argv)
    origin_img = cv.imread(argv[0])
    if origin_img is None:
        print("image does not exist")
        return 0
    #mean subtraction
    img = np.subtract(origin_img, IMAGENET_MEAN)
    #tile the image
    tiled_image = np.tile(img, (batch_size, 1, 1, 1))
    tiled_image = tiled_image.astype(np.float32)
    # TF placeholder for graph input and output
    x = tf.placeholder(tf.float32, [batch_size, 227, 227, 3])
    keep_prob = tf.placeholder(tf.float32)
    # Initialize model
    model = AlexNet(x, keep_prob, num_classes, train_layers)

    # Link variable to model output
    score = model.fc8

    with tf.name_scope("predict"):
        predict = score

    # Start Tensorflow session
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print('Restoring weights from: ' + weights_file)
        saver = tf.train.Saver()
        saver.restore(sess, weights_file)
        prediction = sess.run(predict, feed_dict={x: tiled_image, keep_prob: 1.})
    # find the label with highest prediction value
    pred_label = np.argmax(prediction[0])
    if pred_label == 0:
        print("This is a bud")
    elif pred_label == 1:
        print("This is a flower")
    elif pred_label == 2:
        print("This is a fruit")
    elif pred_label == 3:
        print("I don't know what it is")
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])