# The Data Incubator Capstone Project

This project proposes an alternative method to input the user's preferences in 
dating apps using image recognition. The final product is an app that can be deployed
as a flask on Spyder by running the file **app.py**. The free Heroku profile would not
accept a large dataset for full online deployment. Also, please keep in mind that
github reduced the dataset size from 5000-6000 images to 1000 images for both men and women.

## 1: Download

- Download this repository by cloning "https://github.com/akhorshid1/flask-image-browser.git"

## 2: Image Processing

- All the processing has been already done for the images stored in this repository, so the
previous steps should only be performed if the user wishes to process a new dataset.
- The **classify_image_oop.py** contains the basic components for the ImageNet model
used for image classification in an objected oriented format. This code will download 
the ImageNet model in your /tmp folder if it does not already exist.
- Running the **main.py** file will slice the entire image dataset in the *data_dir* directory
and output all the sliced images in the *output_dir* directory. This code will only run if the
module image_slice is installed ($ pip install image_slicer). Once the slicing is done,
the code will call on **classify_image_oop.py** to predict the class of the entire dataset
and append the results to a .csv file that will get stored locally. 
The results include the prediction with the highest certainty and the score from the ImageNet model prediction.
- Warning: processing a dataset could take hours, so keep this in mind before doing so!

## 3: Deploy the App
- Simply run the **app.py** in a spyder kernel, which will produce a local link to use the app
in your browser
- Ex: "* Running on http://127.0.0.1:33507/ (Press CTRL+C to quit)"