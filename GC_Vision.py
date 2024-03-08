# Imports the Google Cloud client library
from google.cloud import vision
import os
import yaml






def filter_labels(labels):
    # Define a list of labels that you want to exclude
    exclude_labels = ['girl', 'boy', 'explicit', 'nudities']

    # Define a dictionary to combine related labels
    combine_labels = {
        'Skyscraper': 'Building',
        'Tower': 'Building'
    }

    # Filter out the excluded labels
    filtered_labels = [label for label in labels if label.description not in exclude_labels]

    # Combine related labels
    combined_labels = []
    for label in filtered_labels:
        if label.description in combine_labels:
            combined_labels.append(combine_labels[label.description])
        else:
            combined_labels.append(label.description)

    # Remove duplicates
    final_labels = list(set(combined_labels))

    return final_labels

def run_quickstart(image_path, use_vision_api=False, labels_set='labels_set_1', image_style='Photo') -> vision.EntityAnnotation:
    """Provides a quick start example for Cloud Vision."""
    # Load the labels and image styles from the YAML file
    with open('configs.yaml', 'r') as f:
        configs = yaml.safe_load(f)
        
    try:
        if use_vision_api:
            # Instantiates a client
            client = vision.ImageAnnotatorClient()

            # Load the image from the local file system
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            # Create an Image object and set its content to the image data
            image = vision.Image(content=image_data)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            # Filter the labels
            filtered_labels = filter_labels(labels)

            # Add the labels from the labels_set to the filtered_labels
            filtered_labels += [f'[{label}]' for label in configs[labels_set]]
            
            # Add the image style to the labels
            filtered_labels.insert(0, image_style)
            
            print ([label.description if isinstance(label, vision.EntityAnnotation) else label for label in filtered_labels])
            return [label.description if isinstance(label, vision.EntityAnnotation) else label for label in filtered_labels]

        else:
            # Use the specified set of labels
            labels = [f'[{label}]' for label in configs[labels_set]]

            # Add the image style to the labels
            labels.insert(0, image_style)

            print(labels)
            return labels

    except Exception as e:
        print(f"An error occurred: {e}")
        
#TESTING SCRIPT         
#run_quickstart('D:\\13-SPURE\\Source\\Background_PostApo_ref_2\\Rev_PostApo_00060_.png', False)