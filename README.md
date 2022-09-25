# image-classification-labeler
A Super simple and quick Image Classification Tool Written in Python
-------------------------------------------------------------

This is a graphical tool that lets you quickly flip through datasets of images to categorize them.
The original script was written by Ryan Mones - https://github.com/rmones/tkteach


Getting started
----------
Run python install -r requirements.txt to install required packages.

Write your labels in categories.config file in the config directory.
Format:
(<key-shortcut>) <label-name>

eg.
(A) Bike
(B) Car
(C) Pedestrian


Write your dataset locations in datasets.config file in the config directory. The entered locations should contain the images.
Format:
<dataset-location>

eg.
/home/username/documents/dataset1
/home/username/documents/dataset2
/home/username/pictures/dataset3


Run python run.py to run the tool.


Features
----------

- Easily customizable categories and keyboard shortcuts
- Categorization can be done with arrow keys and keyboard shortcuts for improved speed, OR can be done with the mouse
- Category labels saved to sqLite database for easy retrieval
- Operates on one or more user-collected datasets of images
- Images can be zoomed in or out
- Allows multiple categorizations per image
- Shows number of unlabeled images
- Allows navigating between unlabeled images


About
-----------

- Tested with Python >= 3.7