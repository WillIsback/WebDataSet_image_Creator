""" Project Description: WebDataSet_image_Creator

Step 1: Resize the image to 512 and renamed it to xxx.jpg

Step 2 :Generate a text description of the image file and sate it to xxx.txt

Step 3 : Create a tar file with the the processed image and text files

@Author: William Derue

@Date: 07/03/2024

@Version: 1.0

@License: GNU General Public License v3.0

"""

import webdataset as wds
import os
import tarfile
from PIL import Image
import glob
from GC_Vision import run_quickstart
import yaml


#function to resize the image
def resize_image(input_image_path, output_image_path, size=512):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print(f"The original image size is {width} wide x {height} tall")

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate the new dimensions while maintaining the aspect ratio
    new_width = size
    new_height = round(size / aspect_ratio)

    # Resize the image
    resized_image = original_image.resize((new_width, new_height))

    width, height = resized_image.size
    print(f"The resized image size is {width} wide x {height} tall")

    resized_image.save(output_image_path)

#function to generate a text description of the image file
def generate_text_description(image_path, text_file_path, use_vision_api, labels_set, image_style):
    
    # Get the labels for the image
    labels = run_quickstart(image_path, use_vision_api, labels_set, image_style=image_style)


    # If labels is None or a single label, make it a list
    if labels is None:
        labels = []
    elif not isinstance(labels, list):
        labels = [labels]
        
    # Write the labels to the text file
    with open(text_file_path, 'w') as f:
        f.write(image_path + ": " + ', '.join(labels))
        
#function to create a tar file with the processed image and text files
def create_tar_file(output_tar_path, files):
    with tarfile.open(output_tar_path, "w") as tar:
        for file in files:
            tar.add(file)



# Specify the path to your images
image_folder_path = 'Sample\Background_PostApo_ref_2'

# Specify the output directory
output_directory = 'output'

# Check if the output directory exists, if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
# Get a list of all image files
image_files = glob.glob(f'{image_folder_path}/*.jpg') + glob.glob(f'{image_folder_path}/*.png')

# Load the image styles from the YAML file
with open('configs.yaml', 'r') as f:
    configs = yaml.safe_load(f)
image_styles = configs['image_styles']

# Load the label sets from the YAML file
label_sets = {key: value for key, value in configs.items() if key.startswith('labels_set')}

# Prompt the user to choose a set of labels
print("Please choose a set of labels:")
for i, (key, labels) in enumerate(label_sets.items(), start=1):
    print(f"{i}. {key}: {labels}")
choice = int(input("Enter the number of your choice: ")) - 1
chosen_label_set = list(label_sets.keys())[choice]

# Prompt the user to choose an image style
print("Please choose an image style:")
for i, style in enumerate(image_styles, start=1):
    print(f"{i}. {style}")
choice = int(input("Enter the number of your choice: ")) - 1
chosen_style = image_styles[choice]

# Step 3 : Create a tar file with the processed image and text files
output_tar_path = 'output.tar'
tar = tarfile.open(output_tar_path, "w")

#Main process Loop
#--------------------------------------------------------------
for i, input_image_path in enumerate(image_files, start=1):
    

    # Format the output image path
    output_image_path = os.path.join(output_directory, f'{str(i).zfill(3)}.jpg')#str(i).zfill(3) is used to pad the file name with leading zeros
    
    # Step 1: Resize the image to 512x512 and renamed it to xxx.jpg
    #--------------------------------------------------------------
    resize_image(input_image_path, output_image_path, size=(512))#size=(512) is the new size of the image
    
    # Step 2 :Generate a text description of the image file and save it to xxx.txt
    #--------------------------------------------------------------
    text_file_path = os.path.join(output_directory, f'{str(i).zfill(3)}.txt')
    generate_text_description(input_image_path, text_file_path, False, chosen_label_set, chosen_style)

    # Step 3 : Create a tar file with the processed image and text files
    #--------------------------------------------------------------
    # Add the image and text files to the tar file
    tar.add(output_image_path, arcname=f'{str(i).zfill(3)}.jpg')
    tar.add(text_file_path, arcname=f'{str(i).zfill(3)}.txt')
    
# Close the tar file
tar.close()  
#--------------------------------------------------------------


    
