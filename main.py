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
import sys

#function to resize the image
def resize_image(input_image_path, output_image_path, size=512, method=None, crop_choice=None):
    original_image = Image.open(input_image_path)
    
    original_width, original_height = original_image.size 
    # Check if the image is square
    if original_width != original_height:
        print("The image is not square.")
        if crop_choice.lower() == 'yes':
            # Crop the image to a square
            min_dim = min(original_width, original_height)
            left = (original_width - min_dim) / 2
            top = (original_height - min_dim) / 2
            right = (original_width + min_dim) / 2
            bottom = (original_height + min_dim) / 2
            original_image = original_image.crop((left, top, right, bottom))
            print("The image has been cropped to a square.")
            
    width, height = original_image.size 
          
    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate the new dimensions while maintaining the aspect ratio
    new_width = size
    new_height = round(size / aspect_ratio)

    # If the method is not provided, ask the user for it
    if method is None:
        print("Which method do you want to use for resizing the image?")
        print("1. Nearest neighbor")
        print("2. Bilinear")
        print("3. Bicubic")
        print("4. Lanczos")
        method = input("Enter the number of your choice: ")

    # Resize the image using the chosen method
    if method == '1':
        resized_image = original_image.resize((new_width, new_height), Image.NEAREST)
    elif method == '2':
        resized_image = original_image.resize((new_width, new_height), Image.BILINEAR)
    elif method == '3':
        resized_image = original_image.resize((new_width, new_height), Image.BICUBIC)
    elif method == '4':
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    else:
        print("Invalid choice. Using the nearest neighbor method by default.")
        resized_image = original_image.resize((new_width, new_height), Image.NEAREST)

    width, height = resized_image.size
    print(f"The resized image size is {width} wide x {height} tall")

    resized_image.save(output_image_path)

    # Return the chosen method along with the resized image
    return method
    
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
        f.write(', '.join(labels))        



# Specify the path to your images
image_folder_path = 'Sample\Background_PostApo_ref_2'

# Check if the path exists
if not os.path.exists(image_folder_path):
    print(f"Error: The path {image_folder_path} does not exist.")
    sys.exit(1)
    
# Ask the user for the output directory name
output_dir = input("Enter the output directory name: ")

# Check if the output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get a list of all image files
image_files = glob.glob(f'{image_folder_path}/*.jpg') + glob.glob(f'{image_folder_path}/*.png')

# Load the image styles from the YAML file
with open('configs.yaml', 'r') as f:
    configs = yaml.safe_load(f)
image_styles = configs['image_styles']

# Load the label sets from the YAML file
label_sets = {key: value for key, value in configs.items() if key.startswith('labels_set')}

# Prompt the user to enter a desired size dimension for the image
print("Please enter a desired size dimension for the image (default is 512):")
size = input("Enter the size: ")

# If the user didn't enter anything, use the default size
if not size:
    size = 512
else:
    size = int(size)

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




#Main process Loop
#--------------------------------------------------------------

with tarfile.open(os.path.join(output_dir, f'{output_dir}.tar'), 'w') as tar:
    method = None #method is used to resize the image
    crop_choice= None #crop_choice is used to crop the image
    
    # Ask the user once if they want to crop the images
    crop_choice = input("Do you want to crop the images before resizing them? (yes/no): ")
    
    for i, input_image_path in enumerate(image_files, start=1):
        

        # Format the output image path
        output_image_path = os.path.join(output_dir, f'{str(i).zfill(3)}.jpg')#str(i).zfill(3) is used to pad the file name with leading zeros
        
        # Step 1: Crop and Resize the image before renaming it to xxx.jpg
        #--------------------------------------------------------------
        method = resize_image(input_image_path, output_image_path, size, method, crop_choice)
        
        # Step 2 :Generate a text description of the image file and save it to xxx.txt
        #--------------------------------------------------------------
        text_file_path = os.path.join(output_dir, f'{str(i).zfill(3)}.txt')
        generate_text_description(input_image_path, text_file_path, False, chosen_label_set, chosen_style)
        

    # Step 3 : Create a tar file with the processed image and text files
    #--------------------------------------------------------------
    # Add the image and text files to the tar file
    # Add the output directory and its files to the tar file
    tar.add(output_dir, arcname=os.path.basename(output_dir))
        
#--------------------------------------------------------------


    
