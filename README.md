# A simple Image classification annotation tool
-------------------------------------------------------------

This is a python based graphical tool that lets you quickly flip through datasets of images to categorize them.
\
The original script was written by Ryan Mones - https://github.com/rmones/tkteach

Want to try a more sophisticated image annotation platform? [Learn more about the Mindkosh image annotation platform here.](https://mindkosh.com/annotation-platform/image-annotation.html)

![Screenshot from 2024-01-25 13-08-33](https://github.com/Mindkosh/image-classification-labeler/assets/4280242/ea8c5343-f5b9-4dc0-b900-6022d1ed3d8f)


Getting started
----------
**Install required packaged**

Run python install -r requirements.txt to install required packages.

\
**Setup class labels**

Write your labels in categories.config file in the config directory.

Format:
(keyboard-shortcut) label-name


eg.

(A) Bike
\
(B) Car
\
(C) Pedestrian

\
**Setup dataset locations**

Create a datasets.config file in the config directory if it does not already exist. Then enter your dataset locations in the file - one dataset location in one line. The entered locations should be the root directory containing the images.

Format:
dataset-location


eg.

/home/username/documents/dataset1
\
/home/username/documents/dataset2
\
/home/username/pictures/dataset3


\
**Run the tool**

Run python run.py to run the tool.

\
\
Using the tool
----------
\
**Navigation**
1. Once you have setup your labels and dataset locations, you are ready to label.
2. All your provided dataset locations will appear in the _Dataset Location_ panel on the left
3. Select a dataset to start labeling.
4. Use the next and previous buttons or the left and right arrow keys on the keyboard to move to the next or previous image
5. You can also directly go to an image, by entering the the image number on the left and pressing the _Go_ button
6. The tool saves the last image you labeled, so when you open the tool the next time you can start where you left off.
7. If you want to only see unlabeled images, check the _Show unlabeled images_ checkbox.

**Labeling**
1. To zoom into an image, use the scroll wheel. You can also zoom in using the zoom buttons on the left.
2. To move around the image hold the left mouse button and move the mouse. 
3. To assign a label to an image, click on the label in the _Categories_ panel on the left.
   8.1. Or press the shortcut key specified in the categories.config file.
   8.2. You can assign multiple labels to a file.
   8.3. Your labels are saved in a sqlite file named _storage.db_ in the root of the repository directory.
   8.4. To export the labels, click the export button on the left. This will export the labels and the filenames in CSV format.
    

\
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

\
About
-----------

- Tested with Python >= 3.7
