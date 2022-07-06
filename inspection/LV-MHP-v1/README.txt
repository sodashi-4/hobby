List of contents:

./images:
    All images in the dataset. 

./annotations
    The segmentation annotation files corresponding to the images. 

    One image is corresponding to multiple annotation files with the same prefix, one file per person. In each annotation file, the label represents:

    0:  background
    1:  hat
    2:  hair
    3:  sunglass
    4:  upper-clothes
    5:  skirt
    6:  pants
    7:  dress
    8:  belt 
    9:  left-shoe
    10: right-shoe
    11: face
    12: left-leg
    13: right-leg
    14: left-arm 
    15: right-arm
    16: bag
    17: scarf
    18: torso-skin

./visualization.m
    Matlab script to visualize the annotations


./train_list.txt
    The list of images for training and validataion

./test_list.txt
    The list of images for testing