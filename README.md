# DermaGram
CUNY Computer Science Capstone Project, Fall 2017  

DermaGram is an image recognition classifier that analyzses photos of skin lesions. The goal is to accurately classify the most severe case of cancer: melanoma.

### I. Data Sets
All images used for *training* and *evaluation* will be saved to Imgur. The name of each album should correspond to it's organization and intended use-case. All images should be of uniform dimensions (800x600).
* Original Data Source: 
  - ISIC-archive: https://isic-archive.com/
* Imgur Albums:
  - https://dermagram.imgur.com/

### II. Web Design
The User-Interface (UI) will be designed using Flask - a microframework for Python-based web applications.
* Flask Overview: http://flask.pocoo.org/
* Flask Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### III. Model
We will be using TensorFlow's image recognition model 'Inception-v3'
* TensorFlow Intro: https://www.tensorflow.org/tutorials/image_recognition
* Inception-v3 Github: https://github.com/tensorflow/models/tree/master/official/resnet
* Inception-v3 *Official* Setup Guide: https://github.com/tensorflow/models/tree/master/research/inception
  - Skip to "How to Fine-Tune a Pre-Trained Model on a New Task"
  - https://github.com/tensorflow/models/tree/master/research/inception
* Inception-v3 *Unofficial* Setup Guide: https://medium.com/towards-data-science/deep-learning-with-tensorflow-part-2-image-classification-58fcdffa7b84 
