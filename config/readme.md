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