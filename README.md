# wasatch-forests

This application is currently running at www.wasatch-forests.us.

The application displays 144 aerial image segmentations into species labels.

The categories and colors for these labels are as follows:

|   | Class   | Color       |
|---|---------|-------------|
| 1 | Maple   | Red         |
| 2 | Aspen   | Yellow      |
| 3 | Oak     | Orange      |
| 4 | Conifer | Dark Green  |
| 5 | Other   | Lime Green  |
| 6 | None    | Light Beige |

The segmented images were created by training a 3D Convolutional Neural Net on images of the Wasatch Range in Northern Utah downloaded from the USGS EarthExplorer portal. 3 of the 144 images were used for training and testing. Another 3 were used exclusively for testing to see how well the model would scale up to images not seen in training.

I labeled these 6 images manually using the application GIMP to create partial ground truth images. Predictions on the 3 test images were around 75% accurate. These are good preliminary results that could be improved by labeling more of each of the training images and adding more labeled images for training. The model creation process is detailed in wasatch_model_no_images.ipynb. Some of the cell outputs of this notebook have been removed to decrease file size for upload.

Once the model was created, prediction images were made for all 144 images in the dataset (predict_wasatch.py), then compressed to ease memory needs for display (compress_images.py). Each image was also downloaded with text information related to them, from which bounding coordinates were extracted and saved to a new text file (extract_coordinates.py).

A Dash app was then created using the dash-leaflet library for display (wasatch_map_app.py). The compressed images and coordinates are found in the "assets" folder. The app is hosted using Pythonanywhere at www.wasatch-forests.us.
