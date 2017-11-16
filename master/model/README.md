#Inference
To get the prediction for an image, run trial.py and pass the image with the --image_test flag and the model directory with --model_dir
(if loading the model fails, give the absolute path for the model directory)

Trained model weights are stored in model.ckpt-1989.data-00000-of-00001 and the graph is stored in graph.pbtxt
vgg_preprocessing.py is used to preprocess the image and resnet_model.py has the architecture for the resnet model.

Format of the prediction:
[p0, p1, p2]
where p0 is confidence for background (unsure), p1 is confidence for benign and p2 for malignant

