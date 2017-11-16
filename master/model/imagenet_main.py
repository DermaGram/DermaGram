# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import tensorflow as tf
import numpy as np

import resnet_model
import vgg_preprocessing

parser = argparse.ArgumentParser()

parser.add_argument(
    '--data_dir', type=str, default='',
    help='The directory where the ImageNet input data is stored.')

parser.add_argument(
    '--image_test', type=str, default='',
    help='Image')

parser.add_argument(
    '--model_dir', type=str, default='/tmp/resnet_model',
    help='The directory where the model will be stored.')

parser.add_argument(
    '--resnet_size', type=int, default=50, choices=[18, 34, 50, 101, 152, 200],
    help='The size of the ResNet model to use.')

# parser.add_argument(
#     '--train_steps', type=int, default=6400000,
#     help='The number of steps to use for training.')
parser.add_argument(
    '--train_steps', type=int, default=2000,
    help='The number of steps to use for training.')

# parser.add_argument(
#     '--steps_per_eval', type=int, default=40000,
#     help='The number of training steps to run between evaluations.')
parser.add_argument(
    '--steps_per_eval', type=int, default=13,
    help='The number of training steps to run between evaluations.')

# parser.add_argument(
#     '--batch_size', type=int, default=32,
#     help='Batch size for training and evaluation.')
parser.add_argument(
    '--batch_size', type=int, default=7,
    help='Batch size for training and evaluation.')
# Net was trained on batch_size 7, but using one for testing

parser.add_argument(
    '--map_threads', type=int, default=5,
    help='The number of threads for dataset.map.')

parser.add_argument(
    '--first_cycle_steps', type=int, default=None,
    help='The number of steps to run before the first evaluation. Useful if '
    'you have stopped partway through a training cycle.')

dir(tf.contrib)
FLAGS = parser.parse_args()
Flags=FLAGS

# Scale the learning rate linearly with the batch size. When the batch size is
# 256, the learning rate should be 0.1.
# _INITIAL_LEARNING_RATE = 0.08 * FLAGS.batch_size / 256
_INITIAL_LEARNING_RATE = 0.0001

_NUM_CHANNELS = 3
_LABEL_CLASSES = 3

# _MOMENTUM = 0.9
_MOMENTUM = 0.7
_WEIGHT_DECAY = 1e-4

# _NUM_IMAGES = {
#     'train': 1281167,
#     'validation': 50000,
# }
_NUM_IMAGES = {
    'train': 1900,
    'validation': 100,
}


image_preprocessing_fn = vgg_preprocessing.preprocess_image
network = resnet_model.resnet_v2(
    resnet_size=FLAGS.resnet_size, num_classes=_LABEL_CLASSES)


batches_per_epoch = _NUM_IMAGES['train'] / FLAGS.batch_size

# def filenames(is_training):
#   """Return filenames for dataset."""
#   if is_training:
#     return [
#         os.path.join(FLAGS.data_dir, 'train-%05d-of-01024' % i)
#         for i in xrange(0, 1024)]
#   else:
#     return [
#         os.path.join(FLAGS.data_dir, 'validation-%05d-of-00128' % i)
#         for i in xrange(0, 128)]
def filenames(is_training):
  """Return filenames for dataset."""
  if is_training:
    return [
        os.path.join(FLAGS.data_dir, 'train-%05d-of-00128' % i)
        for i in xrange(0, 128)]
  else:
    return [
        os.path.join(FLAGS.data_dir, 'validation-%05d-of-00024' % i)
        for i in xrange(0, 24)]

def dataset_parser(value, is_training):
  """Parse an Imagenet record from value."""
  keys_to_features = {
      'image/encoded':
          tf.FixedLenFeature((), tf.string, default_value=''),
      'image/format':
          tf.FixedLenFeature((), tf.string, default_value='jpeg'),
      'image/class/label':
          tf.FixedLenFeature([], dtype=tf.int64, default_value=-1),
      'image/class/text':
          tf.FixedLenFeature([], dtype=tf.string, default_value=''),
      'image/object/bbox/xmin':
          tf.VarLenFeature(dtype=tf.float32),
      'image/object/bbox/ymin':
          tf.VarLenFeature(dtype=tf.float32),
      'image/object/bbox/xmax':
          tf.VarLenFeature(dtype=tf.float32),
      'image/object/bbox/ymax':
          tf.VarLenFeature(dtype=tf.float32),
      'image/object/class/label':
          tf.VarLenFeature(dtype=tf.int64),
  }

  parsed = tf.parse_single_example(value, keys_to_features)

  image = tf.image.decode_image(
      tf.reshape(parsed['image/encoded'], shape=[]),
      _NUM_CHANNELS)
  image = tf.image.convert_image_dtype(image, dtype=tf.float32)

  image = image_preprocessing_fn(
      image=image,
      output_height=network.default_image_size,
      output_width=network.default_image_size,
      is_training=is_training)

  label = tf.cast(
      tf.reshape(parsed['image/class/label'], shape=[]),
      dtype=tf.int32)

  return image, tf.one_hot(label, _LABEL_CLASSES)


def input_fn(is_training):
  """Input function which provides a single batch for train or eval."""
  dataset = tf.contrib.data.Dataset.from_tensor_slices(filenames(is_training))
  if is_training:
    dataset = dataset.shuffle(buffer_size=1024)
  dataset = dataset.flat_map(tf.contrib.data.TFRecordDataset)

  if is_training:
    dataset = dataset.repeat()

  dataset = dataset.map(lambda value: dataset_parser(value, is_training),
                        num_threads=FLAGS.map_threads,
                        output_buffer_size=FLAGS.batch_size)

  if is_training:
    buffer_size = 1250 + 2 * FLAGS.batch_size
    dataset = dataset.shuffle(buffer_size=buffer_size)

  iterator = dataset.batch(FLAGS.batch_size).make_one_shot_iterator()
  images, labels = iterator.get_next()
  return images, labels


def resnet_model_fn(features, labels, mode=False):
  """ Our model_fn for ResNet to be used with our Estimator."""
  tf.summary.image('images', features, max_outputs=6)

  logits = network(
      inputs=features, is_training=(mode == tf.estimator.ModeKeys.TRAIN))

  predictions = {
      'classes': tf.argmax(logits, axis=1),
      'probabilities': tf.nn.softmax(logits, name='softmax_tensor')
  }

  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate loss, which includes softmax cross entropy and L2 regularization.
  cross_entropy = tf.losses.softmax_cross_entropy(
      logits=logits, onehot_labels=labels)

  # Create a tensor named cross_entropy for logging purposes.
  tf.identity(cross_entropy, name='cross_entropy')
  tf.summary.scalar('cross_entropy', cross_entropy)

  # Add weight decay to the loss. We perform weight decay on all trainable
  # variables, which includes batch norm beta and gamma variables.
  loss = cross_entropy + _WEIGHT_DECAY * tf.add_n(
      [tf.nn.l2_loss(v) for v in tf.trainable_variables()])

  if mode == tf.estimator.ModeKeys.TRAIN:
    global_step = tf.train.get_or_create_global_step()

    # # Multiply the learning rate by 0.1 at 30, 60, 120, and 150 epochs.
    # Multiply the learning rate by 0.1 at 30, 60, 120, and 150 epochs.
    boundaries = [
        int(batches_per_epoch * epoch) for epoch in [10, 20, 40, 60]]
    values = [
        _INITIAL_LEARNING_RATE * decay for decay in [1, 0.1, 0.01, 1e-3, 1e-4]]
    learning_rate = tf.train.piecewise_constant(
        tf.cast(global_step, tf.int32), boundaries, values)

    # boundaries = [
    #     int(batches_per_epoch * epoch) for epoch in [30, 60, 120, 150]]
    # values = [
    #     _INITIAL_LEARNING_RATE * decay for decay in [1, 0.1, 0.01, 1e-3, 1e-4]]
    # learning_rate = tf.train.piecewise_constant(
    #     tf.cast(global_step, tf.int32), boundaries, values)



    # Create a tensor named learning_rate for logging purposes.
    tf.identity(learning_rate, name='learning_rate')
    tf.summary.scalar('learning_rate', learning_rate)

    optimizer = tf.train.MomentumOptimizer(
        learning_rate=learning_rate,
        momentum=_MOMENTUM)

    # Batch norm requires update_ops to be added as a train_op dependency.
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
      train_op = optimizer.minimize(loss, global_step)
  else:
    train_op = None

  accuracy = tf.metrics.accuracy(
      tf.argmax(labels, axis=1), predictions['classes'])
  metrics = {'accuracy': accuracy}

  # Create a tensor named train_accuracy for logging purposes.
  tf.identity(accuracy[1], name='train_accuracy')
  tf.summary.scalar('train_accuracy', accuracy[1])

  return tf.estimator.EstimatorSpec(
      mode=mode,
      predictions=predictions,
      loss=loss,
      train_op=train_op,
      eval_metric_ops=metrics)

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

  image = vgg_preprocessing.preprocess_image(
    image=image,
    output_height=network.default_image_size,
    output_width=network.default_image_size,
    is_training=False)
  print(image)
  print(image.shape)
  image_2 = tf.expand_dims(image, 0)
  image_2=tf.tile(image_2, [7, 1, 1, 1])
  print(image_2)
  image=image_2
  return image






def main(unused_argv):
  # Using the Winograd non-fused algorithms provides a small performance boost.
  os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
  dir(tf.contrib)
  # resnet_classifier = tf.estimator.Estimator(
  #     model_fn=resnet_model_fn, model_dir=FLAGS.model_dir)


  # coder = ImageCoder() #Create an instance of ImageCoder for _process_image
  # image, im_height, im_width = _process_image(Flags.image_test, coder)

  # image = tf.image.decode_image(
  #   tf.reshape(image, shape=[]),
  #   _NUM_CHANNELS)
  # image = tf.image.convert_image_dtype(image, dtype=tf.float32)

  # image = vgg_preprocessing.preprocess_image(
  #   image=image,
  #   output_height=network.default_image_size,
  #   output_width=network.default_image_size,
  #   is_training=False)
  # print(image)
  # print(image.shape)
  # image_2 = tf.expand_dims(image, 0)
  # image_2=tf.tile(image_2, [7, 1, 1, 1])
  # print(image_2)
  # image=image_2
  # graph = tf.Graph()
  # with graph.as_default():
  #   with tf.Session(graph=graph) as sess:
  #     dir(tf.contrib)
  #     saver = tf.train.import_meta_graph('/Users/jaspalsingh/Desktop/dermagram/part2/models/research/inception/tmp/derm/res/inference/model.ckpt-1989.meta')
  #     saver.restore(sess, tf.train.latest_checkpoint('./'))

  #     coder = ImageCoder() #Create an instance of ImageCoder for _process_image
  #     image, im_height, im_width = _process_image(Flags.image_test, coder)
  #     # logits = network(
  #     #     inputs=image, is_training=False)
      
  #     # predictions = {
  #     #     'classes': tf.argmax(logits, axis=1),
  #     #     'probabilities': tf.nn.softmax(logits, name='softmax_tensor')
  #     # }
  #     # test_results= tf.estimator.EstimatorSpec(tf.estimator.ModeKeys.PREDICT, predictions=predictions)
  #     # print(test_results)
  #     resnet_classifier = tf.estimator.Estimator(
  #       model_fn=resnet_model_fn, model_dir=Flags.model_dir)
  #     numpy_input_fn = tf.estimator.inputs.numpy_input_fn
  #     test_results = resnet_classifier.predict(input_fn=lambda: input_fn_2(image))
  #     print('prediction computed')
  #     tests=list(test_results)
  #     print(tests)


      # print('Starting to evaluate.')
      # eval_results = resnet_classifier.evaluate(input_fn=lambda: input_fn(False))
      # print(eval_results)


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
