# WebDataSet Image Creator

This project is a Python script that processes a set of images and generates a tar file compatible with the WebDataset library. The script performs the following steps:

1. Resizes each image to a width of 512 pixels per default while maintaining the aspect ratio.
2. Generates a text description of each image using the Google Cloud Vision API or not and also specify a few customs labels (lora training).
3. Packs the processed images and their corresponding text descriptions into a tar file.

## Description:
I did this little project to build dataset for training StableCascade image generative AI from [Stability-AI](https://github.com/Stability-AI/StableCascade).
Also I use google cloud VISION api to generate image labels for training. This service don't have free tier anymore and I have not found an alternative yet.
You will need a json key file and to activate the facturation to use this API.
Per default the use is set to `use_vision_api=False`. Documentation -> [Vision API](https://cloud.google.com/vision/docs/)
Finally the results of the dataset is a output folder filled with image and text file matching and a .tar file, all in the expected format for [WebDataSet](https://github.com/webdataset/webdataset).

here a sample result printing from the terminal :
```bash
The original image size is 768 wide x 512 tall
The resized image size is 512 wide x 341 tall
['Futurism', 'postapocalyptic', 'city', 'desolated']
```



## Requirements

- Python 3.6 or higher
- PIL (Pillow)
- glob
- tarfile
- Google Cloud Vision API
- yaml

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/WebDataSet_Image_Creator.git
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```
3. Run the script:
```bash
python main.py
```

## Configuration
You can specify the path to your images and the output directory at the top of the main.py script:
```Python
# Specify the path to your images
image_folder_path = 'Sample\Background_PostApo_ref_2'

# Specify the output directory
output_directory = 'output'
```

You can choose a style from a list when running the script, feel free to add specifyc styles in the configs.yaml file:
```yaml
image_styles:
  - style1
  - style2
  - style3
```
You also can specify a labels in the configs.yaml file:
```yaml
#list of image labels
labels_set_1: ['postapocalyptic', 'city', 'desolated']
#labels_set_2: ['postapocalyptic', 'landscape', 'desolated']
# Add more sets of labels as needed
```

@This project is licensed under the terms of the GNU General Public License v3.0
