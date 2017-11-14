Website
 - General
   * Choose a color scheme for all the templates so that we have one look
   
 - Home
   * ~~Logo for DermaGram in top left-hand corner (this launches home.html)~~
   * Another link (or icon) for home in the top right-hand corner next to 'Login' and 'Sign Up'.
   * More descriptive notes about DermaGram
   * A link to our github page
   * Pictures of each team member (or avatar if you prefer)
   * Update descriptive info. for each team member (whatever you'd like to share online)

- Login/Sign Up
  * Merge these two templates (as per the teacher's recommendation)
  * Ensure the logic for login() and register() that calls templates is well tested for edge cases

- Profile
  * ~~Image upload: need to write code such that when file is uploded, it appears in right-hand side~~
  * ~~Image upload: the details written into the control boxes should be stored in imgur w/ the image.~~
  * Image analysis: Hook into our model to analyze the image and return a classification
  * Image analysis: There should be a box that returns the classification result after analysis is complete.
  * ~~Image analysis: update the image in imgur w/ this new classification so we can retrieve in image_table.html~~
  * Progress bar: the progress bar should indicate the progress of the image classification while we wait for response
  * ~~Image table: the items that are labeled Malignant should be highlighted red~~
  * Image table: clicking on an image in the table should auto-slide the image_carousel to that image, and vice versa
  * Image sizing: use CSS to control how much space uploaded image takes - the image size should be adjusted to fit the template
  
Model
 - Model: Choose a model (tensorflow / alexnet / etc)
 - Data: Upload a clean set of training and evaluation data to imgur w/ the correct dimensions
 - Data: Try to go through the set of images and exclude the ones that are the worst (black borders / hair / rulers on skin)
 - Train: train the model and try to beat 0.50
 - Website: figure out how to connect our website to the model to retrieve classification for image
 - Website: figure out how this model can be loaded to server so that it doesn't need to be run from personal computer 
