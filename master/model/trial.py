
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import sys
import threading

import numpy as np
import tensorflow as tf
import resnet_model
import vgg_preprocessing
import imagenet_main
from imagenet_main import resnet_model_fn
import itertools

parser_2 = argparse.ArgumentParser()

parser_2.add_argument(
    '--image', type=str, default='',
    help='Image to be inferenced.')

parser_2.add_argument(
    '--resnet_size', type=int, default=50, choices=[1],
    help='The size of the ResNet model to use.')

parser_2.add_argument(
    '--model_dir', type=str, default='../model',
    help='The directory where the model will be stored.')

Flags = parser_2.parse_args()

from imagenet_main import resnet_model_fn

_INITIAL_LEARNING_RATE = 0.0001

_NUM_CHANNELS = 3
_LABEL_CLASSES = 3

# _MOMENTUM = 0.9
_MOMENTUM = 0.7
_WEIGHT_DECAY = 1e-4

_NUM_IMAGES = {
    'train': 1900,
    'validation': 100,
}

network = resnet_model.resnet_v2(
    resnet_size=Flags.resnet_size, num_classes=_LABEL_CLASSES)

class ImageCoder(object):
  """Helper class that provides TensorFlow image coding utilities."""

  def __init__(self):
    # Create a single Session to run all image coding calls.
    self._sess = tf.Session()

    # Initializes function that converts PNG to JPEG data.
    self._png_data = tf.placeholder(dtype=tf.string)
    image = tf.image.decode_png(self._png_data, channels=3)
    self._png_to_jpeg = tf.image.encode_jpeg(image, format='rgb', quality=100)

    # Initializes function that decodes RGB JPEG data.
    self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
    self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

  def png_to_jpeg(self, image_data):
    return self._sess.run(self._png_to_jpeg,
                          feed_dict={self._png_data: image_data})

  def decode_jpeg(self, image_data):
    image = self._sess.run(self._decode_jpeg,
                           feed_dict={self._decode_jpeg_data: image_data})
    assert len(image.shape) == 3
    assert image.shape[2] == 3
    return image

def _is_png(filename):
  """Determine if a file contains a PNG format image.

  Args:
    filename: string, path of the image file.

  Returns:
    boolean indicating if the image is a PNG.
  """
  return filename.endswith('.png')

def _process_image(filename, coder):
  """Process a single image file.

  Args:
    filename: string, path to an image file e.g., '/path/to/example.JPG'.
    coder: instance of ImageCoder to provide TensorFlow image coding utils.
  Returns:
    image_buffer: string, JPEG encoding of RGB image.
    height: integer, image height in pixels.
    width: integer, image width in pixels.
  """
  # Read the image file.
  with tf.gfile.FastGFile(filename, 'rb') as f:
    image_data = f.read()

  # Convert any PNG to JPEG's for consistency.
  if _is_png(filename):
    print('Converting PNG to JPEG for %s' % filename)
    image_data = coder.png_to_jpeg(image_data)

  # Decode the RGB JPEG.
  image = coder.decode_jpeg(image_data)

  # Check that image converted to RGB
  assert len(image.shape) == 3
  height = image.shape[0]
  width = image.shape[1]
  assert image.shape[2] == 3

  return image_data, height, width


def input_fn_2(image):
  image = tf.image.decode_image(
    tf.reshape(image, shape=[]),
    _NUM_CHANNELS)
  image = tf.image.convert_image_dtype(image, dtype=tf.float32)

  image = vgg_preprocessing.preprocess_image(image=image, 
    output_height=network.default_image_size,
    output_width=network.default_image_size,
    is_training=False)
  image_2 = tf.expand_dims(image, 0)
  image_2=tf.tile(image_2, [7, 1, 1, 1])
  image=image_2
  return image

def main(unused_argv):
# Using the Winograd non-fused algorithms provides a small performance boost.
  os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
  dir(tf.contrib)

  graph = tf.Graph()
  with graph.as_default():
    with tf.Session(graph=graph) as sess:
      dir(tf.contrib)
      saver = tf.train.import_meta_graph('../model/model.ckpt-1376.meta')
      saver.restore(sess, 'model.ckpt-1376')
      coder = ImageCoder() #Create an instance of ImageCoder for _process_image
      image, im_height, im_width = _process_image(Flags.image_test, coder)

      resnet_classifier = tf.estimator.Estimator(
        model_fn=imagenet_main.resnet_model_fn, model_dir=Flags.model_dir)
      test_results = next(resnet_classifier.predict(input_fn=lambda: input_fn_2(image)))

      print('prediction computed')
      print(test_results['probabilities'])


if __name__ == '__main__':
  tf.app.run()
